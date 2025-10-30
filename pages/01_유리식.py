# ----------------------------------------------------
    # 풀이/필기 공간 (Canvas)
    # ----------------------------------------------------
    st.markdown("### 📝 풀이/필기 공간")
    col_tools, col_canvas = st.columns([1, 4])
    
    # 💡 [수정] 지우개 상태를 저장하는 새로운 세션 키를 사용합니다.
    eraser_key = f"is_eraser_{st.session_state.canvas_key}"
    if eraser_key not in st.session_state:
        st.session_state[eraser_key] = False

    with col_tools:
        drawing_mode = st.selectbox("도구 선택", ["freedraw", "line", "rect", "circle", "transform"], index=0, key=f"tool_{st.session_state.canvas_key}")
        
        # 💡 [수정] st.color_picker를 먼저 실행하여 키를 생성하고, 값을 변수에 저장합니다.
        default_color = "#000000"
        stroke_color_picker = st.color_picker("펜/하이라이트 색상", default_color, key=f"color_picker_{st.session_state.canvas_key}")
        stroke_width = st.slider("펜 두께", 1, 20, 3, key=f"width_{st.session_state.canvas_key}")
        
        # 실제 펜 색상을 결정: 지우개 모드이거나, 사용자가 색을 선택했을 때
        if st.button("지우개 활성화", key=f"eraser_btn_{st.session_state.canvas_key}"):
            # 지우개 버튼을 누르면 상태를 토글합니다.
            st.session_state[eraser_key] = not st.session_state[eraser_key]
            st.rerun() # 상태 변경 후 즉시 재실행
            
        if st.session_state[eraser_key]:
            st.warning("지우개 모드 활성화됨 (펜 색상: 흰색)")

        if st.button("전체 지우기", key=f"clear_canvas_{st.session_state.canvas_key}"):
            st.session_state.canvas_key += 1
            st.rerun()
            
    # 최종 캔버스 색상 결정
    if st.session_state[eraser_key]:
        final_stroke_color = "#FFFFFF" # 지우개 모드일 때 흰색
    else:
        final_stroke_color = stroke_color_picker # 일반 모드일 때 사용자가 선택한 색상

    with col_canvas:
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color=final_stroke_color, 
            background_color="#FFFFFF",
            update_streamlit=True,
            height=300,
            drawing_mode=drawing_mode,
            point_display_radius=0,
            key=f"canvas_{st.session_state.canvas_key}",
        )
