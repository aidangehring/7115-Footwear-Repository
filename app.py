#%%
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os

from data_loader import load_data, get_series
from metrics import compute_summary, symmetry_index
from config import SHOES, VARIABLE_LABELS, JOINT_OPTIONS, AXIS_OPTIONS, VARIABLE_OPTIONS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Footwear Biomechanics Assessment",
    page_icon="👟",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .main { background-color: #0f0f0f; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 600;
        letter-spacing: -0.03em;
        color: #f0f0f0;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        font-size: 1rem;
        color: #888;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    .shoe-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        height: 100%;
    }
    .shoe-card h3 {
        font-size: 1rem;
        font-weight: 600;
        color: #f0f0f0;
        margin: 0.6rem 0 0.3rem 0;
    }
    .shoe-card p {
        font-size: 0.78rem;
        color: #888;
        line-height: 1.5;
        margin: 0;
    }
    .shoe-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
    }
    .section-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #666;
        font-family: 'DM Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        font-size: 1.3rem;
        font-weight: 500;
        color: #f0f0f0;
    }
    .stSelectbox label, .stRadio label { color: #aaa !important; font-size: 0.85rem; }
    div[data-testid="stPlotlyChart"] { border-radius: 12px; overflow: hidden; }
    .divider { border: none; border-top: 1px solid #222; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
data = load_data()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">Footwear Biomechanics Assessment</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">3D lower limb kinematic & kinetic analysis across three footwear conditions</p>', unsafe_allow_html=True)

# ── Shoe cards ────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Footwear Conditions</p>', unsafe_allow_html=True)
cols = st.columns(3)

for col, (shoe_key, shoe_info) in zip(cols, SHOES.items()):
    with col:
        image_path = shoe_info.get('image', '')
        img_html = ''
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)

        st.markdown(f"""
        <div class="shoe-card">
            <h3>
                <span class="shoe-dot" style="background:{shoe_info['color']}"></span>
                {shoe_info['name']}
            </h3>
            <p>{shoe_info['description']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Analysis Controls</p>', unsafe_allow_html=True)
variable_key = st.radio("Variable", list(VARIABLE_OPTIONS.keys()),
                        format_func=lambda k: VARIABLE_OPTIONS[k],
                        horizontal=True)
ctrl1, ctrl2, ctrl3 = st.columns(3)

with ctrl1:
    if variable_key == 'grf':
        side = st.radio("Side", ['Left', 'Right'], horizontal=True)
        joint = side  # e.g. 'Left' or 'Right'
    else:
        joint = st.selectbox("Joint", JOINT_OPTIONS)
with ctrl2:
    axis = st.radio("Axis", AXIS_OPTIONS, horizontal=True)


y_label = VARIABLE_LABELS[variable_key]

# ── Waveform plot ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-label" style="margin-top:1.5rem">Ensemble Waveform — Mean ± 1 SD</p>', unsafe_allow_html=True)

fig = go.Figure()

for shoe_key, shoe_info in SHOES.items():
    mean = get_series(data, variable_key, shoe_key, joint, axis, stat='Mean')
    sd   = get_series(data, variable_key, shoe_key, joint, axis, stat='Std Dev')

    if mean is None:
        continue

    x = list(mean.index)
    color = shoe_info['color']

    # SD band
    if sd is not None:
        fig.add_trace(go.Scatter(
            x=x + x[::-1],
            y=list(mean + sd) + list((mean - sd).iloc[::-1]),
            fill='toself',
            fillcolor=color,
            opacity=0.12,
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Mean line
    fig.add_trace(go.Scatter(
        x=x,
        y=mean,
        name=shoe_info['name'],
        line=dict(color=color, width=2.5),
        hovertemplate=f"<b>{shoe_info['name']}</b><br>%{{x}}% GC<br>%{{y:.2f}}<extra></extra>"
    ))

fig.update_layout(
    paper_bgcolor='#141414',
    plot_bgcolor='#141414',
    font=dict(family='DM Sans', color='#aaa', size=12),
    xaxis=dict(
        title='Gait Cycle (%)',
        gridcolor='#222',
        zeroline=False,
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        title=y_label,
        gridcolor='#222',
        zeroline=True,
        zerolinecolor='#333',
        zerolinewidth=1,
        tickfont=dict(size=11)
    ),
    legend=dict(
        bgcolor='#1a1a1a',
        bordercolor='#2a2a2a',
        borderwidth=1,
        font=dict(size=12, color='#f0f0f0')
    ),
    margin=dict(l=60, r=20, t=20, b=60),
    height=420,
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True, key=f"{joint}_{variable_key}_{axis}")

# ── Advanced metrics (collapsible) ────────────────────────────────────────────
with st.expander("Advanced Metrics", expanded=False):
    st.markdown('<p class="section-label">Peak Values & Range of Motion</p>', unsafe_allow_html=True)

    summary_rows = []
    for shoe_key, shoe_info in SHOES.items():
        metrics = compute_summary(data, variable_key, shoe_key, joint, axis)
        if metrics:
            metrics['Shoe'] = shoe_info['name']
            summary_rows.append(metrics)

    if summary_rows:
        df_summary = pd.DataFrame(summary_rows).set_index('Shoe')
        st.dataframe(
            df_summary.style.format("{:.2f}", na_rep="—")
                            .background_gradient(cmap='RdYlGn', axis=0),
            use_container_width=True
        )

    # Symmetry index for left/right if applicable
    if 'Left' in joint:
        right_joint = joint.replace('Left', 'Right')
        st.markdown('<p class="section-label" style="margin-top:1.5rem">Bilateral Symmetry Index</p>', unsafe_allow_html=True)
        sym_cols = st.columns(3)
        for col, (shoe_key, shoe_info) in zip(sym_cols, SHOES.items()):
            left_s  = get_series(data, variable_key, shoe_key, joint, axis)
            right_s = get_series(data, variable_key, shoe_key, right_joint, axis)
            si = symmetry_index(left_s, right_s)
            with col:
                si_color = "#4ade80" if si and si < 10 else "#facc15" if si and si < 20 else "#f87171"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{shoe_info['name']}</div>
                    <div class="metric-value" style="color:{si_color}">{si}%</div>
                    <div class="metric-label">Symmetry Index</div>
                </div>
                """, unsafe_allow_html=True)

# %%

# %%
