# Sensitivity, Specificity & Prevalence — Interactive Dot Plot

An interactive Streamlit app for teaching diagnostic test concepts in public health and epidemiology courses.

## What it does

- Displays a population of **200 people** as colored dots
- Sliders let students adjust **prevalence**, **sensitivity**, and **specificity** in real time
- Dots update instantly to show true positives, false positives, true negatives, and false negatives
- Calculates and displays **PPV** (positive predictive value) and **NPV**
- Provides automatic interpretation of results (e.g. low-prevalence false-positive trap)

## Color key

| Color | Meaning |
|-------|---------|
| 🟠 Orange (ringed) | False positive — no disease, but tested positive |
| 🔴 Red (ringed) | True positive — has disease, tested positive |
| ⚫ Dark gray | False negative — has disease, missed by test |
| 🩶 Light gray | True negative — no disease, correctly negative |

> Ringed dots = everyone who received a positive test result.

## Deploy to Streamlit Community Cloud

1. Fork or push this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New app** → select your repo → set main file to `app.py`
4. Click **Deploy**

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Learning objectives supported

- Understand why low prevalence leads to high false-positive rates
- Visualize the SnNout / SpPin mnemonics
- Explore how PPV and NPV change with population characteristics
- Connect 2×2 table counts to real population proportions
