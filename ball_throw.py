# ... (앞선 코드 동일) ...

# 5. 애니메이션 및 그래프 생성 함수 수정
def create_basketball_anim():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.set_xlabel("수평 거리 (x)")
    ax.set_ylabel("높이 (y)")
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # [추가] 전체 가이드 궤적 (배경에 깔리는 연한 점선)
    ax.plot(x_frames, y_frames, color='#4f46e5', alpha=0.15, linestyle='--', label='가이드라인')

    # 골대 그리기
    goal = plt.Rectangle((st.session_state.target_x - 0.4, st.session_state.target_y), 0.8, 0.2, color='#ef4444', zorder=3)
    ax.add_patch(goal)
    ax.text(st.session_state.target_x, st.session_state.target_y + 0.4, "GOAL", color='#ef4444', ha='center', fontweight='bold')

    trace_line, = ax.plot([], [], color='#4f46e5', alpha=0.5, linewidth=3) # 지나가는 선 (조금 더 진하게)
    ball, = ax.plot([], [], 'o', color='#f59e0b', markersize=15, markeredgecolor='black', zorder=5)

    def animate(i):
        trace_line.set_data(x_frames[:i], y_frames[:i])
        ball.set_data([x_frames[i]], [y_frames[i]])
        return trace_line, ball

    ani = animation.FuncAnimation(fig, animate, frames=len(x_frames), interval=40, blit=True, repeat=False)
    return ani

# 6. 실행 및 성공 판정 부분 수정
play_col, _ = st.columns([1, 2])
with play_col:
    launch = st.button("🚀 공 던지기!", use_container_width=True, type="primary")

if launch:
    dist = np.sqrt((x_frames - st.session_state.target_x)**2 + (y_frames - st.session_state.target_y)**2)
    is_success = np.min(dist) < 0.6 

    ani = create_basketball_anim()
    st.components.v1.html(ani.to_jshtml(), height=550)
    
    if is_success:
        st.balloons()
        st.success("🎯 GOAL!!! 수학적으로 완벽한 궤도입니다!")
    else:
        st.error("앗! 골대를 빗나갔습니다. 점선을 보고 다시 조정해보세요.")
else:
    # [수정] 버튼 누르기 전 미리보기 화면에도 점선 궤적 표시
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # 현재 설정값에 따른 실시간 점선 궤적
    ax.plot(x_frames, y_frames, color='#4f46e5', alpha=0.3, linestyle='--')
    
    # 골대 표시
    goal = plt.Rectangle((st
