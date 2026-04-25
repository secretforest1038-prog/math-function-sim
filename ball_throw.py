import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Page Config
st.set_page_config(page_title="Kumgok Math: Pro", layout="centered")

# --- UI CSS ---
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; height: 70px; font-size: 1.8rem !important;
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important; border-radius: 20px !important; border: none !important;
    }
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. Learning Mode & Sidebar
st.sidebar.header("🎯 Learning Mode")
mode = st.sidebar.selectbox("Mission Type", ["Adjust 'a' (Width)", "Adjust 'b' (Axis)", "Adjust 'c' (Starting Point)"])

default_a, default_b, default_c = -1.5, 8.0, 2.0

with st.sidebar:
    st.write("---")
    if "Adjust 'a'" in mode:
        a = st.slider("a (Gravity/Width)", -5.0, -0.2, default_a, 0.1)
        b, c = default_b, default_c
    elif "Adjust 'b'" in mode:
        b = st.slider("b (Velocity/Axis)", 0.0, 20.0, default_b, 0.1)
        a, c = default_a, default_c
    else:
        c = st.slider("c (Initial Height)", 0.0, 10.0, default_c, 0.1)
        a, b = default_a, default_b

    if st.button("New Target"):
        st.session_state.tx = round(np.random.uniform(7, 15), 1)
        st.session_state.ty = round(np.random.uniform(1, 6), 1)
        st.rerun()

if 'tx' not in st.session_state:
    st.session_state.tx, st.session_state.ty = 12.0, 3.5

# 3. Math Calculations
axis_x = -b / (2*a)
vertex_y = c - b**2 / (4*a)
x_end = (-b - np.sqrt(max(0, b**2 - 4*a*c))) / (2*a)

# High-resolution trajectory
x_full = np.linspace(0, x_end, 50)
y_full = a * x_full**2 + b * x_full + c

# 4. Drawing Function
def draw_graph(step=None):
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Dynamic limits
    ax.set_xlim(-1.5, max(x_end, st.session_state.tx) + 2)
    ax.set_ylim(-0.5, max(vertex_y, st.session_state.ty) + 2)
    
    # 1. Subtle Axis of Symmetry (Faded Yellow)
    ax.axvline(x=axis_x, color='#FFD700', linestyle=':', alpha=0.3, lw=1.5)
    
    # 2. Target
    ax.add_patch(plt.Rectangle((st.session_state.tx-0.4, st.session_state.ty-0.15), 0.8, 0.3, color='#ef4444', zorder=4))
    
    # 3. Human Silhouette (More detailed)
    # Leg & Body
    ax.add_patch(plt.Polygon([[-0.2, 0], [0.2, 0], [0.1, c*0.6], [-0.1, c*0.6]], color='#334155'))
    ax.add_patch(plt.Polygon([[-0.1, c*0.6], [0.1, c*0.6], [0.2, c], [-0.2, c]], color='#334155'))
    # Arm throwing
    ax.plot([0.1, 0.5], [c*0.8, c], color='#334155', lw=4, solid_capstyle='round')
    # Head
    head = plt.Circle((0, c+0.25), 0.25, color='#334155')
    ax.add_patch(head)
    
    # 4. Trajectory & Ball
    if step is not None:
        ax.plot(x_full[:step], y_full[:step], color='#4f46e5', lw=3, alpha=0.7)
        ax.plot(x_full[step], y_full[step], 'o', color='#f59e0b', ms=14, mec='black', zorder=5)
    else:
        ax.plot(x_full, y_full, color='#4f46e5', alpha=0.1, ls='--')
        ax.plot(0, c, 'o', color='#f59e0b', ms=12, alpha=0.4)

    ax.set_axis_off() # 깔끔한 화면을 위해 축 레이블 숨김 (필요시 제거 가능)
    return fig

# 5. UI Execution
st.info(f"Target: ({st.session_state.tx}, {st.session_state.ty}) | Mode: {mode}")

plot_spot = st.empty()
plot_spot.pyplot(draw_graph())

if st.button("LAUNCH 🚀"):
    # Extremely fast redraw
    for i in range(len(x_full)):
        plot_spot.pyplot(draw_graph(step=i))
    
    # Final Judgement
    dist = np.sqrt((x_full - st.session_state.tx)**2 + (y_full - st.session_state.ty)**2)
    if np.min(dist) < 0.7:
        st.balloons()
        st.success("🎯 MISSION COMPLETE!")
    else:
        st.error("MISS!")
