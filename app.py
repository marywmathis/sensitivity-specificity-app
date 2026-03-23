import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="Sensitivity, Specificity & Prevalence",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Sensitivity, Specificity & Prevalence")
st.markdown("Each dot represents one person in a population of **200**. Ringed dots tested positive.")

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Adjust the test parameters")

    prevalence = st.slider(
        "Prevalence (%)",
        min_value=1, max_value=50, value=5, step=1,
        help="How common the disease is in this population."
    )
    sensitivity = st.slider(
        "Sensitivity (%)",
        min_value=50, max_value=100, value=90, step=1,
        help="How well the test catches people who DO have the disease."
    )
    specificity = st.slider(
        "Specificity (%)",
        min_value=50, max_value=100, value=70, step=1,
        help="How well the test avoids false alarms in healthy people."
    )

    st.divider()
    st.markdown("**Key reminders**")
    st.markdown("- 🔵 High sensitivity → negative result is trustworthy (*rules OUT*)")
    st.markdown("- 🟢 High specificity → positive result is trustworthy (*rules IN*)")
    st.markdown("- 📉 Low prevalence + low specificity → lots of false positives")

# ── Generate population ───────────────────────────────────────────────────────
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
    sick & test_pos,  "TP",
    np.where(
        ~sick & test_pos, "FP",
        np.where(
            sick & ~test_pos, "FN", "TN"
        )
    )
)

# Sort: TP first, then FP, FN, TN
order_map = {"TP": 0, "FP": 1, "FN": 2, "TN": 3}
sort_idx = np.argsort([order_map[c] for c in categories])
categories_sorted = categories[sort_idx]
test_pos_sorted = test_pos[sort_idx]

# ── Counts & metrics ──────────────────────────────────────────────────────────
tp = np.sum(categories == "TP")
fp = np.sum(categories == "FP")
tn = np.sum(categories == "TN")
fn = np.sum(categories == "FN")
total_pos = tp + fp
ppv = round(tp / total_pos * 100) if total_pos > 0 else 0
npv_denom = tn + fn
npv = round(tn / npv_denom * 100) if npv_denom > 0 else 0

# ── Metric cards ──────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("True positives", tp, help="Has disease AND tested positive")
col2.metric("False positives", fp, help="No disease but tested positive (false alarm)")
col3.metric("False negatives", fn, help="Has disease but tested negative (missed)")
col4.metric("PPV", f"{ppv}%", help="Of everyone who tested positive, this % actually has the disease")
col5.metric("NPV", f"{npv}%", help="Of everyone who tested negative, this % truly doesn't have the disease")

# ── Dot plot ──────────────────────────────────────────────────────────────────
COLOR_MAP = {
    "TP": "#D85A30",
    "FP": "#EF9F27",
    "TN": "#B4B2A9",
    "FN": "#5F5E5A",
}
ALPHA_MAP = {"TP": 1.0, "FP": 1.0, "TN": 0.45, "FN": 0.7}

fig, ax = plt.subplots(figsize=(12, 5.2))
fig.patch.set_facecolor("#FAFAF8")
ax.set_facecolor("#FAFAF8")

for i, (cat, pos) in enumerate(zip(categories_sorted, test_pos_sorted)):
    col = i % COLS
    row = i // COLS
    x = col + 0.5
    y = ROWS - row - 0.5

    color = COLOR_MAP[cat]
    alpha = ALPHA_MAP[cat]

    circle = plt.Circle((x, y), 0.36, color=color, alpha=alpha, zorder=2)
    ax.add_patch(circle)

    if pos:
        ring_color = "#993C1D" if cat == "TP" else "#854F0B"
        ring = plt.Circle((x, y), 0.44, fill=False, edgecolor=ring_color,
                           linewidth=1.8, alpha=0.9, zorder=3)
        ax.add_patch(ring)

ax.set_xlim(0, COLS)
ax.set_ylim(0, ROWS)
ax.set_aspect("equal")
ax.axis("off")

# Legend
legend_patches = [
    mpatches.Patch(color="#D85A30", label=f"True positive — has disease, test + ({tp})"),
    mpatches.Patch(color="#EF9F27", label=f"False positive — no disease, test + ({fp})"),
    mpatches.Patch(color="#5F5E5A", label=f"False negative — has disease, test − ({fn})"),
    mpatches.Patch(color="#B4B2A9", label=f"True negative — no disease, test − ({tn})"),
]
ax.legend(
    handles=legend_patches,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.18),
    ncol=2,
    fontsize=10,
    frameon=False,
)

plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── Interpretation box ────────────────────────────────────────────────────────
st.divider()

if ppv < 50 and total_pos > 0:
    st.warning(
        f"⚠️ **Most positive results are false alarms.** "
        f"With {prevalence}% prevalence and {specificity}% specificity, "
        f"only **{ppv}%** of positive tests reflect true disease (PPV = {ppv}%). "
        f"This is the classic low-prevalence trap."
    )
elif ppv >= 80:
    st.success(
        f"✅ **Positive results are fairly reliable.** "
        f"PPV = {ppv}% — most people who test positive ({tp} of {total_pos}) actually have the disease."
    )
else:
    st.info(
        f"ℹ️ PPV = {ppv}%. About {ppv}% of positive tests are true positives. "
        f"Consider the tradeoffs between sensitivity and specificity for this disease and population."
    )

# ── Concept summary ───────────────────────────────────────────────────────────
with st.expander("📘 Concept review"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### Sensitivity")
        st.markdown(
            "How well the test catches people who **do** have the disease.  \n"
            "High sensitivity → a **negative** result is trustworthy.  \n"
            "*Mnemonic: **Sn**-N-out — rules **out** disease.*"
        )
    with c2:
        st.markdown("#### Specificity")
        st.markdown(
            "How well the test avoids false alarms in healthy people.  \n"
            "High specificity → a **positive** result is trustworthy.  \n"
            "*Mnemonic: **Sp**-P-in — rules **in** disease.*"
        )
    with c3:
        st.markdown("#### Prevalence & PPV")
        st.markdown(
            "Even a sensitive test floods results with false positives when  \n"
            "the disease is rare — because most people are healthy.  \n"
            "PPV rises with higher prevalence **or** higher specificity."
        )
