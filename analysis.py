import pandas as pd, numpy as np, json
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
rng=np.random.default_rng(2026)
df=pd.read_csv("data/penguins.csv")
R={}
R["n_total"]=len(df)
d=df.dropna(subset=["body_mass_g","sex"]).copy()
R["n_clean"]=len(d)
R["missing"]=int(df.body_mass_g.isna().sum()), int(df.sex.isna().sum())
x=d.body_mass_g.values
R["desc"]={"mean":x.mean(),"sd":x.std(ddof=1),"min":x.min(),"max":x.max(),"median":float(np.median(x))}
# group desc
g=d.groupby("species").body_mass_g.agg(["count","mean","std","min","max"])
R["groups"]=g.reset_index().to_dict("records")
# normality
R["shapiro_all"]=stats.shapiro(x)
R["shapiro_sp"]={s:tuple(stats.shapiro(v.body_mass_g)) for s,v in d.groupby("species")}
# figure 1: hist overall vs by species
fig,ax=plt.subplots(1,2,figsize=(8,3.2))
ax[0].hist(x,bins=20,color="#7a9cc6",edgecolor="white");ax[0].set_title("All penguins (n=%d)"%len(x));ax[0].set_xlabel("Body mass, g")
for s,c in zip(["Adelie","Chinstrap","Gentoo"],["#e07b39","#6a4c93","#2a9d8f"]):
    ax[1].hist(d[d.species==s].body_mass_g,bins=15,alpha=.7,label=s,color=c,edgecolor="white")
ax[1].legend(frameon=False);ax[1].set_title("By species");ax[1].set_xlabel("Body mass, g")
plt.tight_layout();plt.savefig("fig/f1.png",dpi=200);plt.close()
# QQ
fig,ax=plt.subplots(1,3,figsize=(8,2.9))
for a,s in zip(ax,["Adelie","Chinstrap","Gentoo"]):
    stats.probplot(d[d.species==s].body_mass_g,plot=a);a.set_title(s);a.get_lines()[0].set_markersize(3);a.set_xlabel("Theoretical quantiles");a.set_ylabel("Sample" if s=="Adelie" else "")
plt.tight_layout();plt.savefig("fig/f2.png",dpi=200);plt.close()
# CI for mean per species
def ci_mean(v,conf=.95):
    n=len(v);m=v.mean();s=v.std(ddof=1);se=s/np.sqrt(n)
    t=stats.t.ppf(1-(1-conf)/2,n-1);z=stats.norm.ppf(1-(1-conf)/2)
    return dict(n=n,mean=m,s=s,se=se,t=t,z=z,t_lo=m-t*se,t_hi=m+t*se,z_lo=m-z*se,z_hi=m+z*se)
def ci_var(v,conf=.95):
    n=len(v);s2=v.var(ddof=1);a=1-conf
    lo=(n-1)*s2/stats.chi2.ppf(1-a/2,n-1);hi=(n-1)*s2/stats.chi2.ppf(a/2,n-1)
    return dict(s2=s2,lo=lo,hi=hi,sd_lo=np.sqrt(lo),sd_hi=np.sqrt(hi),c1=stats.chi2.ppf(1-a/2,n-1),c2=stats.chi2.ppf(a/2,n-1))
R["ci_all"]=ci_mean(x)
R["ci_sp"]={s:ci_mean(v.body_mass_g.values) for s,v in d.groupby("species")}
R["ci_var_sp"]={s:ci_var(v.body_mass_g.values) for s,v in d.groupby("species")}
R["ci_var_all"]=ci_var(x)
# confidence level comparison for Gentoo
gen=d[d.species=="Gentoo"].body_mass_g.values
R["levels"]={c:ci_mean(gen,c) for c in [.90,.95,.99]}
# sample size effect (Adelie)
ad=d[d.species=="Adelie"].body_mass_g.values
ns=[10,20,40,80,len(ad)]
R["ssize"]=[]
for n in ns:
    sub=rng.choice(ad,n,replace=False);c=ci_mean(sub);R["ssize"].append((n,c["mean"],c["t_lo"],c["t_hi"],c["t_hi"]-c["t_lo"]))
# difference male vs female per species (Welch)
R["diff"]={}
for s,v in d.groupby("species"):
    m=v[v.sex=="MALE"].body_mass_g.values;f=v[v.sex=="FEMALE"].body_mass_g.values
    diff=m.mean()-f.mean();va=m.var(ddof=1)/len(m);vb=f.var(ddof=1)/len(f);se=np.sqrt(va+vb)
    df_=(va+vb)**2/(va**2/(len(m)-1)+vb**2/(len(f)-1));t=stats.t.ppf(.975,df_)
    R["diff"][s]=dict(nm=len(m),nf=len(f),mm=m.mean(),mf=f.mean(),diff=diff,se=se,df=df_,lo=diff-t*se,hi=diff+t*se,p=stats.ttest_ind(m,f,equal_var=False).pvalue)
# proportion: share of males among all (n=333)
k=(d.sex=="MALE").sum();n=len(d);p=k/n;z=1.959964
R["prop"]=dict(k=int(k),n=n,p=p,wald=(p-z*np.sqrt(p*(1-p)/n),p+z*np.sqrt(p*(1-p)/n)))
c=(p+z*z/(2*n))/(1+z*z/n);h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n);R["prop"]["wilson"]=(c-h,c+h)
# sample size needed for margin E=50g for Gentoo: n=(z s/E)^2
s_g=gen.std(ddof=1);R["need"]={"s":s_g,"E50":int(np.ceil((1.959964*s_g/50)**2)),"E25":int(np.ceil((1.959964*s_g/25)**2))}
# Simulation of coverage: population = Gentoo (treated as pop), samples n=15 and 30
cov={}
mu=gen.mean()
for n in [5,10,30]:
    hit_t=hit_z=0;N=10000
    for _ in range(N):
        sm=rng.choice(gen,n,replace=True);m=sm.mean();s=sm.std(ddof=1)
        t=stats.t.ppf(.975,n-1);hit_t+= abs(m-mu)<=t*s/np.sqrt(n)
        hit_z+= abs(m-mu)<=1.959964*s/np.sqrt(n)
    cov[n]=(hit_t/N,hit_z/N)
R["cov"]=cov
# figure 3: 100 intervals n=30
fig,ax=plt.subplots(figsize=(6.5,4))
miss=0
for i in range(50):
    sm=rng.choice(gen,30,replace=True);m=sm.mean();h=stats.t.ppf(.975,29)*sm.std(ddof=1)/np.sqrt(30)
    ok=abs(m-mu)<=h;miss+=(not ok)
    ax.plot([m-h,m+h],[i,i],color="#2a9d8f" if ok else "#d62828",lw=1.6)
ax.axvline(mu,color="k",ls="--",lw=1);ax.set_xlabel("Body mass, g");ax.set_ylabel("Sample #")
ax.set_title(f"50 CIs (95%, n=30). Red = missed the true mean ({miss} of 50)")
plt.tight_layout();plt.savefig("fig/f3.png",dpi=200);plt.close()
R["miss50"]=int(miss)
# figure 4: CI plot per species and sex
fig,ax=plt.subplots(figsize=(6.5,3.4))
yl=[];i=0
for s,v in d.groupby("species"):
    for sx,c in [("FEMALE","#e07b39"),("MALE","#2a6f97")]:
        w=v[v.sex==sx].body_mass_g.values;ci=ci_mean(w)
        ax.errorbar(ci["mean"],i,xerr=ci["t"]*ci["se"],fmt="o",color=c,capsize=4,label=sx.title() if s=="Adelie" else None)
        yl.append(f"{s}, {sx.lower()} (n={len(w)})");i+=1
ax.set_yticks(range(i));ax.set_yticklabels(yl);ax.invert_yaxis();ax.legend(frameon=False);ax.set_xlabel("Mean body mass with 95% CI, g")
plt.tight_layout();plt.savefig("fig/f4.png",dpi=200);plt.close()
# bootstrap check Gentoo
bs=[rng.choice(gen,len(gen)).mean() for _ in range(10000)]
R["boot"]=tuple(np.percentile(bs,[2.5,97.5]))
def conv(o):
    if isinstance(o,dict):return {str(k):conv(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [conv(v) for v in o]
    if isinstance(o,(np.floating,np.integer)):return o.item()
    return o
json.dump(conv(R),open("results.json","w"),indent=1,ensure_ascii=False)
print(json.dumps(conv(R),indent=1,ensure_ascii=False))
