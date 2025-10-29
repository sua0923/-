import streamlit as st
import random
from streamlit_drawable_canvas import st_canvas

# ----------------------------------------------------
# 1. 문제 데이터 (총 30개)
# 난이도 ('상', '중', '하') 및 'canvas_state' 추가
# ----------------------------------------------------
FULL_QUIZ_DATA = [
    # OX 문제 15개
    {'type': 'ox', 'level': '하', 'q': "유리식 $\\frac{x^2 - 1}{x + 1}$은 분자와 분모가 모두 다항식이므로 유리식이다.", 'ans': 'O', 'exp': "유리식은 (다항식) / (다항식) 꼴로 분자와 분모가 모두 다항식이므로 유리식입니다."},
    {'type': 'ox', 'level': '하', 'q': "다항식 $3x + 5$는 유리식이 아니다.", 'ans': 'X', 'exp': "다항식은 분모가 $1$인 유리식($\\frac{3x+5}{1} = 3x+5$)에 포함되므로 유리식입니다."},
    {'type': 'ox', 'level': '중', 'q': "$\frac{5}{\sqrt{x}}$는 유리식이다.", 'ans': 'X', 'exp': "분모 $\sqrt{x}$는 다항식이 아니므로 유리식이 아닙니다. 문자의 지수가 음이 아닌 정수여야 다항식입니다."},
    {'type': 'ox', 'level': '중', 'q': "유리식 $\\frac{2x}{x-3}$는 $x=3$에서 성립한다.", 'ans': 'X', 'exp': "유리식은 분모가 $0$이 되는 값($x=3$)에서는 정의되지 않아 성립하지 않습니다. 이를 정의역에서 제외합니다."},
    {'type': 'ox', 'level': '중', 'q': "유리식 $\\frac{x-1}{x^2+1}$는 모든 실수 $x$에서 성립한다.", 'ans': 'O', 'exp': "분모 $x^2+1$은 항상 $1$ 이상이므로 $0$이 될 수 없습니다. 따라서 모든 실수에서 성립합니다."},
    {'type': 'ox', 'level': '하', 'q': "$\\frac{x}{0}$는 유리식이다.", 'ans': 'X', 'exp': "분모에 상수 다항식 '0'은 올 수 없습니다. 수학적으로 분모가 0인 식은 정의되지 않습니다."},
    {'type': 'ox', 'level': '하', 'q': "유리식 $\\frac{x^2+2x+1}{(x+1)^2}$을 약분하면 $1$이 된다. (단, $x \\ne -1$)", 'ans': 'O', 'exp': "분자 $x^2+2x+1 = (x+1)^2$ 이므로, 약분하면 $1$입니다."},
    {'type': 'ox', 'level': '하', 'q': "$\\frac{x}{y}$는 유리식이다. (단, $x, y$는 다항식이다.)", 'ans': 'O', 'exp': "두 다항식의 비(분수 형태)로 나타낼 수 있으므로 유리식입니다."},
    {'type': 'ox', 'level': '중', 'q': "유리식 $\\frac{x+1}{x-1}$에서 $x=1$을 대입할 수 있다.", 'ans': 'X', 'exp': "$x=1$을 대입하면 분모가 $0$이 되어 유리식이 정의되지 않습니다."},
    {'type': 'ox', 'level': '하', 'q': "유리식의 덧셈, 뺄셈, 곱셈 결과는 항상 유리식이다. (단, 나눗셈은 제외)", 'ans': 'O', 'exp': "유리식의 사칙연산 결과는 분자와 분모가 다항식인 유리식 형태로 나타낼 수 있습니다."},
    {'type': 'ox', 'level': '상', 'q': "$\\frac{x^2-4}{x-2} = x+2$는 모든 실수 $x$에서 성립한다.", 'ans': 'X', 'exp': "$x=2$에서는 좌변 $\\frac{0}{0}$이 정의되지 않으므로 $x \\ne 2$일 때만 성립합니다."},
    {'type': 'ox', 'level': '하', 'q': "다항식 $P(x)$의 유리식 $\\frac{P(x)}{Q(x)}$에 대한 역수는 $\\frac{Q(x)}{P(x)}$이다.", 'ans': 'O', 'exp': "유리식의 역수는 분자와 분모를 바꾼 식입니다."},
    {'type': 'ox', 'level': '중', 'q': "분수식의 정의역은 모든 실수이다.", 'ans': 'X', 'exp': "분수식은 분모를 $0$으로 만드는 $x$의 값을 정의역에서 제외해야 합니다."},
    {'type': 'ox', 'level': '하', 'q': "분수식 $\\frac{x+1}{2}$는 다항식으로 분류된다.", 'ans': 'O', 'exp': "분모가 $0$이 아닌 상수이므로 다항식 $P(x) = \\frac{1}{2}x + \\frac{1}{2}$와 같습니다."},
    {'type': 'ox', 'level': '상', 'q': "유리식 $\\frac{x^2+1}{x^2+2}$는 모든 실수에서 성립한다.", 'ans': 'O', 'exp': "분모 $x^2+2$는 항상 $2$ 이상이므로 $0$이 될 수 없습니다. 따라서 모든 실수에서 성립합니다."}, # 추가 15번
    
    # 주관식 문제 15개 (답은 정수)
    {'type': 'sub', 'level': '중', 'q': "유리식 $\\frac{x}{x-1} + \\frac{1}{1-x}$의 값을 간단히 하면? (단, $x \\ne 1$)", 'ans': 1, 'exp': "$1-x = -(x-1)$이므로, $\\frac{x}{x-1} - \\frac{1}{x-1} = \\frac{x-1}{x-1}$. 약분하면 $1$입니다."},
    {'type': 'sub', 'level': '중', 'q': "유리식 $\\frac{x+5}{x+3}$를 $\\frac{k}{x+3} + 1$ 꼴로 나타낼 때, 상수 $k$의 값은? (단, $x \\ne -3$)", 'ans': 2, 'exp': "$x+5 = (x+3) + 2$이므로 $\\frac{x+5}{x+3} = \\frac{x+3}{x+3} + \\frac{2}{x+3} = 1 + \\frac{2}{x+3}$. 따라서 $k=2$입니다."},
    {'type': 'sub', 'level': '상', 'q': "유리식 $\\frac{x+1}{x+2} + \\frac{x+3}{x+2}$의 합을 간단히 했을 때, $x=0$에서의 값은? (단, $x \\ne -2$)", 'ans': 2, 'exp': "두 식을 더하면 $\\frac{2x+4}{x+2} = \\frac{2(x+2)}{x+2} = 2$입니다. $x=0$을 대입해도 값은 $2$입니다."},
    {'type': 'sub', 'level': '중', 'q': "유리식 $\\frac{x^2+x-2}{x-1}$을 간단히 했을 때, $x=0$에서의 값은? (단, $x \\ne 1$)", 'ans': 2, 'exp': "$x^2+x-2 = (x+2)(x-1)$이므로, 약분하면 $x+2$입니다. $x=0$을 대입하면 $0+2=2$입니다."},
    {'type': 'sub', 'level': '상', 'q': "유리식 $\\frac{x^2-9}{x-3} \\div (x+3)$의 값을 간단히 하면 $k$이다. 이때 $x=1$에서의 $k$ 값은? (단, $x \\ne 3, -3$)", 'ans': 1, 'exp': "$\\frac{x^2-9}{x-3} \\div (x+3) = \\frac{(x-3)(x+3)}{x-3} \\times \\frac{1}{x+3} = 1$. $k=1$입니다."},
    {'type': 'sub', 'level': '중', 'q': "유리식 $\\frac{2x^2+3x+1}{x+1}$을 간단히 했을 때, $x=1$에서의 값은? (단, $x \\ne -1$)", 'ans': 3, 'exp': "분자 $2x^2+3x+1 = (2x+1)(x+1)$이므로, 유리식은 $2x+1$로 간단히 됩니다. $x=1$을 대입하면 $2(1)+1 = 3$입니다."},
    {'type': 'sub', 'level': '상', 'q': "$\\frac{1}{x} + \\frac{1}{2x} = \\frac{3}{k}$일 때, $k$는 $2x$이다. 이때 $x=5$일 때 $k$의 값은?", 'ans': 10, 'exp': "좌변을 통분하면 $\\frac{2}{2x} + \\frac{1}{2x} = \\frac{3}{2x}$이므로, $k=2x$입니다. $x=5$를 대입하면 $2 \\times 5 = 10$입니다."},
    {'type': 'sub', 'level': '중', 'q': "$\\frac{1}{x-1} - \\frac{1}{x+1}$을 간단히 했을 때, 분모가 $x^2-1$일 때 분자의 값은? (단, $x \\ne 1, -1$)", 'ans': 2, 'exp': "$\\frac{x+1}{x^2-1} - \\frac{x-1}{x^2-1} = \\frac{(x+1)-(x-1)}{x^2-1} = \\frac{2}{x^2-1}$이므로 분자는 $2$입니다."},
    {'type': 'sub', 'level': '하', 'q': "$\\frac{1}{x-1} \\times \\frac{x^2-1}{3}$을 간단히 했을 때, $x=2$에서의 값은?", 'ans': 1, 'exp': "$\\frac{1}{x-1} \\times \\frac{(x-1)(x+1)}{3} = \\frac{x+1}{3}$입니다. $x=2$를 대입하면 $\\frac{2+1}{3} = 1$입니다."},
    {'type': 'sub', 'level': '하', 'q': "$\\frac{x-1}{x-2} - \\frac{1}{x-2}$을 간단히 했을 때, $x=5$에서의 값은? (단, $x \\ne 2$)", 'ans': 1, 'exp': "두 식을 빼면 $\\frac{x-1-1}{x-2} = \\frac{x-2}{x-2} = 1$입니다. $x=5$를 대입해도 값은 $1$입니다."},
    {'type': 'sub', 'level': '중', 'q': "$\\frac{2}{x} - \\frac{1}{2x}$을 간단히 했을 때, $\\frac{k}{2x}$이다. 상수 $k$의 값은? (단, $x \\ne 0$)", 'ans': 3, 'exp': "$\\frac{4}{2x} - \\frac{1}{2x} = \\frac{3}{2x}$이므로 $k=3$입니다."},
    {'type': 'sub', 'level': '상', 'q': "$\\frac{x}{x-2} = 1 + \\frac{k}{x-2}$일 때, 상수 $k$의 값은? (단, $x \\ne 2$)", 'ans': 2, 'exp': "$\\frac{x}{x-2} = \\frac{(x-2)+2}{x-2} = 1 + \\frac{2}{x-2}$이므로 $k=2$입니다."},
    {'type': 'sub', 'level': '상', 'q': "$\\frac{1}{x} + \\frac{1}{2x} + \\frac{1}{3x}$을 간단히 했을 때, 분모를 $6x$로 통분하면 분자는 $k$이다. $k$의 값은? (단, $x \\ne 0$)", 'ans': 11, 'exp': "$\\frac{6}{6x} + \\frac{3}{6x} + \\frac{2}{6x} = \\frac{11}{6x}$이므로 $k=11$입니다."},
    {'type': 'sub', 'level': '상', 'q': "$\\frac{x^2-1}{x^2+2x+1} \\times \\frac{x+1}{x-1}$을 간단히 했을 때의 상수 값은? (단, $x \\ne 1, -1$)", 'ans': 1, 'exp': "$\\frac{(x-1)(x+1)}{(x+1)^2} \\times \\frac{x+1}{x-1} = 1$입니다."},
    {'type': 'sub', 'level': '하', 'q': "유리식 $\\frac{x+1}{x}$의 값을 $x=1$에서 구하면?", 'ans': 2, 'exp': "$x=1$을 대입하면 $\\frac{1+1}{1} = 2$입니다."}, # 추가 15번
]

# ----------------------------------------------------
# 2. 세션 초기화 및 문제 선택 로직
# ----------------------------------------------------
def restart_quiz():
    """세션 상태를 초기화하고 새로운 10문제를 랜덤으로 선택합니다."""
    # 전체 30문제에서 10문제를 랜덤으로 추출
    st.session_state.question_indices = random.sample(range(len(FULL_QUIZ_DATA)), 10)
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.quiz_history = []
    st.session_state.incorrect_count = 0  
    st.session_state.show_explanation = False 
    st.session_state.quiz_finished = False
    st.session_state.quiz_initialized = True
    st.session_state.is_last_correct = None
    st.session_state.canvas_key = 0 # 캔버스 초기화를 위한 키 초기화

def next_question():
    """다음 문제로 넘어가거나 퀴즈를 종료하고, 캔버스를 초기화합니다."""
    st.session_state.current_index += 1
    st.session_state.incorrect_count = 0
    st.session_state.show_explanation = False
    st.session_state.is_last_correct = None
    st.session_state.canvas_key += 1 # 캔버스 초기화를 위해 키 값 증가
    
    if st.session_state.current_index >= len(st.session_state.question_indices):
        st.balloons()
        st.session_state.quiz_finished = True

def check_answer(q_data, user_input):
    """사용자 답변을 확인하고 정오를 반환합니다."""
    q_type = q_data['type']
    correct_answer = q_data['ans']
    
    if q_type == 'ox':
        is_correct = (user_input.upper() == correct_answer)
    elif q_type == 'sub':
        try:
            user_int = int(user_input)
            is_correct = (user_int == correct_answer)
        except ValueError:
            return False
            
    return is_correct

# ----------------------------------------------------
# 3. Streamlit 앱 메인 함수
# ----------------------------------------------------
def main():
    if 'quiz_initialized' not in st.session_state:
        restart_quiz()

    st.title("🧠 유리식 마스터 10문제 퀴즈")
    
    # 퀴즈 재시작 버튼
    if st.button("🔄 새로운 10문제로 다시 풀기", key='restart_btn_top'):
        restart_quiz()
        st.rerun()

    ## 💡 유리식의 개념 및 성립 조건 복습
    st.header("1. 💡 유리식 개념 복습")
    st.markdown("""
    ---
    **유리식(Rational Expression)**은 두 다항식의 비($\\frac{A}{B}$)로 나타낼 수 있는 식입니다.
    
    수식: $$\frac{A}{B}$$
    * **성립 조건**: 분모 $B$는 **절대 $0$이 아니어야** 합니다 ($B \\ne 0$).
    ---
    """)
    
    st.header(f"2. 📝 문제 풀이 (총 {len(st.session_state.question_indices)}문제)")

    # 퀴즈 종료 상태
    if st.session_state.get('quiz_finished', False):
        st.subheader("🎉 퀴즈 종료!")
        st.success(f"최종 점수: **{st.session_state.score} / {len(st.session_state.question_indices)}**")
        return

    # ----------------------------------------------------
    # 현재 문제 표시 및 제출
    # ----------------------------------------------------
    q_index = st.session_state.question_indices[st.session_state.current_index]
    q_data = FULL_QUIZ_DATA[q_index]
    q_number = st.session_state.current_index + 1
    total_questions = len(st.session_state.question_indices)

    # 난이도 표시
    level_color = {"상": "red", "중": "orange", "하": "green"}
    st.markdown(f"#### 난이도: <span style='color:{level_color.get(q_data['level'], 'gray')};'>**{q_data['level']}**</span>", unsafe_allow_html=True)
    
    st.subheader(f"문제 {q_number}/{total_questions} (유형: {'O/X' if q_data['type'] == 'ox' else '주관식'})")
    st.markdown(f"**{q_data['q']}**")

    # 오답 횟수 표시
    if st.session_state.incorrect_count > 0 and st.session_state.is_last_correct is False:
        st.error(f"❌ 틀렸습니다! (재시도: {st.session_state.incorrect_count}회)")
    
    # 두 번 틀려서 풀이 강제 노출 및 다음 문제로 이동
    if st.session_state.incorrect_count >= 2:
        st.warning("❌ 두 번 틀려 풀이를 공개하고 다음 문제로 넘어갑니다.")
        st.info(f"**정답:** {q_data['ans']} ({'정수' if q_data['type'] == 'sub' else 'O/X'})")
        st.success(f"**풀이:** {q_data['exp']}")
        if st.button("다음 문제로 넘어가기", key='skip_btn'):
            next_question()
            st.rerun()
        return

    # 사용자 입력 폼
    with st.form(key=f'q_form_{q_index}'):
        user_input = None
        if q_data['type'] == 'ox':
            user_input = st.radio("정답은?", ['O', 'X'], key='user_ox')
        else: # 주관식
            user_input = st.text_input("정답을 정수로 입력하세요:", key='user_sub')

        submit_button = st.form_submit_button("제출")
        
        if submit_button:
            is_correct = check_answer(q_data, user_input)

            if is_correct:
                st.session_state.score += 1
                st.session_state.quiz_history.append((q_number, q_data['q'], user_input, True))
                st.session_state.show_explanation = True
                st.session_state.is_last_correct = True
                
            else:
                st.session_state.incorrect_count += 1
                st.session_state.quiz_history.append((q_number, q_data['q'], user_input, False))
                st.session_state.show_explanation = False
                st.session_state.is_last_correct = False
                
            st.rerun()

    # ----------------------------------------------------
    # 풀이/필기 공간 (Canvas)
    # ----------------------------------------------------
    st.markdown("### 📝 풀이/필기 공간")
    col_tools, col_canvas = st.columns([1, 4])
    
    with col_tools:
        # 필기 도구 선택
        drawing_mode = st.selectbox("도구 선택", ["freedraw", "line", "rect", "circle", "transform"], index=0, key=f"tool_{st.session_state.canvas_key}")
        # 펜 색상 및 두께
        stroke_color = st.color_picker("펜/하이라이트 색상", "#000000", key=f"color_{st.session_state.canvas_key}")
        stroke_width = st.slider("펜 두께", 1, 20, 3, key=f"width_{st.session_state.canvas_key}")
        # 지우개 기능 (색상을 배경과 같게 설정)
        if st.button("지우개", key=f"eraser_{st.session_state.canvas_key}"):
            stroke_color = "#FFFFFF" # 배경색과 동일하게 설정하여 지우개 효과
        # 캔버스 초기화 (전체 지우기) - 키 변경을 통해 전체 초기화
        if st.button("전체 지우기", key=f"clear_canvas_{st.session_state.canvas_key}"):
            st.session_state.canvas_key += 1
            st.rerun()

    with col_canvas:
        # 캔버스 컴포넌트
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # 채우기 색상
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color="#FFFFFF",
            update_streamlit=True,
            height=300,
            drawing_mode=drawing_mode,
            point_display_radius=0,
            key=f"canvas_{st.session_state.canvas_key}", # 키가 변경되면 캔버스 내용 초기화
        )

    # ----------------------------------------------------
    # 결과 및 해설 표시 (제출 후)
    # ----------------------------------------------------
    if st.session_state.get('show_explanation'):
        st.success("✅ **정답입니다!** 풀이를 확인하세요.")
        st.info(f"**정답:** {q_data['ans']} ({'정수' if q_data['type'] == 'sub' else 'O/X'})")
        st.success(f"**풀이:** {q_data['exp']}")
        
        # 다음 문제로 이동 버튼
        if st.button("다음 문제 풀기", key='correct_next_btn'):
            next_question()
            st.rerun()

    st.markdown(f"\n---")
    st.subheader(f"현재 점수: {st.session_state.score} / {len(st.session_state.quiz_history)} 문항 완료")

if __name__ == "__main__":
    main()
