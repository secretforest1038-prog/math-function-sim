import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="이차함수 공 던지기 시각화", page_icon="🏀", layout="centered")

# --- UI 스타일링 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@600;800&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 800;
        text-align: center;
        color: #1e293b;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.2rem;
        text-align: center;
        color: #64748b;
        margin-bottom: 30px;
    }
    /* 사이드바 UI 스타일 */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 2px solid #e2e8f0;
    }
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; display: none; }
    </style>
""", unsafe_allow_html=True)

# 2. 메인 화면 타이틀
st.markdown("<div class='main-title'>🏀 이차함수 포물선 운동 시각화</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>공을 던질 때 생기는 궤적(y = ax² + bx + c)을 그려보세요.</div>", unsafe_allow_html=True)

# --- 사이드바: 이차함수 계수 설정 (조정값) ---
with st.sidebar:
    st.header("⚙️ 함수 계수 설정")
    st.write("---")
    
    # [조건 a]: 중력 가속도 영향 (y축 방향 가속도)
    # 물리학에서는 -1/2 * g가 사용되지만, 수업 난이도를 고려해 계수 a 자체를 조정하도록 합니다.
    # 포물선은 위로 볼록해야 하므로 a는 항상 음수여야 합니다.
    a = st.slider(
        "계수 a (중력 가속도 영향)", 
        min_value=-5.0, # 위로 볼록 유지
        max_value=-0.1, 
        value=-1.0, # 기본값
        step=0.1,
        help="이 값이 작을수록(절댓값이 클수록) 공이 빨리 떨어집니다. (중력이 셈)"
    )
    
    # [조건 b]: 초기 속도 영향 (y축 방향 초기 속도)
    # 이 값이 클수록 공이 위로 세게 던져집니다.
    b = st.slider(
        "계수 b (초기 속도)", 
        min_value=0.0, 
        max_value=20.0, 
        value=5.0, # 기본값
        step=0.5,
        help="이 값이 클수록 공이 더 높이, 더 멀리 날아갑니다."
    )
    
    # [조건 c]: 초기 위치 (y 절편)
    # 던지는 사람의 키나 손의 높이입니다.
    c = st.slider(
        "계수 c (초기 위치)", 
        min_value=0.0, 
        max_value=10.0, 
        value=2.0, # 기본값
        step=0.1,
        help="공을 던지기 시작하는 높이입니다. (y절편)"
    )
    st.divider()
    st.write("y = ax² + bx + c")

# --- 궤적 계산 및 그래프 그리기 ---

# 1. 계산 범위 설정 (x: 시간 또는 수평 거리)
# 공이 땅에 떨어질 때(y=0)까지 그리기 위해 근의 공식을 사용하여 x_max를 대략적으로 구함
# ax^2 + bx + c = 0 의 양수 근
x_end = (-b - np.sqrt(b**2 - 4*a*c)) / (2*a)
x = np.linspace(0, x_end, 500) # 0부터 땅에 떨어질 때까지 500개의 점

# 2. 이차함수 값 계산 (y: 공의 높이)
y = a * x**2 + b * x + c

# 3. 최댓값 (꼭짓점) 찾기
vertex_x = -b / (2*a)
vertex_y = c - b**2 / (4*a)

# 4. Matplotlib으로 그래프 그리기
fig, ax = plt.subplots(figsize=(8, 5))

# 공의 궤적 (포물선)
ax.plot(x, y, color='#4f46e5', linewidth=3, label='Ball Trajectory')

# 공이 던져진 지점 (초기 위치)
ax.scatter(0, c, color='#FF6B6B', s=100, edgecolors='black', zorder=5, label='Start Point (c)')

# 땅에 떨어진 지점 (x절편)
ax.scatter(x_end, 0, color='#333', s=100, marker='X', zorder=5, label='Ground (y=0)')

# 꼭짓점 (최고 높이) 표시
ax.scatter(vertex_x, vertex_y, color='#FFA502', s=80, marker='*', zorder=4, label=f'Max Height: {vertex_y:.2f}m')
ax.vlines(vertex_x, 0, vertex_y, color='#FFA502', linestyle='--') # 최고 높이까지의 점선

# 그래프 스타일링
ax.set_title(f"y = {a:.1f}x² + {b:.1f}x + {c:.1f}", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("수평 거리 (x)", fontsize=11)
ax.set_ylabel("높이 (y)", fontsize=11)
ax.set_ylim(0, vertex_y + 1) # y축 범위를 최고 높이보다 조금 더 높게 설정
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=9, loc='upper right')

# 화면에 그래프 표시
st.pyplot(fig)

# --- 결과 분석 및 수업 팁 섹션 ---
st.write("---")
st.subheader("💡 궤적 분석")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    * **공이 던져진 높이:** `{c:.2f}`m
    * **최고 높이:** `{vertex_y:.2f}`m
    """)
with col2:
    st.markdown(f"""
    * **최고 높이에 도달하는 거리:** `{vertex_x:.2f}`m
    * **땅에 떨어지는 거리:** `{x_end:.2f}`m
    """)

# 수업 안내 메시지
st.markdown(f"""
<div style="background-color: #f1f5f9; padding: 15px; border-radius: 10px; color: #1e293b;">
    <span style="font-weight: bold;">🧑‍🏫 수업 시간에 활용해 보세요!</span><br>
    1. 계수 <b>a</b>를 더 작은 값(절댓값이 큰 값)으로 움직이면 궤적이 어떻게 변하나요? (중력이 강한 목성으로 가면?)<br>
    2. 계수 <b>b</b>(초기 속도)를 크게 하면 최고 높이는 어떻게 되나요?<br>
    3. 계수 <b>c</b>(초기 위치)가 0이면 공은 어디서 출발하나요?
</div>
""", unsafe_allow_html=True)