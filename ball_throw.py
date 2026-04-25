import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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
    .mission-status { background: #f8fafc; padding: 15px; border-radius: 15px; border: 2px solid #e2e8f0; text-align: center; font-weight: bold; font-size: 1.2rem; }
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
    st.session_state.tx, st.session_state.ty = 11.0, 3.5

# 3. Math Calculations
# Vertex (Axis of Symmetry)
axis_x = -b / (2*a)
vertex_y = c - b**2 / (4*a)

# End point (Ground)
discriminant = max(0, b**2 - 4*a*c)
x_end = (-b - np.sqrt(discriminant)) / (2*a)

# High-resolution trajectory for smoothness
x_full = np.linspace(0, x_end, 60)
y_full = a * x_full**2 + b * x_full + c

# 4. Fast Drawing Function
def draw_graph(step=None):
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Set dynamic limits
    ax.set_xlim(-1.5, max(x_end, st.session_state.tx) + 2)
    ax.set_ylim(-0.5, max(vertex_y, st.session_state.ty) + 2)
    
    # 1. Axis of Symmetry (Yellow Dashed Line)
    ax.axvline(x=axis_x, color='#FFD700', linestyle='--', alpha=0.8, lw=2, label='Axis')
    
    # 2. Target
    ax.add_patch(plt.Rectangle((st.session_state.tx-0.4, st.session_state.ty-0.15), 0.8, 0.3, color='#ef4444', zorder=4))
    
    # 3. Human Silhouette (Simple representation)
    ax.plot([0, 0], [0, c], color='black', lw=4) # Body
    ax.plot([-0.3, 0.3], [c-0.8, c], color='black', lw=3) # Arm throwing
    ax.plot(0, c+0.3, 'o', color='black', ms=10) # Head
    
    # 4. Trajectory & Ball
    if step is not None:
        ax.plot(x_full[:step], y_full[:step], color='#4f46e5', lw=3, alpha=0.7)
        ax.plot(x_full[step], y_full[step], 'o', color='#f59e0b', ms=14, mec='black', zorder=5)
    else:
        # Static Guide Line
        ax.plot(x_full, y_full, color='#4f46e5', alpha=0.15, ls='--')
        ax.plot(0, c, 'o', color='#f59e0b', ms=12, alpha=0.5)

    ax.set_xlabel("Distance (x)")
    ax.set_ylabel("Height (y)")
    ax.grid(True, alpha=0.2)
    return fig

# 5. Execution UI
st.markdown(f"<div class='mission-status'>{mode} | Target: ({st.session_state.tx}, {st.session_state.ty})</div>", unsafe_allow_html=True)

plot_spot = st.empty()
plot_spot.pyplot(draw_graph())

if st.button("LAUNCH 🚀"):
    # Faster animation with fewer redraws of heavy elements
    for i in range(len(x_full)):
        plot_spot.pyplot(draw_graph(step=i))
    
    # Result Feedback
    dist = np.sqrt((x_full - st.session_state.tx)**2 + (y_full - st.session_state.ty)**2)
    if np.min(dist) < 0.7:
        st.balloons()
        st.success("🎯 MISSION COMPLETE!")
        if "Adjust 'a'" in mode:
            st.info("**Math Tip:** 'a'가 변하면 포물선의 폭이 변하지만, 대칭축의 위치는 고정됩니다!")
        elif "Adjust 'b'" in mode:
            st.info("**Math Tip:** 'b'가 변하면 대칭축($x = -b/2a$)이 좌우로 이동합니다!")
        else:
            st.info("**Math Tip:** 'c'가 변하면 그래프가 그대로 위아래로 평행이동합니다!")
    else:
        st.error("MISS! Try adjusting the value.")
