import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. 페이지 설정
st.set_page_config(page_title="Kumgok Math Class", layout="centered")

# --- UI 스타일 (한글 깨짐 방지 및 버튼 강조) ---
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; height: 60px; font-size: 1.5rem !important;
        background: #4f46e5 !important; color: white !important; border-radius: 12px !important;
    }
    .status-box { background: #f1f5f9; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 20px; }
    #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# 2. 미션 모드 및 사이드바 설정
st.sidebar.header("🎯 학습 모드 선택")
mode = st.sidebar.selectbox("미션을 선택하세요", ["A: a(폭) 조절하기", "B: b(축) 조절하기", "C: c(높이) 조절하기"])

# 기본값 설정
default_a, default_b, default_c = -1.5, 8.0, 2.0

with st.sidebar:
    st.write("---")
    if "A:" in mode:
        a = st.slider("계수 a (그래프 폭)", -5.0, -0.2, default_a, 0.1)
        b, c = default_b, default_c
    elif "B:" in mode:
        b = st.slider("계수 b (축의 위치)", 0.0, 20.0, default_b, 0.1)
        a, c = default_a, default_c
    else:
        c = st.slider("계수 c (시작 높이)", 0.0, 10.0, default_c, 0.1)
        a, b = default_a, default_b

    if st.button("새 목표 지점 생성"):
        st.session_state.tx = round(np.random.uniform(7, 15), 1)
        st.session_state.ty = round(np.random.uniform(1, 6), 1)
        st.rerun()

if 'tx' not in st.session_state:
    st.session_state.tx, st.session_state.ty = 11.0, 3.5

# 3. 수학 계산 (궤적 및 범위)
axis_x = -b / (2*a)
vertex_y = c - b**2 / (4*a)
x_end = (-b - np.sqrt(max(0, b**2 - 4*a*c))) / (2*a)

x_full = np.linspace(0, x_end, 40) # 애니메이션 프레임
y_full = a * x_full**2 + b * x_full + c

# 4. 그래프 그리기 함수 (좌표축 선명하게)
def draw_plot(step=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 궤적 범위에 맞춰 축 범위 설정
    max_x = max(x_end, st.session_state.tx) + 2
    max_y = max(vertex_y, st.session_state.ty) + 2
    
    ax.set_xlim(-1, max_x)
    ax.set_ylim(-1, max_y)
    
    # 1. 좌표축 강조 및 눈금 표시
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # 2. 목표 지점 (빨간 사각형)
    ax.add_patch(plt.Rectangle((st.session_state.tx-0.4, st.session_state.ty-0.2), 0.8, 0.4, color='red', zorder=5))
    ax.text(st.session_state.tx, st.session_state.ty+0.5, f"({st.session_state.tx}, {st.session_state.ty})", 
            ha='center', color='red', fontweight='bold')

    # 3. 노란 점선 (대칭축) - 희미하게 가이드만
    ax.axvline(x=axis_x, color='#FFD700', linestyle='--', alpha=0.4)

    # 4. 공과 궤적
    if step is not None:
        # 애니메이션 중
        ax.plot(x_full[:step], y_full[:step], color='#4f46e5', lw=3)
        ax.plot(x_full[step], y_full[step], 'o', color='orange', ms=12, mec='black')
    else:
        # 대기 중 (실시간 점선 가이드)
        ax.plot(x_full, y_full, color='#4f46e5', alpha=0.3, ls='--')
        ax.plot(0, c, 'o', color='orange', ms=12, mec='black')

    ax.set_xlabel("x (Distance)")
    ax.set_ylabel("y (Height)")
    return fig

# 5. 메인 화면 실행
st.markdown(f"<div class='status-box'>{mode}<br>목표 좌표: ({st.session_state.tx}, {st.session_state.ty})</div>", unsafe_allow_html=True)

placeholder = st.empty()
placeholder.pyplot(draw_plot())

if st.button("공 던지기 🚀"):
    # 애니메이션 진행
    for i in range(len(x_full)):
        placeholder.pyplot(draw_plot(step=i))
    
    # 결과 판정
    dist = np.sqrt((x_full - st.session_state.tx)**2 + (y_full - st.session_state.ty)**2)
    if np.min(dist) < 0.7:
        st.balloons()
        st.success("🎯 골인! 미션 성공!")
    else:
        st.error("앗! 빗나갔습니다. 슬라이더를 다시 조절해보세요.")
