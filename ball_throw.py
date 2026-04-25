import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Page Config
st.set_page_config(page_title="Math Ball: Mission", layout="centered")

# --- UI CSS ---
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; height: 60px; font-size: 1.5rem !important;
        background: #4f46e5 !important; color: white !important; border-radius: 15px !important;
    }
    .mission-info { background: #e0e7ff; padding: 10px; border-radius: 10px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. Mission Mode Selection
st.sidebar.header("Select Learning Mode")
mode = st.sidebar.selectbox("Choose Mission", ["Mode A: Adjust 'a'", "Mode B: Adjust 'b'", "Mode C: Adjust 'c'"])

# Default Values
default_a, default_b, default_c = -1.5, 8.0, 2.0

# 3. Sidebar Controls based on Mode
with st.sidebar:
    st.write("---")
    if mode == "Mode A: Adjust 'a'":
        st.info("Goal: Change the width of parabola")
        a = st.slider("a (Gravity)", -5.0, -0.1, default_a, 0.1)
        b, c = default_b, default_c
    elif mode == "Mode B: Adjust 'b'":
        st.info("Goal: Move the vertex (axis)")
        b = st.slider("b (Velocity)", 0.0, 20.0, default_b, 0.1)
        a, c = default_a, default_c
    else:
        st.info("Goal: Change the starting point")
        c = st.slider("c (Initial Height)", 0.0, 10.0, default_c, 0.1)
        a, b = default_a, default_b

    if st.button("New Target Location"):
        st.session_state.tx = round(np.random.uniform(6, 14), 1)
        st.session_state.ty = round(np.random.uniform(1, 5), 1)
        st.rerun()

if 'tx' not in st.session_state:
    st.session_state.tx, st.session_state.ty = 10.0, 4.0

# 4. Math Calculations
x_end = (-b - np.sqrt(max(0, b**2 - 4*a*c))) / (2*a)
x_full = np.linspace(0, x_end, 40) # 프레임 수 축소로 속도 향상
y_full = a * x_full**2 + b * x_full + c
y_max = c - b**2 / (4*a)

# 5. Graph Drawing
def draw_frame(current_x=None, current_y=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(-1, max(x_end, st.session_state.tx) + 2)
    ax.set_ylim(-0.5, max(y_max, st.session_state.ty) + 2)
    
    # Target
    ax.add_patch(plt.Rectangle((st.session_state.tx-0.4, st.session_state.ty-0.1), 0.8, 0.2, color='red'))
    
    # Dashed Guide
    ax.plot(x_full, y_full, color='indigo', alpha=0.15, linestyle='--')
    
    if current_x is not None:
        idx = (np.abs(x_full - current_x)).argmin()
        ax.plot(x_full[:idx], y_full[:idx], color='indigo', alpha=0.6, lw=3)
        ax.plot(current_x, current_y, 'o', color='orange', ms=12)
    else:
        ax.plot(0, c, 'o', color='orange', ms=12)
    
    ax.grid(True, alpha=0.2)
    return fig

# 6. Execution
st.markdown(f"<div class='mission-info'>{mode} - Target: ({st.session_state.tx}, {st.session_state.ty})</div>", unsafe_allow_html=True)
placeholder = st.empty()
placeholder.pyplot(draw_frame())

if st.button("LAUNCH 🚀"):
    for i in range(len(x_full)):
        placeholder.pyplot(draw_frame(x_full[i], y_full[i]))
        time.sleep(0.005) # 속도 대폭 향상
    
    # Result & Principle Feedback
    dist = np.sqrt((x_full - st.session_state.tx)**2 + (y_full - st.session_state.ty)**2)
    if np.min(dist) < 0.6:
        st.balloons()
        st.success("SUCCESS!")
        
        # 계수별 학습 원리 도출
        if mode == "Mode A: Adjust 'a'":
            st.info("💡 Principle: 'a' 결정! 그래프의 폭과 볼록한 정도를 결정합니다. (절댓값이 클수록 좁아짐)")
        elif mode == "Mode B: Adjust 'b'":
            st.info("💡 Principle: 'b' 결정! 대칭축의 위치를 좌우로 움직입니다.")
        else:
            st.info("💡 Principle: 'c' 결정! y절편으로서 공의 시작 높이를 결정합니다.")
    else:
        st.error("MISS! ADJUST THE VALUE.")
