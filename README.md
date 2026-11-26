# Confidence Intervals for the Body Mass of Palmer Archipelago Penguins

Research project for **MATH 2001 Theory of Probability and Mathematical Statistics**, Narxoz University (Fall 2026).
Topic: confidence intervals for the parameters of a normal distribution (syllabus week 15).
Author: Kuanyshuly Abilmansur · Lecturer: Dr. Abdullah Almas · n = 333 observations.

**Website:** https://probablity-project.streamlit.app

**Data:** Palmer Penguins (Gorman, Williams & Fraser, 2014; Horst, Hill & Gorman, 2020), 344 birds, 333 after removing rows with missing body mass or sex. Source file: [seaborn-data](https://github.com/mwaskom/seaborn-data).

## Contents
| File | Description |
|---|---|
| `report/probablity-project.docx` | Full report: theory, assumptions check, results, simulation, conclusions, code |
| `app.py` | Interactive Streamlit website (English / Russian), data embedded in the file |
| `analysis.py` | Script that produces every number and figure in the report |
| `data/penguins.csv` | Data set |
| `report/figures/` | Figures used in the report |

## Methods
CI for the mean (t, z with known σ, z with σ ≈ s) · CI for variance and σ (chi-square) · Welch CI for a difference of means · Wald and Wilson CI for a proportion · sample size for a given margin of error · Shapiro–Wilk test and Q–Q plots · coverage simulation (10,000 repetitions) · bootstrap check.

## Run the website locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open http://localhost:8501.

## Re-run the analysis
```bash
python analysis.py
```
Run it from the repository root (it reads `data/penguins.csv`; the folder `fig/` must exist: `mkdir -p fig`).
