import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Page Config
st.set_page_config(page_title="Math Ball", layout="centered")

# --- UI CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #f8fafc !important; }
    .stButton>button { 
        width: 100%; height: 60px; font-size: 1.5rem !important; font-weight: bold !important;
        background: #4f46e5 !important; color: white !important; border-radius: 15px !important;
    }
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Settings
with st.sidebar:
    st.header("Equation: y = ax² + bx + c")
    a = st.slider("a (Gravity)", -5.0, -0.5, -1.5, 0.1)
    b = st.slider("b (Velocity)", 0.0, 20.0, 8.0, 0.1)
    c = st.slider("c (Height)", 0.0, 10.0, 2.0, 0.1)
    
    if st.button("Reset Target"):
        st.session_state.tx = round(np.random.uniform(5, 15), 1)
        st.session_state.ty = round(np.random.uniform(1, 6), 1)
        st.rerun()

# Target Sync
if 'tx' not in st.session_state:
    st.session_state.tx, st.session_state.ty = 10.0, 3.0

# 3. Math Calculations
# Solve ax^2 + bx + c = 0
x_end = (-b - np.sqrt(max(0, b**2 - 4*a*c))) / (2*a)
x_full = np.linspace(0, x_end, 100)
y_full = a * x_full**2 + b * x_full + c
y_max = c - b**2 / (4*a)

# 4. Graph Display Function
def draw_frame(current_x=None, current_y=None, is_guide=True):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Dynamic Range: Ensure everything fits
    ax.set_xlim(-1, max(x_end, st.session_state.tx) + 2)
    ax.set_ylim(-0.5, max(y_max, st.session_state.ty) + 2)
    
    # Target (Red Square)
    ax.add_patch(plt.Rectangle((st.session_state.tx-0.4, st.session_state.ty-0.1), 0.8, 0.2, color='red'))
    
    # Guide Line (Dashed)
    if is_guide:
        ax.plot(x_full, y_full, color='indigo', alpha=0.2, linestyle='--')
    
    # Moving Ball & Trajectory
    if current_x is not None:
        idx = (np.abs(x_full - current_x)).argmin()
        ax.plot(x_full[:idx], y_full[:idx], color='indigo', alpha=0.6, lw=3)
        ax.plot(current_x, current_y, 'o', color='orange', ms=12, mec='black')
    else:
        ax.plot(0, c, 'o', color='orange', ms=12, mec='black')

    ax.grid(True, alpha=0.3)
    return fig

# 5. Execution
placeholder = st.empty()
placeholder.pyplot(draw_frame())

if st.button("LAUNCH 🚀"):
    # Animation Loop: Real-time update
    for i in range(len(x_full)):
        with placeholder.container():
            st.pyplot(draw_frame(x_full[i], y_full[i]))
        time.sleep(0.01) # Speed control
    
    # Result Check
    dist = np.sqrt((x_full - st.session_state.tx)**2 + (y_full - st.session_state.ty)**2)
    if np.min(dist) < 0.6:
        st.balloons()
        st.success("SUCCESS! (TARGET HIT)")
    else:
        st.error("MISS! (TRY AGAIN)")
