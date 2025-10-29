import streamlit as st
import random

# 유리식 문제 데이터 (수식 표현 수정)
quiz_data = [
    ("$\frac{x^2 - 1}{x + 1}$는 유리식이다.", True, "유리식은 (다항식) / (다항식) 꼴로 분자와 분모가 모두 다항식이므로 유리식입니다."),
    ("다항식 $3x + 5$는 유리식이 아니다.", False, "다항식은 분모가 $1$인 유리식($\frac{3x+5}{1}$)에 포함되므로 유리식입니다."),
    ("$\frac{5}{\sqrt{x}}$는 유리식이다.", False, "분모 $\sqrt{x}$는 다항식이 아니므로 유리식이 아닙니다. 문자의 지수가 음이 아닌 정수여야 다항식입니다."),
    ("유리식 $\frac{2x}{x-3}$는 $x=3$에서 성립한다.", False, "유리식은 분모가 $0$이 되는 값($x-3=0$, 즉 $x=3$)에서는 정의되지 않아 성립하지 않습니다. 이를 정의역에서 제외합니다."),
    ("유리식 $\frac{x-1}{x^2+1}$는 모든 실수 $x$에서 성립한다.", True, "분모 $x^2+1$은 항상 $x^2 \ge 0$이므로 $x^2+1 \ge 1$입니다. 따라서 분모가 절대 $0$이 될 수 없으므로 모든 실수에서 성립합니다."),
    ("$\frac{x}{0}$는 유리식이다.", False, "유리식은 (다항식) / (다항식) 꼴이지만, 분모에 상수 다항식 '0'은 올 수 없습니다. 수학적으로 분모가 0인 식은 정의되지 않습니다."),
    ("유리식 $\frac{x^2+x+1}{2}$는 $x$에 대한 다항식이다.", True, "분모가 $0$이 아닌 상수 다항식인 경우, 이 유리식은 다항식으로 분류됩니다."),
]

def check_answer(question_index, user_answer):
    """사용자 답변의 정오를 확인하고 해설을 반환합니다."""
    is_correct = quiz_data[question_index][1]
    is_user_correct = (user_answer == "O" and is_correct) or (user_answer == "X" and not is_correct)

    result_text = "✅ **정답입니다!**" if is_user_correct else "❌ **오답입니다.**"
    explanation = f"**해설:** {quiz_data[question_index][2]}"

    return result_text, explanation

def display_quiz():
    """Streamlit 앱 화면을 구성하고 퀴즈를 진행합니다."""
    st.title("📚 유리식 개념 O/X 퀴즈 (ver.2)")
    
    ## 🧠 유리식의 개념 설명
    st.header("1. 💡 유리식의 개념")
    st.markdown("""
    ---
    **유리식(Rational Expression)**은 **두 다항식의 비**로 나타낼 수 있는 식입니다.

    수식으로 표현하면 다음과 같습니다:
    $$\\text{유리식} = \\frac{A}{B}$$
    단, $A$와 $B$는 **다항식**이며, $B$는 **상수 다항식 $0$이 아닙니다**.

    * **다항식도 유리식이다**: 분모 $B$가 $0$이 아닌 상수 다항식일 경우, 유리식은 다항식이 됩니다. (예: $\frac{3x+5}{1} = 3x+5$)
    * **분수식**: 유리식 중에서 다항식이 아닌 식, 즉 **분모에 문자가 포함**된 식을 특별히 분수식이라고 부릅니다.
    ---
    """)

    ## 🚫 유리식의 성립 조건
    st.header("2. 🚫 유리식의 성립 조건")
    st.markdown("""
    ---
    유리식 $\\frac{A}{B}$가 **성립(정의)하기 위한 조건**은 **분모가 $0$이 아니어야** 합니다.
    $$B \\ne 0$$
    분모 $B$를 $0$으로 만드는 $x$의 값에서는 유리식이 정의되지 않아 **성립하지 않습니다**.
    ---
    """)
    
    ## 퀴즈 진행 섹션
    st.header("3. 📝 O/X 문제 풀이")
    
    if 'current_question' not in st.session_state:
        st.session_state.current_question = -1  # 초기 상태는 문제 로드 전
        st.session_state.score = 0
        st.session_state.quiz_history = []
        st.session_state.used_questions = []

    # 문제 선택 및 초기화
    if st.session_state.current_question == -1 or 'new_question' in st.session_state and st.session_state.new_question:
        if not st.session_state.used_questions:
            st.session_state.used_questions = list(range(len(quiz_data)))
            random.shuffle(st.session_state.used_questions)
        
        if st.session_state.used_questions:
            st.session_state.current_question = st.session_state.used_questions.pop(0)
            st.session_state.new_question = False
            st.session_state.answer_shown = False
            
        else:
            st.info("모든 문제를 다 풀었습니다! 🎉")
            st.session_state.current_question = -2 # 종료 상태
            
    
    if st.session_state.current_question >= 0:
        q_idx = st.session_state.current_question
        question_text = quiz_data[q_idx][0]

        st.subheader(f"문제 {len(st.session_state.quiz_history) + 1}")
        st.latex(question_text.replace('$','')) # st.latex는 내부적으로 $를 포함하여 렌더링하므로 제거
        # st.markdown(question_text) # st.markdown으로 하면 수식 표현이 더 잘 될 수도 있습니다.

        col1, col2 = st.columns(2)
        with col1:
            o_button = st.button("O (맞다)", key="o_btn", use_container_width=True, disabled=st.session_state.get('answer_shown', False))
        with col2:
            x_button = st.button("X (틀리다)", key="x_btn", use_container_width=True, disabled=st.session_state.get('answer_shown', False))

        user_answer = None
        
        if o_button or x_button:
            user_answer = "O" if o_button else "X"
            result_text, explanation = check_answer(q_idx, user_answer)
            st.session_state.quiz_history.append((q_idx, user_answer, result_text, explanation))
            if "정답입니다" in result_text:
                st.session_state.score += 1
            st.session_state.answer_shown = True
            st.session_state.last_result = (result_text, explanation)
            st.rerun()

    if st.session_state.get('answer_shown', False):
        res, exp = st.session_state.last_result
        st.markdown(f"#### **결과: {res}**")
        st.info(exp)
        
        # 다음 문제 버튼
        if st.button("다음 문제 풀기", key="next_btn"):
            st.session_state.new_question = True
            st.rerun()

    # 결과 및 기록 표시
    st.subheader(f"\n---")
    st.subheader(f"총 점수: {st.session_state.score} / {len(st.session_state.quiz_history)}")
    
    if st.session_state.current_question == -2:
        st.success(f"최종 점수: {st.session_state.score} / {len(st.session_state.quiz_history)}")


if __name__ == "__main__":
    display_quiz()
