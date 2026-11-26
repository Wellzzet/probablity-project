"""Confidence intervals for penguin body mass - interactive site.
Course: Theory of Probability and Mathematical Statistics (Narxoz University).
Run:  pip install streamlit pandas numpy scipy matplotlib
      streamlit run app.py
Data: Palmer Penguins (Gorman et al., 2014; Horst et al., 2020), embedded below.
"""
import io
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy import stats

st.set_page_config(page_title="Confidence Intervals: Penguins", page_icon="🐧", layout="wide")
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "font.size": 10})

CSV = """species,island,bill_length_mm,bill_depth_mm,flipper_length_mm,body_mass_g,sex
Adelie,Torgersen,39.1,18.7,181,3750,MALE
Adelie,Torgersen,39.5,17.4,186,3800,FEMALE
Adelie,Torgersen,40.3,18,195,3250,FEMALE
Adelie,Torgersen,,,,,
Adelie,Torgersen,36.7,19.3,193,3450,FEMALE
Adelie,Torgersen,39.3,20.6,190,3650,MALE
Adelie,Torgersen,38.9,17.8,181,3625,FEMALE
Adelie,Torgersen,39.2,19.6,195,4675,MALE
Adelie,Torgersen,34.1,18.1,193,3475,
Adelie,Torgersen,42,20.2,190,4250,
Adelie,Torgersen,37.8,17.1,186,3300,
Adelie,Torgersen,37.8,17.3,180,3700,
Adelie,Torgersen,41.1,17.6,182,3200,FEMALE
Adelie,Torgersen,38.6,21.2,191,3800,MALE
Adelie,Torgersen,34.6,21.1,198,4400,MALE
Adelie,Torgersen,36.6,17.8,185,3700,FEMALE
Adelie,Torgersen,38.7,19,195,3450,FEMALE
Adelie,Torgersen,42.5,20.7,197,4500,MALE
Adelie,Torgersen,34.4,18.4,184,3325,FEMALE
Adelie,Torgersen,46,21.5,194,4200,MALE
Adelie,Biscoe,37.8,18.3,174,3400,FEMALE
Adelie,Biscoe,37.7,18.7,180,3600,MALE
Adelie,Biscoe,35.9,19.2,189,3800,FEMALE
Adelie,Biscoe,38.2,18.1,185,3950,MALE
Adelie,Biscoe,38.8,17.2,180,3800,MALE
Adelie,Biscoe,35.3,18.9,187,3800,FEMALE
Adelie,Biscoe,40.6,18.6,183,3550,MALE
Adelie,Biscoe,40.5,17.9,187,3200,FEMALE
Adelie,Biscoe,37.9,18.6,172,3150,FEMALE
Adelie,Biscoe,40.5,18.9,180,3950,MALE
Adelie,Dream,39.5,16.7,178,3250,FEMALE
Adelie,Dream,37.2,18.1,178,3900,MALE
Adelie,Dream,39.5,17.8,188,3300,FEMALE
Adelie,Dream,40.9,18.9,184,3900,MALE
Adelie,Dream,36.4,17,195,3325,FEMALE
Adelie,Dream,39.2,21.1,196,4150,MALE
Adelie,Dream,38.8,20,190,3950,MALE
Adelie,Dream,42.2,18.5,180,3550,FEMALE
Adelie,Dream,37.6,19.3,181,3300,FEMALE
Adelie,Dream,39.8,19.1,184,4650,MALE
Adelie,Dream,36.5,18,182,3150,FEMALE
Adelie,Dream,40.8,18.4,195,3900,MALE
Adelie,Dream,36,18.5,186,3100,FEMALE
Adelie,Dream,44.1,19.7,196,4400,MALE
Adelie,Dream,37,16.9,185,3000,FEMALE
Adelie,Dream,39.6,18.8,190,4600,MALE
Adelie,Dream,41.1,19,182,3425,MALE
Adelie,Dream,37.5,18.9,179,2975,
Adelie,Dream,36,17.9,190,3450,FEMALE
Adelie,Dream,42.3,21.2,191,4150,MALE
Adelie,Biscoe,39.6,17.7,186,3500,FEMALE
Adelie,Biscoe,40.1,18.9,188,4300,MALE
Adelie,Biscoe,35,17.9,190,3450,FEMALE
Adelie,Biscoe,42,19.5,200,4050,MALE
Adelie,Biscoe,34.5,18.1,187,2900,FEMALE
Adelie,Biscoe,41.4,18.6,191,3700,MALE
Adelie,Biscoe,39,17.5,186,3550,FEMALE
Adelie,Biscoe,40.6,18.8,193,3800,MALE
Adelie,Biscoe,36.5,16.6,181,2850,FEMALE
Adelie,Biscoe,37.6,19.1,194,3750,MALE
Adelie,Biscoe,35.7,16.9,185,3150,FEMALE
Adelie,Biscoe,41.3,21.1,195,4400,MALE
Adelie,Biscoe,37.6,17,185,3600,FEMALE
Adelie,Biscoe,41.1,18.2,192,4050,MALE
Adelie,Biscoe,36.4,17.1,184,2850,FEMALE
Adelie,Biscoe,41.6,18,192,3950,MALE
Adelie,Biscoe,35.5,16.2,195,3350,FEMALE
Adelie,Biscoe,41.1,19.1,188,4100,MALE
Adelie,Torgersen,35.9,16.6,190,3050,FEMALE
Adelie,Torgersen,41.8,19.4,198,4450,MALE
Adelie,Torgersen,33.5,19,190,3600,FEMALE
Adelie,Torgersen,39.7,18.4,190,3900,MALE
Adelie,Torgersen,39.6,17.2,196,3550,FEMALE
Adelie,Torgersen,45.8,18.9,197,4150,MALE
Adelie,Torgersen,35.5,17.5,190,3700,FEMALE
Adelie,Torgersen,42.8,18.5,195,4250,MALE
Adelie,Torgersen,40.9,16.8,191,3700,FEMALE
Adelie,Torgersen,37.2,19.4,184,3900,MALE
Adelie,Torgersen,36.2,16.1,187,3550,FEMALE
Adelie,Torgersen,42.1,19.1,195,4000,MALE
Adelie,Torgersen,34.6,17.2,189,3200,FEMALE
Adelie,Torgersen,42.9,17.6,196,4700,MALE
Adelie,Torgersen,36.7,18.8,187,3800,FEMALE
Adelie,Torgersen,35.1,19.4,193,4200,MALE
Adelie,Dream,37.3,17.8,191,3350,FEMALE
Adelie,Dream,41.3,20.3,194,3550,MALE
Adelie,Dream,36.3,19.5,190,3800,MALE
Adelie,Dream,36.9,18.6,189,3500,FEMALE
Adelie,Dream,38.3,19.2,189,3950,MALE
Adelie,Dream,38.9,18.8,190,3600,FEMALE
Adelie,Dream,35.7,18,202,3550,FEMALE
Adelie,Dream,41.1,18.1,205,4300,MALE
Adelie,Dream,34,17.1,185,3400,FEMALE
Adelie,Dream,39.6,18.1,186,4450,MALE
Adelie,Dream,36.2,17.3,187,3300,FEMALE
Adelie,Dream,40.8,18.9,208,4300,MALE
Adelie,Dream,38.1,18.6,190,3700,FEMALE
Adelie,Dream,40.3,18.5,196,4350,MALE
Adelie,Dream,33.1,16.1,178,2900,FEMALE
Adelie,Dream,43.2,18.5,192,4100,MALE
Adelie,Biscoe,35,17.9,192,3725,FEMALE
Adelie,Biscoe,41,20,203,4725,MALE
Adelie,Biscoe,37.7,16,183,3075,FEMALE
Adelie,Biscoe,37.8,20,190,4250,MALE
Adelie,Biscoe,37.9,18.6,193,2925,FEMALE
Adelie,Biscoe,39.7,18.9,184,3550,MALE
Adelie,Biscoe,38.6,17.2,199,3750,FEMALE
Adelie,Biscoe,38.2,20,190,3900,MALE
Adelie,Biscoe,38.1,17,181,3175,FEMALE
Adelie,Biscoe,43.2,19,197,4775,MALE
Adelie,Biscoe,38.1,16.5,198,3825,FEMALE
Adelie,Biscoe,45.6,20.3,191,4600,MALE
Adelie,Biscoe,39.7,17.7,193,3200,FEMALE
Adelie,Biscoe,42.2,19.5,197,4275,MALE
Adelie,Biscoe,39.6,20.7,191,3900,FEMALE
Adelie,Biscoe,42.7,18.3,196,4075,MALE
Adelie,Torgersen,38.6,17,188,2900,FEMALE
Adelie,Torgersen,37.3,20.5,199,3775,MALE
Adelie,Torgersen,35.7,17,189,3350,FEMALE
Adelie,Torgersen,41.1,18.6,189,3325,MALE
Adelie,Torgersen,36.2,17.2,187,3150,FEMALE
Adelie,Torgersen,37.7,19.8,198,3500,MALE
Adelie,Torgersen,40.2,17,176,3450,FEMALE
Adelie,Torgersen,41.4,18.5,202,3875,MALE
Adelie,Torgersen,35.2,15.9,186,3050,FEMALE
Adelie,Torgersen,40.6,19,199,4000,MALE
Adelie,Torgersen,38.8,17.6,191,3275,FEMALE
Adelie,Torgersen,41.5,18.3,195,4300,MALE
Adelie,Torgersen,39,17.1,191,3050,FEMALE
Adelie,Torgersen,44.1,18,210,4000,MALE
Adelie,Torgersen,38.5,17.9,190,3325,FEMALE
Adelie,Torgersen,43.1,19.2,197,3500,MALE
Adelie,Dream,36.8,18.5,193,3500,FEMALE
Adelie,Dream,37.5,18.5,199,4475,MALE
Adelie,Dream,38.1,17.6,187,3425,FEMALE
Adelie,Dream,41.1,17.5,190,3900,MALE
Adelie,Dream,35.6,17.5,191,3175,FEMALE
Adelie,Dream,40.2,20.1,200,3975,MALE
Adelie,Dream,37,16.5,185,3400,FEMALE
Adelie,Dream,39.7,17.9,193,4250,MALE
Adelie,Dream,40.2,17.1,193,3400,FEMALE
Adelie,Dream,40.6,17.2,187,3475,MALE
Adelie,Dream,32.1,15.5,188,3050,FEMALE
Adelie,Dream,40.7,17,190,3725,MALE
Adelie,Dream,37.3,16.8,192,3000,FEMALE
Adelie,Dream,39,18.7,185,3650,MALE
Adelie,Dream,39.2,18.6,190,4250,MALE
Adelie,Dream,36.6,18.4,184,3475,FEMALE
Adelie,Dream,36,17.8,195,3450,FEMALE
Adelie,Dream,37.8,18.1,193,3750,MALE
Adelie,Dream,36,17.1,187,3700,FEMALE
Adelie,Dream,41.5,18.5,201,4000,MALE
Chinstrap,Dream,46.5,17.9,192,3500,FEMALE
Chinstrap,Dream,50,19.5,196,3900,MALE
Chinstrap,Dream,51.3,19.2,193,3650,MALE
Chinstrap,Dream,45.4,18.7,188,3525,FEMALE
Chinstrap,Dream,52.7,19.8,197,3725,MALE
Chinstrap,Dream,45.2,17.8,198,3950,FEMALE
Chinstrap,Dream,46.1,18.2,178,3250,FEMALE
Chinstrap,Dream,51.3,18.2,197,3750,MALE
Chinstrap,Dream,46,18.9,195,4150,FEMALE
Chinstrap,Dream,51.3,19.9,198,3700,MALE
Chinstrap,Dream,46.6,17.8,193,3800,FEMALE
Chinstrap,Dream,51.7,20.3,194,3775,MALE
Chinstrap,Dream,47,17.3,185,3700,FEMALE
Chinstrap,Dream,52,18.1,201,4050,MALE
Chinstrap,Dream,45.9,17.1,190,3575,FEMALE
Chinstrap,Dream,50.5,19.6,201,4050,MALE
Chinstrap,Dream,50.3,20,197,3300,MALE
Chinstrap,Dream,58,17.8,181,3700,FEMALE
Chinstrap,Dream,46.4,18.6,190,3450,FEMALE
Chinstrap,Dream,49.2,18.2,195,4400,MALE
Chinstrap,Dream,42.4,17.3,181,3600,FEMALE
Chinstrap,Dream,48.5,17.5,191,3400,MALE
Chinstrap,Dream,43.2,16.6,187,2900,FEMALE
Chinstrap,Dream,50.6,19.4,193,3800,MALE
Chinstrap,Dream,46.7,17.9,195,3300,FEMALE
Chinstrap,Dream,52,19,197,4150,MALE
Chinstrap,Dream,50.5,18.4,200,3400,FEMALE
Chinstrap,Dream,49.5,19,200,3800,MALE
Chinstrap,Dream,46.4,17.8,191,3700,FEMALE
Chinstrap,Dream,52.8,20,205,4550,MALE
Chinstrap,Dream,40.9,16.6,187,3200,FEMALE
Chinstrap,Dream,54.2,20.8,201,4300,MALE
Chinstrap,Dream,42.5,16.7,187,3350,FEMALE
Chinstrap,Dream,51,18.8,203,4100,MALE
Chinstrap,Dream,49.7,18.6,195,3600,MALE
Chinstrap,Dream,47.5,16.8,199,3900,FEMALE
Chinstrap,Dream,47.6,18.3,195,3850,FEMALE
Chinstrap,Dream,52,20.7,210,4800,MALE
Chinstrap,Dream,46.9,16.6,192,2700,FEMALE
Chinstrap,Dream,53.5,19.9,205,4500,MALE
Chinstrap,Dream,49,19.5,210,3950,MALE
Chinstrap,Dream,46.2,17.5,187,3650,FEMALE
Chinstrap,Dream,50.9,19.1,196,3550,MALE
Chinstrap,Dream,45.5,17,196,3500,FEMALE
Chinstrap,Dream,50.9,17.9,196,3675,FEMALE
Chinstrap,Dream,50.8,18.5,201,4450,MALE
Chinstrap,Dream,50.1,17.9,190,3400,FEMALE
Chinstrap,Dream,49,19.6,212,4300,MALE
Chinstrap,Dream,51.5,18.7,187,3250,MALE
Chinstrap,Dream,49.8,17.3,198,3675,FEMALE
Chinstrap,Dream,48.1,16.4,199,3325,FEMALE
Chinstrap,Dream,51.4,19,201,3950,MALE
Chinstrap,Dream,45.7,17.3,193,3600,FEMALE
Chinstrap,Dream,50.7,19.7,203,4050,MALE
Chinstrap,Dream,42.5,17.3,187,3350,FEMALE
Chinstrap,Dream,52.2,18.8,197,3450,MALE
Chinstrap,Dream,45.2,16.6,191,3250,FEMALE
Chinstrap,Dream,49.3,19.9,203,4050,MALE
Chinstrap,Dream,50.2,18.8,202,3800,MALE
Chinstrap,Dream,45.6,19.4,194,3525,FEMALE
Chinstrap,Dream,51.9,19.5,206,3950,MALE
Chinstrap,Dream,46.8,16.5,189,3650,FEMALE
Chinstrap,Dream,45.7,17,195,3650,FEMALE
Chinstrap,Dream,55.8,19.8,207,4000,MALE
Chinstrap,Dream,43.5,18.1,202,3400,FEMALE
Chinstrap,Dream,49.6,18.2,193,3775,MALE
Chinstrap,Dream,50.8,19,210,4100,MALE
Chinstrap,Dream,50.2,18.7,198,3775,FEMALE
Gentoo,Biscoe,46.1,13.2,211,4500,FEMALE
Gentoo,Biscoe,50,16.3,230,5700,MALE
Gentoo,Biscoe,48.7,14.1,210,4450,FEMALE
Gentoo,Biscoe,50,15.2,218,5700,MALE
Gentoo,Biscoe,47.6,14.5,215,5400,MALE
Gentoo,Biscoe,46.5,13.5,210,4550,FEMALE
Gentoo,Biscoe,45.4,14.6,211,4800,FEMALE
Gentoo,Biscoe,46.7,15.3,219,5200,MALE
Gentoo,Biscoe,43.3,13.4,209,4400,FEMALE
Gentoo,Biscoe,46.8,15.4,215,5150,MALE
Gentoo,Biscoe,40.9,13.7,214,4650,FEMALE
Gentoo,Biscoe,49,16.1,216,5550,MALE
Gentoo,Biscoe,45.5,13.7,214,4650,FEMALE
Gentoo,Biscoe,48.4,14.6,213,5850,MALE
Gentoo,Biscoe,45.8,14.6,210,4200,FEMALE
Gentoo,Biscoe,49.3,15.7,217,5850,MALE
Gentoo,Biscoe,42,13.5,210,4150,FEMALE
Gentoo,Biscoe,49.2,15.2,221,6300,MALE
Gentoo,Biscoe,46.2,14.5,209,4800,FEMALE
Gentoo,Biscoe,48.7,15.1,222,5350,MALE
Gentoo,Biscoe,50.2,14.3,218,5700,MALE
Gentoo,Biscoe,45.1,14.5,215,5000,FEMALE
Gentoo,Biscoe,46.5,14.5,213,4400,FEMALE
Gentoo,Biscoe,46.3,15.8,215,5050,MALE
Gentoo,Biscoe,42.9,13.1,215,5000,FEMALE
Gentoo,Biscoe,46.1,15.1,215,5100,MALE
Gentoo,Biscoe,44.5,14.3,216,4100,
Gentoo,Biscoe,47.8,15,215,5650,MALE
Gentoo,Biscoe,48.2,14.3,210,4600,FEMALE
Gentoo,Biscoe,50,15.3,220,5550,MALE
Gentoo,Biscoe,47.3,15.3,222,5250,MALE
Gentoo,Biscoe,42.8,14.2,209,4700,FEMALE
Gentoo,Biscoe,45.1,14.5,207,5050,FEMALE
Gentoo,Biscoe,59.6,17,230,6050,MALE
Gentoo,Biscoe,49.1,14.8,220,5150,FEMALE
Gentoo,Biscoe,48.4,16.3,220,5400,MALE
Gentoo,Biscoe,42.6,13.7,213,4950,FEMALE
Gentoo,Biscoe,44.4,17.3,219,5250,MALE
Gentoo,Biscoe,44,13.6,208,4350,FEMALE
Gentoo,Biscoe,48.7,15.7,208,5350,MALE
Gentoo,Biscoe,42.7,13.7,208,3950,FEMALE
Gentoo,Biscoe,49.6,16,225,5700,MALE
Gentoo,Biscoe,45.3,13.7,210,4300,FEMALE
Gentoo,Biscoe,49.6,15,216,4750,MALE
Gentoo,Biscoe,50.5,15.9,222,5550,MALE
Gentoo,Biscoe,43.6,13.9,217,4900,FEMALE
Gentoo,Biscoe,45.5,13.9,210,4200,FEMALE
Gentoo,Biscoe,50.5,15.9,225,5400,MALE
Gentoo,Biscoe,44.9,13.3,213,5100,FEMALE
Gentoo,Biscoe,45.2,15.8,215,5300,MALE
Gentoo,Biscoe,46.6,14.2,210,4850,FEMALE
Gentoo,Biscoe,48.5,14.1,220,5300,MALE
Gentoo,Biscoe,45.1,14.4,210,4400,FEMALE
Gentoo,Biscoe,50.1,15,225,5000,MALE
Gentoo,Biscoe,46.5,14.4,217,4900,FEMALE
Gentoo,Biscoe,45,15.4,220,5050,MALE
Gentoo,Biscoe,43.8,13.9,208,4300,FEMALE
Gentoo,Biscoe,45.5,15,220,5000,MALE
Gentoo,Biscoe,43.2,14.5,208,4450,FEMALE
Gentoo,Biscoe,50.4,15.3,224,5550,MALE
Gentoo,Biscoe,45.3,13.8,208,4200,FEMALE
Gentoo,Biscoe,46.2,14.9,221,5300,MALE
Gentoo,Biscoe,45.7,13.9,214,4400,FEMALE
Gentoo,Biscoe,54.3,15.7,231,5650,MALE
Gentoo,Biscoe,45.8,14.2,219,4700,FEMALE
Gentoo,Biscoe,49.8,16.8,230,5700,MALE
Gentoo,Biscoe,46.2,14.4,214,4650,
Gentoo,Biscoe,49.5,16.2,229,5800,MALE
Gentoo,Biscoe,43.5,14.2,220,4700,FEMALE
Gentoo,Biscoe,50.7,15,223,5550,MALE
Gentoo,Biscoe,47.7,15,216,4750,FEMALE
Gentoo,Biscoe,46.4,15.6,221,5000,MALE
Gentoo,Biscoe,48.2,15.6,221,5100,MALE
Gentoo,Biscoe,46.5,14.8,217,5200,FEMALE
Gentoo,Biscoe,46.4,15,216,4700,FEMALE
Gentoo,Biscoe,48.6,16,230,5800,MALE
Gentoo,Biscoe,47.5,14.2,209,4600,FEMALE
Gentoo,Biscoe,51.1,16.3,220,6000,MALE
Gentoo,Biscoe,45.2,13.8,215,4750,FEMALE
Gentoo,Biscoe,45.2,16.4,223,5950,MALE
Gentoo,Biscoe,49.1,14.5,212,4625,FEMALE
Gentoo,Biscoe,52.5,15.6,221,5450,MALE
Gentoo,Biscoe,47.4,14.6,212,4725,FEMALE
Gentoo,Biscoe,50,15.9,224,5350,MALE
Gentoo,Biscoe,44.9,13.8,212,4750,FEMALE
Gentoo,Biscoe,50.8,17.3,228,5600,MALE
Gentoo,Biscoe,43.4,14.4,218,4600,FEMALE
Gentoo,Biscoe,51.3,14.2,218,5300,MALE
Gentoo,Biscoe,47.5,14,212,4875,FEMALE
Gentoo,Biscoe,52.1,17,230,5550,MALE
Gentoo,Biscoe,47.5,15,218,4950,FEMALE
Gentoo,Biscoe,52.2,17.1,228,5400,MALE
Gentoo,Biscoe,45.5,14.5,212,4750,FEMALE
Gentoo,Biscoe,49.5,16.1,224,5650,MALE
Gentoo,Biscoe,44.5,14.7,214,4850,FEMALE
Gentoo,Biscoe,50.8,15.7,226,5200,MALE
Gentoo,Biscoe,49.4,15.8,216,4925,MALE
Gentoo,Biscoe,46.9,14.6,222,4875,FEMALE
Gentoo,Biscoe,48.4,14.4,203,4625,FEMALE
Gentoo,Biscoe,51.1,16.5,225,5250,MALE
Gentoo,Biscoe,48.5,15,219,4850,FEMALE
Gentoo,Biscoe,55.9,17,228,5600,MALE
Gentoo,Biscoe,47.2,15.5,215,4975,FEMALE
Gentoo,Biscoe,49.1,15,228,5500,MALE
Gentoo,Biscoe,47.3,13.8,216,4725,
Gentoo,Biscoe,46.8,16.1,215,5500,MALE
Gentoo,Biscoe,41.7,14.7,210,4700,FEMALE
Gentoo,Biscoe,53.4,15.8,219,5500,MALE
Gentoo,Biscoe,43.3,14,208,4575,FEMALE
Gentoo,Biscoe,48.1,15.1,209,5500,MALE
Gentoo,Biscoe,50.5,15.2,216,5000,FEMALE
Gentoo,Biscoe,49.8,15.9,229,5950,MALE
Gentoo,Biscoe,43.5,15.2,213,4650,FEMALE
Gentoo,Biscoe,51.5,16.3,230,5500,MALE
Gentoo,Biscoe,46.2,14.1,217,4375,FEMALE
Gentoo,Biscoe,55.1,16,230,5850,MALE
Gentoo,Biscoe,44.5,15.7,217,4875,
Gentoo,Biscoe,48.8,16.2,222,6000,MALE
Gentoo,Biscoe,47.2,13.7,214,4925,FEMALE
Gentoo,Biscoe,,,,,
Gentoo,Biscoe,46.8,14.3,215,4850,FEMALE
Gentoo,Biscoe,50.4,15.7,222,5750,MALE
Gentoo,Biscoe,45.2,14.8,212,5200,FEMALE
Gentoo,Biscoe,49.9,16.1,213,5400,MALE"""

# ---------- language ----------
lang = st.sidebar.radio("Language / Язык", ["English", "Русский"], horizontal=True)
def T(en, ru):
    return ru if lang == "Русский" else en

@st.cache_data
def load():
    df = pd.read_csv(io.StringIO(CSV))
    return df.dropna(subset=["body_mass_g", "sex"]).reset_index(drop=True)

df = load()
COL = {"Adelie": "#e07b39", "Chinstrap": "#6a4c93", "Gentoo": "#2a9d8f"}

# ---------- statistics ----------
def ci_mean(x, conf, method="t", sigma=None):
    n, m, s = len(x), x.mean(), x.std(ddof=1)
    a = 1 - conf
    if method == "z (σ known)":
        crit, se = stats.norm.ppf(1 - a / 2), sigma / np.sqrt(n)
    elif method == "z (σ ≈ s)":
        crit, se = stats.norm.ppf(1 - a / 2), s / np.sqrt(n)
    else:
        crit, se = stats.t.ppf(1 - a / 2, n - 1), s / np.sqrt(n)
    return dict(n=n, mean=m, s=s, se=se, crit=crit, lo=m - crit * se, hi=m + crit * se)

def ci_var(x, conf):
    n, s2, a = len(x), x.var(ddof=1), 1 - conf
    c_hi, c_lo = stats.chi2.ppf(1 - a / 2, n - 1), stats.chi2.ppf(a / 2, n - 1)
    return dict(n=n, s2=s2, c_hi=c_hi, c_lo=c_lo, lo=(n - 1) * s2 / c_hi, hi=(n - 1) * s2 / c_lo)

def subset(species, sex):
    d = df if species == "All" else df[df.species == species]
    if sex != "All":
        d = d[d.sex == sex.upper()]
    return d.body_mass_g.values

def pick(key):
    c1, c2 = st.columns(2)
    sp = c1.selectbox(T("Species", "Вид"), ["Adelie", "Chinstrap", "Gentoo", "All"], key=key + "sp")
    sx = c2.selectbox(T("Sex", "Пол"), ["All", "Female", "Male"], key=key + "sx")
    return sp, sx

# ---------- pages ----------
pages = [T("Home", "Главная"), T("1. Data & normality", "1. Данные и нормальность"),
         T("2. CI for the mean", "2. ДИ для среднего"), T("3. CI for variance / σ", "3. ДИ для дисперсии / σ"),
         T("4. Two groups & proportion", "4. Две группы и доля"), T("5. Simulation", "5. Симуляция"),
         T("6. Sample size", "6. Объём выборки")]
page = st.sidebar.radio(T("Section", "Раздел"), pages)
st.sidebar.caption(T("Narxoz University · MATH 2001", "Университет Нархоз · MATH 2001"))

if page == pages[0]:
    st.title("🐧 " + T("Confidence intervals for penguin body mass", "Доверительные интервалы для массы пингвинов"))
    st.write(T(
        "An interactive project for the course *Theory of Probability and Mathematical Statistics* (Week 15: confidence intervals for the parameters of a normal distribution).",
        "Интерактивный проект по курсу «Теория вероятностей и математическая статистика» (неделя 15: доверительные интервалы для параметров нормального распределения)."))
    c = st.columns(4)
    c[0].metric(T("Observations", "Наблюдений"), len(df))
    c[1].metric(T("Species", "Видов"), 3)
    c[2].metric(T("Mean mass, g", "Средняя масса, г"), f"{df.body_mass_g.mean():,.0f}")
    c[3].metric(T("Std. dev., g", "Ст. откл., г"), f"{df.body_mass_g.std():,.0f}")
    st.markdown(T(
        """**Data.** Palmer Penguins (Gorman, Williams & Fraser, 2014; Horst, Hill & Gorman, 2020): 344 birds from the Palmer Archipelago, Antarctica. Rows with missing body mass or sex were removed, leaving **333**.

**Sections**
1. Data and a check of the normality assumption (histogram, Q–Q plot, Shapiro–Wilk).
2. Confidence interval for the mean: t or z, any confidence level.
3. Confidence interval for the variance and standard deviation (chi-square).
4. Difference of two means (Welch) and a proportion (Wald and Wilson).
5. Simulation: how often does a 95% interval really contain the true mean?
6. How large a sample is needed for a given margin of error?""",
        """**Данные.** Palmer Penguins (Gorman, Williams & Fraser, 2014; Horst, Hill & Gorman, 2020): 344 пингвина с архипелага Палмер, Антарктика. Строки без массы или пола удалены, осталось **333**.

**Разделы**
1. Данные и проверка нормальности (гистограмма, Q–Q график, тест Шапиро–Уилка).
2. Доверительный интервал для среднего: t или z, любой уровень доверия.
3. Доверительный интервал для дисперсии и стандартного отклонения (хи-квадрат).
4. Разность двух средних (Уэлч) и доля (Вальд и Уилсон).
5. Симуляция: как часто 95% интервал действительно накрывает истинное среднее?
6. Какой нужен объём выборки при заданной погрешности?"""))

elif page == pages[1]:
    st.header(T("Data and normality", "Данные и нормальность"))
    sp, sx = pick("d")
    x = subset(sp, sx)
    c = st.columns(5)
    for col, (lab, v) in zip(c, [("n", len(x)), (T("Mean", "Среднее"), x.mean()), (T("Median", "Медиана"), np.median(x)),
                                 (T("Std. dev.", "Ст. откл."), x.std(ddof=1)), ("min–max", None)]):
        col.metric(lab, f"{x.min():,.0f}–{x.max():,.0f}" if v is None else (f"{v:,.0f}" if lab != "n" else v))
    W, p = stats.shapiro(x)
    st.write(T(f"**Shapiro–Wilk:** W = {W:.3f}, p = {p:.4f}. ", f"**Шапиро–Уилк:** W = {W:.3f}, p = {p:.4f}. ")
             + (T("Normality is rejected at 5%.", "Нормальность отвергается на уровне 5%.") if p < .05 else
                T("No evidence against normality.", "Нет оснований отвергнуть нормальность.")))
    if sp == "All":
        st.warning(T("All species together are a mixture (two bumps), so the sample is not normal. Analyse species separately.",
                     "Все виды вместе образуют смесь (два горба), выборка не нормальна. Анализируйте виды отдельно."))
    a, b = st.columns(2)
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    ax.hist(x, bins=18, color=COL.get(sp, "#7a9cc6"), edgecolor="white"); ax.set_xlabel(T("Body mass, g", "Масса, г"))
    a.pyplot(fig)
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    stats.probplot(x, plot=ax); ax.get_lines()[0].set_markersize(3); ax.set_title("Q–Q")
    b.pyplot(fig)
    with st.expander(T("Show data table", "Показать таблицу данных")):
        st.dataframe(df, use_container_width=True)

elif page == pages[2]:
    st.header(T("Confidence interval for the mean", "Доверительный интервал для среднего"))
    sp, sx = pick("m")
    x = subset(sp, sx)
    c1, c2 = st.columns(2)
    conf = c1.slider(T("Confidence level", "Уровень доверия"), 0.80, 0.99, 0.95, 0.01)
    method = c2.radio(T("Method", "Метод"), ["t", "z (σ ≈ s)", "z (σ known)"], horizontal=True)
    sigma = None
    if method == "z (σ known)":
        sigma = st.number_input(T("Known σ, g", "Известная σ, г"), 50.0, 2000.0, float(round(x.std(ddof=1))), 10.0)
    r = ci_mean(x, conf, method, sigma)
    st.latex(r"\bar x \pm " + ("t_{\\alpha/2,\\,n-1}" if method == "t" else "z_{\\alpha/2}") +
             r"\cdot \dfrac{" + ("s" if sigma is None else r"\sigma") + r"}{\sqrt n}")
    st.write(f"n = {r['n']},  x̄ = {r['mean']:.1f} g,  s = {r['s']:.1f} g,  SE = {r['se']:.2f},  "
             f"{T('critical value','крит. значение')} = {r['crit']:.3f},  {T('margin','погрешность')} = {r['crit']*r['se']:.1f} g")
    st.success(T(f"{conf:.0%} confidence interval for the mean: **[{r['lo']:.1f}; {r['hi']:.1f}] g** (width {r['hi']-r['lo']:.1f} g)",
                 f"{conf:.0%} доверительный интервал для среднего: **[{r['lo']:.1f}; {r['hi']:.1f}] г** (ширина {r['hi']-r['lo']:.1f} г)"))
    fig, ax = plt.subplots(figsize=(7, 2.6))
    ax.hist(x, bins=18, color="#c9d6e6", edgecolor="white")
    ax.axvspan(r["lo"], r["hi"], color="#d62828", alpha=.35, label=T("confidence interval", "доверит. интервал"))
    ax.axvline(r["mean"], color="k", lw=1); ax.legend(frameon=False); ax.set_xlabel(T("Body mass, g", "Масса, г"))
    st.pyplot(fig)
    st.caption(T("The interval is for the mean, so it is much narrower than the spread of the data.",
                 "Интервал относится к среднему, поэтому он намного уже разброса данных."))
    st.subheader(T("All species at a glance", "Все виды на одном графике"))
    fig, ax = plt.subplots(figsize=(7, 2.4))
    for i, s in enumerate(["Adelie", "Chinstrap", "Gentoo"]):
        q = ci_mean(df[df.species == s].body_mass_g.values, conf, "t")
        ax.errorbar(q["mean"], i, xerr=q["crit"] * q["se"], fmt="o", color=COL[s], capsize=5)
    ax.set_yticks(range(3)); ax.set_yticklabels(["Adelie", "Chinstrap", "Gentoo"]); ax.invert_yaxis()
    ax.set_xlabel(T(f"Mean body mass with {conf:.0%} t-interval, g", f"Средняя масса с {conf:.0%} t-интервалом, г"))
    st.pyplot(fig)

elif page == pages[3]:
    st.header(T("Confidence interval for variance and σ", "Доверительный интервал для дисперсии и σ"))
    sp, sx = pick("v")
    x = subset(sp, sx)
    conf = st.slider(T("Confidence level", "Уровень доверия"), 0.80, 0.99, 0.95, 0.01, key="vc")
    r = ci_var(x, conf)
    st.latex(r"\left[\dfrac{(n-1)s^2}{\chi^2_{\alpha/2,\,n-1}},\ \dfrac{(n-1)s^2}{\chi^2_{1-\alpha/2,\,n-1}}\right]")
    st.write(f"n = {r['n']},  s² = {r['s2']:,.0f},  χ²(upper) = {r['c_hi']:.2f},  χ²(lower) = {r['c_lo']:.2f}")
    st.success(T(f"Variance: **[{r['lo']:,.0f}; {r['hi']:,.0f}]**   ·   σ: **[{np.sqrt(r['lo']):.1f}; {np.sqrt(r['hi']):.1f}] g**",
                 f"Дисперсия: **[{r['lo']:,.0f}; {r['hi']:,.0f}]**   ·   σ: **[{np.sqrt(r['lo']):.1f}; {np.sqrt(r['hi']):.1f}] г**"))
    st.caption(T("The interval is not symmetric around s² and it is sensitive to non-normality; check the Q–Q plot first.",
                 "Интервал несимметричен относительно s² и чувствителен к ненормальности; сначала проверьте Q–Q график."))
    k = r["n"] - 1
    g = np.linspace(stats.chi2.ppf(.0005, k), stats.chi2.ppf(.9995, k), 400)
    fig, ax = plt.subplots(figsize=(7, 2.6))
    ax.plot(g, stats.chi2.pdf(g, k), color="k")
    ax.fill_between(g, stats.chi2.pdf(g, k), where=(g >= r["c_lo"]) & (g <= r["c_hi"]), color="#2a9d8f", alpha=.4)
    ax.set_title(T(f"Chi-square, {k} degrees of freedom: middle {conf:.0%} shaded", f"Хи-квадрат, {k} ст. свободы: закрашены средние {conf:.0%}"))
    st.pyplot(fig)

elif page == pages[4]:
    st.header(T("Two groups and a proportion", "Две группы и доля"))
    st.subheader(T("Difference of means, male − female (Welch)", "Разность средних, самцы − самки (Уэлч)"))
    c1, c2 = st.columns(2)
    sp = c1.selectbox(T("Species", "Вид"), ["Adelie", "Chinstrap", "Gentoo", "All"], key="ts")
    conf = c2.slider(T("Confidence level", "Уровень доверия"), 0.80, 0.99, 0.95, 0.01, key="tc")
    m, f = subset(sp, "Male"), subset(sp, "Female")
    va, vb = m.var(ddof=1) / len(m), f.var(ddof=1) / len(f)
    se = np.sqrt(va + vb); nu = (va + vb) ** 2 / (va ** 2 / (len(m) - 1) + vb ** 2 / (len(f) - 1))
    t = stats.t.ppf(1 - (1 - conf) / 2, nu); d = m.mean() - f.mean()
    p = stats.ttest_ind(m, f, equal_var=False).pvalue
    st.write(f"{T('Males','Самцы')}: n = {len(m)}, x̄ = {m.mean():.1f};  {T('females','самки')}: n = {len(f)}, x̄ = {f.mean():.1f};  ν = {nu:.1f}")
    st.success(T(f"Difference = {d:.1f} g, {conf:.0%} CI **[{d-t*se:.1f}; {d+t*se:.1f}] g**. ", f"Разность = {d:.1f} г, {conf:.0%} ДИ **[{d-t*se:.1f}; {d+t*se:.1f}] г**. ")
                 + (T("Zero is outside the interval: the means differ.", "Ноль вне интервала: средние различаются.") if not (d - t * se <= 0 <= d + t * se)
                    else T("Zero is inside the interval: no clear difference.", "Ноль внутри интервала: явной разницы нет.")) + f"  (Welch p = {p:.2g})")
    st.subheader(T("Proportion", "Доля"))
    c1, c2 = st.columns(2)
    what = c1.selectbox(T("Count the share of", "Считать долю"), [T("males", "самцов"), "Adelie", "Chinstrap", "Gentoo"])
    conf2 = c2.slider(T("Confidence level", "Уровень доверия"), 0.80, 0.99, 0.95, 0.01, key="pc")
    k = int((df.sex == "MALE").sum()) if what in ("males", "самцов") else int((df.species == what).sum())
    n = len(df); ph = k / n; z = stats.norm.ppf(1 - (1 - conf2) / 2)
    w = (ph - z * np.sqrt(ph * (1 - ph) / n), ph + z * np.sqrt(ph * (1 - ph) / n))
    cen = (ph + z * z / (2 * n)) / (1 + z * z / n); hw = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    st.write(f"k = {k}, n = {n}, p̂ = {ph:.3f}")
    st.table(pd.DataFrame({T("Method", "Метод"): ["Wald", "Wilson"], T("Lower", "Нижняя"): [w[0], cen - hw], T("Upper", "Верхняя"): [w[1], cen + hw]}).round(3))

elif page == pages[5]:
    st.header(T("What does 95% confidence mean?", "Что значит 95% доверия?"))
    st.write(T("The 119 Gentoo penguins are treated as a small population with a known mean. We draw many samples, build an interval from each, and count how often it contains the true mean.",
               "119 пингвинов Gentoo считаются небольшой генеральной совокупностью с известным средним. Берём много выборок, строим интервал по каждой и считаем, как часто он накрывает истинное среднее."))
    pop = df[df.species == "Gentoo"].body_mass_g.values; mu = pop.mean()
    c1, c2, c3, c4 = st.columns(4)
    n = c1.slider(T("Sample size n", "Объём выборки n"), 3, 100, 10)
    conf = c2.slider(T("Level", "Уровень"), 0.80, 0.99, 0.95, 0.01, key="sc")
    meth = c3.radio(T("Method", "Метод"), ["t", "z (σ ≈ s)"], key="sm")
    N = c4.select_slider(T("Repetitions", "Повторений"), [1000, 5000, 10000], 5000)
    seed = st.number_input("Seed", 0, 99999, 2026)
    rng = np.random.default_rng(int(seed))
    S = rng.choice(pop, (N, n)); m = S.mean(1); s = S.std(1, ddof=1)
    crit = stats.t.ppf(1 - (1 - conf) / 2, n - 1) if meth == "t" else stats.norm.ppf(1 - (1 - conf) / 2)
    h = crit * s / np.sqrt(n); ok = np.abs(m - mu) <= h
    st.metric(T("Observed coverage", "Наблюдаемое покрытие"), f"{ok.mean():.1%}", delta=f"{(ok.mean()-conf)*100:+.1f} pp {T('vs nominal','от номинала')}")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for i in range(40):
        ax.plot([m[i] - h[i], m[i] + h[i]], [i, i], color="#2a9d8f" if ok[i] else "#d62828", lw=1.6)
    ax.axvline(mu, color="k", ls="--", lw=1); ax.invert_yaxis(); ax.set_xlabel(T("Body mass, g", "Масса, г"))
    ax.set_title(T("First 40 intervals (red = missed the true mean)", "Первые 40 интервалов (красные не накрыли среднее)"))
    st.pyplot(fig)
    st.caption(T("Try n = 5 with the z method: coverage falls well below 95%, while the t method stays close.",
                 "Попробуйте n = 5 с методом z: покрытие падает заметно ниже 95%, а метод t остаётся близким к номиналу."))

else:
    st.header(T("Sample size calculator", "Калькулятор объёма выборки"))
    st.latex(r"n \ge \left(\dfrac{z_{\alpha/2}\,\sigma}{E}\right)^2")
    c1, c2, c3 = st.columns(3)
    sp = c1.selectbox(T("Planning σ from species", "σ по виду"), ["Adelie", "Chinstrap", "Gentoo"])
    conf = c2.slider(T("Confidence level", "Уровень доверия"), 0.80, 0.99, 0.95, 0.01, key="nc")
    E = c3.slider(T("Margin of error E, g", "Погрешность E, г"), 10, 200, 50, 5)
    s = df[df.species == sp].body_mass_g.std(ddof=1); z = stats.norm.ppf(1 - (1 - conf) / 2)
    need = int(np.ceil((z * s / E) ** 2))
    st.metric(T("Required n", "Нужное n"), need)
    st.write(f"σ ≈ {s:.1f} g,  z = {z:.3f}")
    Es = np.arange(10, 201, 5); ns = np.ceil((z * s / Es) ** 2)
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(Es, ns, color="#2a6f97"); ax.scatter([E], [need], color="#d62828", zorder=3)
    ax.set_xlabel(T("Margin of error E, g", "Погрешность E, г")); ax.set_ylabel("n"); ax.set_yscale("log")
    st.pyplot(fig)
    st.caption(T("Halving the margin of error needs four times as many observations.", "Чтобы уменьшить погрешность вдвое, нужно в четыре раза больше наблюдений."))
