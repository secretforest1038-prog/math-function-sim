import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="이차함수 포물선 시뮬레이터", page_icon="🏀", layout="centered")

# --- UI 스타일링 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@600;800&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    .main-title { font-size: 2.5rem !important; font-weight: 800; text-align: center; color: #1e293b; margin-bottom: 30px; }
    [data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 2px solid #e2e8f0; }
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; display: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🏀 포물선 운동 애니메이션</div>", unsafe_allow_html=True)

# 2. 사이드바 계수 설정
with st.sidebar:
    st.header("⚙️ 함수 계수 설정")
    a = st.slider("계수 a (중력)", -5.0, -0.5, -1.5, 0.1)
    b = st.slider("계수 b (속도)", 0.0, 20.0, 8.0, 0.5)
    c = st.slider("계수 c (높이)", 0.0, 10.0, 2.0, 0.1)
    st.divider()
    st.write(f"현재 함수: y = {a}x² + {b}x + {c}")

# 3. 궤적 데이터 계산
x_end = (-b - np.sqrt(b**2 - 4*a*c)) / (2*a)
x_data = np.linspace(0, x_end, 60) # 애니메이션 프레임 수 (60프레임)
y_data = a * x_data**2 + b * x_data + c

# 4. 애니메이션 생성 함수
def create_animation():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, x_end + 1)
    ax.set_ylim(0, max(y_data) + 2)
    ax.set_xlabel("수평 거리 (x)")
    ax.set_ylabel("높이 (y)")
    ax.grid(True, linestyle='--', alpha=0.4)

    # 선과 점 초기화
    trace_line, = ax.plot([], [], color='#4f46e5', alpha=0.3, linewidth=2) # 지나간 궤적 (흐릿하게)
    current_ball, = ax.plot([], [], 'o', color='#FF6B6B', markersize=12)   # 현재 공 위치
    
    # 텍스트 정보
    info_text = ax.text(0.5, 0.9, '', transform=ax.transAxes, ha='center', fontweight='bold')

    def init():
        trace_line.set_data([], [])
        current_ball.set_data([], [])
        info_text.set_text('')
        return trace_line, current_ball, info_text

    def animate(i):
        # 지나온 궤적 데이터
        trace_line.set_data(x_data[:i], y_data[:i])
        # 현재 공 위치
        current_ball.set_data([x_data[i]], [y_data[i]])
        # 현재 높이 텍스트 업데이트
        info_text.set_text(f"높이: {y_data[i]:.2f}m")
        return trace_line, current_ball, info_text

    ani = animation.FuncAnimation(fig, animate, frames=len(x_data), init_func=init, blit=True, interval=50, repeat=False)
    return ani

# 5. 실행 버튼 및 출력
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    play_btn = st.button("🚀 공 던지기!", use_container_width=True)

if play_btn:
    ani = create_animation()
    # 애니메이션을 HTML5 비디오로 변환하여 Streamlit에 표시
    components_html = ani.to_jshtml()
    st.components.v1.html(components_html, height=600)
else:
    # 버튼 누르기 전 미리보기 정적 그래프
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_data, y_data, color='#4f46e5', alpha=0.1, linestyle='--') # 가이드 라인
    ax.scatter(0, c, color='#FF6B6B', s=100) # 시작점
    ax.set_xlim(0, x_end + 1)
    ax.set_ylim(0, max(y_data) + 2)
    ax.set_xlabel("수평 거리 (x)")
    ax.set_ylabel("높이 (y)")
    ax.grid(True, linestyle='--', alpha=0.4)
    st.pyplot(fig)
    st.info("위의 버튼을 누르면 공이 날아갑니다!")
