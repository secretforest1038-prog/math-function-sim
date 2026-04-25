import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# 1. 페이지 설정
st.set_page_config(page_title="이차함수 농구 미션", page_icon="🎯", layout="centered")

# --- UI 스타일링 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@600;800&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    .main-title { font-size: 2.8rem !important; font-weight: 800; text-align: center; color: #1e293b; margin-bottom: 5px; }
    .mission-box { background-color: #f1f5f9; padding: 15px; border-radius: 12px; border-left: 5px solid #4f46e5; margin-bottom: 20px; text-align: center; }
    [data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 2px solid #e2e8f0; }
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; display: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🏀 수학 미션: 골대에 넣어라!</div>", unsafe_allow_html=True)

# 2. 미션 좌표 설정 (세션 상태 유지)
if 'target_x' not in st.session_state:
    st.session_state.target_x = round(random.uniform(7.0, 14.0), 1)
    st.session_state.target_y = round(random.uniform(2.0, 5.0), 1)

st.markdown(f"""
<div class='mission-box'>
    <b>📍 현재 목표 골대 좌표: ({st.session_state.target_x}, {st.session_state.target_y})</b><br>
    함수 계수를 조절해서 공이 빨간 골대를 통과하게 만드세요!
</div>
""", unsafe_allow_html=True)

# 3. 사이드바 계수 설정
with st.sidebar:
    st.header("⚙️ 궤도 계산기")
    a = st.slider("계수 a (중력)", -4.0, -0.5, -1.5, 0.1)
    b = st.slider("계수 b (던지는 힘)", 0.0, 15.0, 7.0, 0.1)
    c = st.slider("계수 c (손의 높이)", 0.0, 5.0, 1.8, 0.1)
    
    st.divider()
    if st.button("🔄 미션 새로고침 (골대 이동)"):
        st.session_state.target_x = round(random.uniform(7.0, 14.0), 1)
        st.session_state.target_y = round(random.uniform(2.0, 5.0), 1)
        st.rerun()

# 4. 데이터 계산
# 공이 땅에 떨어지는 x값 (근의 공식)
x_end = (-b - np.sqrt(max(0, b**2 - 4*a*c))) / (2*a)
x_frames = np.linspace(0, x_end, 50)
y_frames = a * x_frames**2 + b * x_frames + c

# 5. 애니메이션 및 그래프 생성
def create_basketball_anim():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.set_xlabel("수평 거리 (x)")
    ax.set_ylabel("높이 (y)")
    
    # 골대 그리기 (빨간색 가로선)
    goal = plt.Rectangle((st.session_state.target_x - 0.4, st.session_state.target_y), 0.8, 0.2, color='#ef4444', zorder=3)
    ax.add_patch(goal)
    ax.text(st.session_state.target_x, st.session_state.target_y + 0.4, "GOAL", color='#ef4444', ha='center', fontweight='bold')

    trace_line, = ax.plot([], [], color='#4f46e5', alpha=0.3, linewidth=2)
    ball, = ax.plot([], [], 'o', color='#f59e0b', markersize=15, markeredgecolor='black')

    def animate(i):
        trace_line.set_data(x_frames[:i], y_frames[:i])
        ball.set_data([x_frames[i]], [y_frames[i]])
        return trace_line, ball

    ani = animation.FuncAnimation(fig, animate, frames=len(x_frames), interval=40, blit=True, repeat=False)
    return ani

# 6. 실행 및 성공 판정
play_col, _ = st.columns([1, 2])
with play_col:
    launch = st.button("🚀 공 던지기!", use_container_width=True, type="primary")

if launch:
    # 성공 판정: 공의 궤적 중 골대와 매우 가까운 점이 있는지 체크
    dist = np.sqrt((x_frames - st.session_state.target_x)**2 + (y_frames - st.session_state.target_y)**2)
    is_success = np.min(dist) < 0.6 # 판정 범위 0.6

    ani = create_basketball_anim()
    st.components.v1.html(ani.to_jshtml(), height=550)
    
    if is_success:
        st.balloons()
        st.success("🎯 GOAL!!! 수학적으로 완벽한 궤도입니다!")
    else:
        st.error("앗! 골대를 빗나갔습니다. 계수를 다시 조정해보세요.")
else:
    # 정적 가이드 그래프
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.grid(True, linestyle='--', alpha=0.3)
    # 골대 표시
    goal = plt.Rectangle((st.session_state.target_x - 0.4, st.session_state.target_y), 0.8, 0.2, color='#ef4444', alpha=0.5)
    ax.add_patch(goal)
    # 시작점 표시
    ax.plot(0, c, 'o', color='#f59e0b', markersize=10)
    st.pyplot(fig)
