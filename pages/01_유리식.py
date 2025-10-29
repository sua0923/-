import streamlit as st
import random

# 유리식 문제 데이터
# (문제 설명, 유리식인지 여부, 성립하지 않는 x 조건 (선택 사항))
quiz_data = [
    ("$\frac{x^2 - 1}{x + 1}$는 유리식이다.", True, "x = -1 에서 정의되지 않습니다."),
    ("다항식 $3x + 5$는 유리식이 아니다.", False, "다항식은 분모가 상수인 유리식에 포함됩니다."),
    ("$\frac{5}{\sqrt{x}}$는 유리식이다.", False, "분모가 다항식이 아니므로 유리식이 아닙니다."),
    ("유리식 $\frac{2x}{x-3}$는 $x=3$에서 성립한다.", False, "분모가 0이 되는 $x=3$에서는 정의되지 않아 성립하지 않습니다."),
    ("유리식 $\frac{x-1}{x^2+1}$는 모든 실수 $x$에서 성립한다.", True, "분모 $x^2+1$은 항상 0보다 크므로, 모든 실수에서 정의됩니다."),
    ("$\frac{x}{0}$는 유리식이다.", False, "분모가 다항식(상수 0)이지만, 수학적으로 정의되지 않습니다."),
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
    st.title("📚 유리식 개념 O/X 퀴즈")
    st.markdown("""
    ---
    ### ✨ 유리식 개념 복습
    유리식은 **두 다항식의 비**로 나타낼 수 있는 식, 즉 **(다항식) / (다항식)** 꼴의 식을 말합니다.
    * **다항식**도 분모가 1인 유리식으로 간주됩니다.
    * 유리식이 **성립하지 않을 때**는 **분모가 0이 되는 $x$의 값**이 존재할 때입니다.
    ---
    """)

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_history = []
        st.session_state.used_questions = []

    # 문제 선택 (반복 피하기)
    if not st.session_state.used_questions:
        st.session_state.used_questions = list(range(len(quiz_data)))
        random.shuffle(st.session_state.used_questions)

    if st.session_state.used_questions:
        st.session_state.current_question = st.session_state.used_questions.pop(0)
    else:
        st.info("모든 문제를 다 풀었습니다! 🎉")
        st.session_state.current_question = -1

    if st.session_state.current_question != -1:
        q_idx = st.session_state.current_question
        question_text = quiz_data[q_idx][0]

        st.header(f"문제 {len(st.session_state.quiz_history) + 1}")
        st.subheader(question_text)

        col1, col2 = st.columns(2)
        with col1:
            o_button = st.button("O (맞다)", key="o_btn", use_container_width=True)
        with col2:
            x_button = st.button("X (틀리다)", key="x_btn", use_container_width=True)

        user_answer = None
        if o_button:
            user_answer = "O"
        elif x_button:
            user_answer = "X"

        if user_answer:
            result_text, explanation = check_answer(q_idx, user_answer)
            st.session_state.quiz_history.append((q_idx, user_answer, result_text, explanation))
            if "정답입니다" in result_text:
                st.session_state.score += 1
            st.rerun()

    # 결과 및 기록 표시
    st.subheader(f"\n---")
    st.subheader(f"현재 점수: {st.session_state.score} / {len(st.session_state.quiz_history)}")

    if st.session_state.quiz_history:
        st.markdown("### 풀이 기록")
        # 가장 최근 문제 결과 표시
        last_q_idx, last_ans, last_res, last_exp = st.session_state.quiz_history[-1]
        st.markdown(f"**방금 문제:** {quiz_data[last_q_idx][0]}")
        st.markdown(f"**내 답:** {last_ans}")
        st.markdown(f"**결과:** {last_res}")
        st.markdown(last_exp)
        st.markdown("---")


if __name__ == "__main__":
    display_quiz()
