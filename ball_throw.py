import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# 1. 페이지 설정
st.set_page_config(page_title="이차함수 농구 미션", page_icon="🎯", layout="centered")

# --- UI 스타일링 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@600;800&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    .main-title { font-size: 2.8rem !important; font-weight: 800; text-align: center; color: #1e293b; margin-bottom: 5px; }
    .mission-box { 
        background-color: #f1f5f9; 
        padding: 15px; 
        border-radius: 12px; 
        border-left: 5px solid #4f46e5; 
        margin-bottom: 20px; 
        text-align: center; 
        font-size: 1.1rem;
    }
    .stButton>button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%) !important;
        height: 60px !important;
        font-size: 1.4rem !important;
        border-radius: 12px !important;
    }
    [data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 2px solid #e2e8f0; }
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; display: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🏀 Kumgok Math Class</div>", unsafe_allow_html=True)

# 2. 미션 목표 좌표 설정 (세션 상태 유지)
if 'target_x' not in st.session_state:
    st.session_state.target_x = round(random.uniform(7.0, 14.0), 1)
    st.session_state.target_y = round(random.uniform(2.0, 5.0), 1)

st.markdown(f"""
<div class='mission-box'>
    <b>🎯 미션: 빨간 골대를 통과시켜라!</b><br>
    목표 좌표: <span style='color:#ef4444;'>x = {st.session_state.target_x}, y = {st.session_state.target_y}</span>
</div>
""", unsafe_allow_html=True)

# 3. 사이드바 계수 설정
with st.sidebar:
    st.header("⚙️ 함수 파라미터")
    st.write("y = ax² + bx + c")
    
    # 계수 조절 슬라이더
    a = st.slider("계수 a (중력의 영향)", -4.0, -0.5, -1.5, 0.1, help="값이 작을수록 궤적이 급격히 꺾입니다.")
    b = st.slider("계수 b (던지는 힘)", 0.0, 15.0, 7.0, 0.1, help="값이 클수록 멀리 날아갑니다.")
    c = st.slider("계수 c (던지는 높이)", 0.0, 5.0, 1.8, 0.1, help="y절편(시작 높이)을 결정합니다.")
    
    st.divider()
    if st.button("🔄 새로운 미션 시작"):
        st.session_state.target_x = round(random.uniform(7.0, 14.0), 1)
        st.session_state.target_y = round(random.uniform(2.0, 5.0), 1)
        st.rerun()

# 4. 데이터 계산 (궤적 및 낙하 지점)
# 근의 공식을 이용해 땅에 닿는 x_end 계산: ax² + bx + c = 0
discriminant = max(0, b**2 - 4*a*c)
x_end = (-b - np.sqrt(discriminant)) / (2*a)
x_frames = np.linspace(0, x_end, 50)
y_frames = a * x_frames**2 + b * x_frames + c

# 5. 그래프 시각화 함수
def draw_plot(is_animating=False):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.set_xlabel("거리 (x)")
    ax.set_ylabel("높이 (y)")
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # 골대 (Target) 그리기
    goal = plt.Rectangle((st.session_state.target_x - 0.4, st.session_state.target_y - 0.1), 0.8, 0.2, color='#ef4444', zorder=3)
    ax.add_patch(goal)
    ax.text(st.session_state.target_x, st.session_state.target_y + 0.3, "GOAL", color='#ef4444', ha='center', fontweight='bold')

    if not is_animating:
        # [핵심] 실시간 점선 가이드라인
        ax.plot(x_frames, y_frames, color='#4f46e5', alpha=0.3, linestyle='--', label='예상 궤적')
        ax.plot(0, c, 'o', color='#f59e0b', markersize=12, markeredgecolor='black', label='시작점')
        ax.set_title("슬라이더를 움직여 점선을 골대에 맞추세요!", fontsize=12, color='#4f46e5')
        return fig
    else:
        # 애니메이션용 초기 설정
        trace_line, = ax.plot([], [], color='#4f46e5', alpha=0.6, linewidth=3)
        ball, = ax.plot([], [], 'o', color='#f59e0b', markersize=15, markeredgecolor='black', zorder=5)
        
        # 가이드는 더 연하게 배경으로 유지
        ax.plot(x_frames, y_frames, color='#4f46e5', alpha=0.1, linestyle='--')

        def animate(i):
            trace_line.set_data(x_frames[:i], y_frames[:i])
            ball.set_data([x_frames[i]], [y_frames[i]])
            return trace_line, ball

        ani = animation.FuncAnimation(fig, animate, frames=len(x_frames), interval=30, blit=True, repeat=False)
        return ani

# 6. 메인 화면 로직
launch = st.button("🚀 공 던지기!", use_container_width=True, type="primary")

if launch:
    # 성공 판정: 궤적 중 골대 중심과의 최소 거리 계산
    dist = np.sqrt((x_frames - st.session_state.target_x)**2 + (y_frames - st.session_state.target_y)**2)
    is_success = np.min(dist) < 0.6 # 판정 오차 범위

    # 애니메이션 출력
    ani = draw_plot(is_animating=True)
    st.components.v1.html(ani.to_jshtml(), height=550)
    
    if is_success:
        st.balloons()
        st.success(f"🎯 완벽합니다! 좌표 ({st.session_state.target_x}, {st.session_state.target_y}) 명중!")
    else:
        st.error("앗! 골대를 벗어났습니다. 점선 가이드를 참고하여 계수를 다시 조정해보세요.")
else:
    # 버튼 누르기 전 실시간 가이드 그래프 표시
    fig = draw_plot(is_animating=False)
    st.pyplot(fig)

# 7. 수학적 원리 안내
with st.expander("📝 이 게임에 숨겨진 수학 원리"):
    st.write(f"""
    - **이차함수의 표준형:** $y = a(x - p)^2 + q$
    - **현재 사용된 일반형:** $y = {a}x^2 + {b}x + {c}$
    - **꼭짓점(최고 높이)의 위치:** $x = -b / 2a$ 일 때 최고 높이에 도달합니다.
    - **y절편(시작 위치):** $x=0$일 때의 값인 상수 $c$가 공을 던지는 높이입니다.
    """)
