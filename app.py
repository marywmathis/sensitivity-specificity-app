import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sensitivity, Specificity & Prevalence",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Sensitivity, Specificity & Prevalence")

left, right = st.columns([1, 2])

with left:
    st.markdown("**Adjust the test parameters**")
    prevalence = st.slider("Prevalence (%)", 1, 50, 5, 1,
        help="How common the disease is in this population.")
    sensitivity = st.slider("Sensitivity (%)", 50, 100, 90, 1,
        help="How well the test catches people who DO have the disease.")
    specificity = st.slider("Specificity (%)", 50, 100, 70, 1,
        help="How well the test avoids false alarms in healthy people.")

    st.divider()
    st.markdown("**Color key** — ringed dots tested positive")
    st.markdown(
        """
        <div style='font-size:13px;line-height:2.2'>
        <span style='color:#D85A30;font-size:18px'>●</span> True positive — has disease, test +<br>
        <span style='color:#EF9F27;font-size:18px'>●</span> False positive — no disease, test +<br>
        <span style='color:#5F5E5A;font-size:18px'>●</span> False negative — has disease, test −<br>
        <span style='color:#B4B2A9;font-size:18px'>●</span> True negative — no disease, test −
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown(
        "<div style='font-size:12px;color:#888;line-height:1.9'>"
        "🔵 High sensitivity → negative = trustworthy <em>(rules OUT)</em><br>"
        "🟢 High specificity → positive = trustworthy <em>(rules IN)</em><br>"
        "📉 Low prevalence + low specificity → many false positives"
        "</div>",
        unsafe_allow_html=True
    )

# Generate population
N = 200
COLS = 20
ROWS = N // COLS

rng = np.random.default_rng(42)
n_sick = round(N * prevalence / 100)
sick = np.array([True] * n_sick + [False] * (N - n_sick))

test_pos = np.where(
    sick,
    rng.random(N) < sensitivity / 100,
    rng.random(N) >= specificity / 100
)

categories = np.where(
    sick & test_pos, "TP",
    np.where(~sick & test_pos, "FP",
    np.where(sick & ~test_pos, "FN", "TN"))
)

order_map = {"TP": 0, "FP": 1, "FN": 2, "TN": 3}
sort_idx = np.argsort([order_map[c] for c in categories])
categories_sorted = categories[sort_idx]
test_pos_sorted = test_pos[sort_idx]

tp = int(np.sum(categories == "TP"))
fp = int(np.sum(categories == "FP"))
tn = int(np.sum(categories == "TN"))
fn = int(np.sum(categories == "FN"))
total_pos = tp + fp
ppv = round(tp / total_pos * 100) if total_pos > 0 else 0
npv_denom = tn + fn
npv = round(tn / npv_denom * 100) if npv_denom > 0 else 0

COLOR_MAP = {"TP": "#D85A30", "FP": "#EF9F27", "TN": "#B4B2A9", "FN": "#5F5E5A"}
ALPHA_MAP = {"TP": 1.0,       "FP": 1.0,       "TN": 0.45,      "FN": 0.7}

with right:
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("True +",  tp)
    m2.metric("False +", fp)
    m3.metric("False −", fn)
    m4.metric("PPV", f"{ppv}%", help="% of positive tests that are real disease")
    m5.metric("NPV", f"{npv}%", help="% of negative tests that are truly disease-free")

    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor("#FAFAF8")
    ax.set_facecolor("#FAFAF8")

    for i, (cat, pos) in enumerate(zip(categories_sorted, test_pos_sorted)):
        col = i % COLS
        row = i // COLS
        x = col + 0.5
        y = ROWS - row - 0.5
        circle = plt.Circle((x, y), 0.36, color=COLOR_MAP[cat], alpha=ALPHA_MAP[cat], zorder=2)
        ax.add_patch(circle)
        if pos:
            ring_color = "#993C1D" if cat == "TP" else "#854F0B"
            ring = plt.Circle((x, y), 0.44, fill=False, edgecolor=ring_color,
                               linewidth=1.6, alpha=0.9, zorder=3)
            ax.add_patch(ring)

    ax.set_xlim(0, COLS)
    ax.set_ylim(0, ROWS)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout(pad=0.3)
    st.pyplot(fig, use_container_width=True)
    plt.close()

    if ppv < 50 and total_pos > 0:
        st.warning(
            f"⚠️ Most positive results are false alarms. "
            f"Only **{ppv}%** of positive tests reflect true disease (PPV). "
            f"Classic low-prevalence false-positive trap."
        )
    elif ppv >= 80:
        st.success(
            f"✅ Positive results are fairly reliable — PPV = {ppv}%. "
            f"{tp} of {total_pos} positive tests are true positives."
        )
    else:
        st.info(f"ℹ️ PPV = {ppv}%. About {ppv}% of positive tests are true positives.")

with st.expander("📘 Concept review"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### Sensitivity")
        st.markdown(
            "Catches people who **do** have disease.  \n"
            "High sensitivity → **negative** result is trustworthy.  \n"
            "*SnNout — rules out disease.*"
        )
    with c2:
        st.markdown("#### Specificity")
        st.markdown(
            "Avoids false alarms in healthy people.  \n"
            "High specificity → **positive** result is trustworthy.  \n"
            "*SpPin — rules in disease.*"
        )
    with c3:
        st.markdown("#### Prevalence & PPV")
        st.markdown(
            "Rare disease → most positives are false alarms.  \n"
            "PPV rises with higher prevalence **or** higher specificity."
        )
