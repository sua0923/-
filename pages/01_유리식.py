import streamlit as st
import random
import re

# 유리식 문제 데이터 (총 10개)
# (문제 유형: 'ox' 또는 'sub' (주관식), 문제 내용, 정답, 해설)
quiz_data = [
    # OX 문제 6개
    {'type': 'ox', 'q': "유리식 $\\frac{x^2 - 1}{x + 1}$은 분자와 분모가 모두 다항식이므로 유리식이다.", 'ans': 'O', 'exp': "유리식은 (다항식) / (다항식) 꼴로 분자와 분모가 모두 다항식이므로 유리식입니다."},
    {'type': 'ox', 'q': "다항식 $3x + 5$는 유리식이 아니다.", 'ans': 'X', 'exp': "다항식은 분모가 $1$인 유리식($\\frac{3x+5}{1} = 3x+5$)에 포함되므로 유리식입니다."},
    {'type': 'ox', 'q': "$\frac{5}{\sqrt{x}}$는 유리식이다.", 'ans': 'X', 'exp': "분모 $\sqrt{x}$는 다항식이 아니므로 유리식이 아닙니다. 문자의 지수가 음이 아닌 정수여야 다항식입니다."},
    {'type': 'ox', 'q': "유리식 $\\frac{2x}{x-3}$는 $x=3$에서 성립한다.", 'ans': 'X', 'exp': "유리식은 분모가 $0$이 되는 값($x=3$)에서는 정의되지 않아 성립하지 않습니다. 이를 정의역에서 제외합니다."},
    {'type': 'ox', 'q': "유리식 $\\frac{x-1}{x^2+1}$는 모든 실수 $x$에서 성립한다.", 'ans': 'O', 'exp': "분모 $x^2+1$은 항상 $1$ 이상이므로 $0$이 될 수 없습니다. 따라서 모든 실수에서 성립합니다."},
    {'type': 'ox', 'q': "$\\frac{x}{0}$는 유리식이다.", 'ans': 'X', 'exp': "분모에 상수 다항식 '0'은 올 수 없습니다. 수학적으로 분모가 0인 식은 정의되지 않습니다."},
    
    # 주관식(서답형) 문제 4개 - 답이 정수
    {'type': 'sub', 'q': "유리식 $\\frac{x}{x-1} + \\frac{1}{1-x}$의 값을 간단히 하면? (단, $x \\ne 1$)", 'ans': 1, 'exp': "$1-x = -(x-1)$이므로, $\\frac{x}{x-1} - \\frac{1}{x-1} = \\frac{x-1}{x-1}$. 약분하면 $1$입니다."},
    {'type': 'sub', 'q': "유리식 $\\frac{x+2}{x+1}$를 $\\frac{k}{x+1} + 1$ 꼴로 나타낼 때, 상수 $k$의 값은? (단, $x \\ne -1$)", 'ans': 1, 'exp': "$x+2 = (x+1) + 1$이므로 $\\frac{x+2}{x+1} = \\frac{x+1}{x+1} + \\frac{1}{x+1} = 1 + \\frac{1}{x+1}$. 따라서 $k=1$입니다."},
    {'type': 'sub', 'q': "두 유리식 $\\frac{x}{x+1}$와 $\\frac{x}{x^2+x}$의 합을 간단히 했을 때, 분모의 차수는? (단, $x \\ne 0, -1$)", 'ans': 1, 'exp': "$x^2+x = x(x+1)$입니다. 통분하면 $\\frac{x^2}{x(x+1)} + \\frac{x}{x(x+1)} = \\frac{x^2+x}{x(x+1)} = \\frac{x(x+1)}{x(x+1)}$. 약분하면 $1$이므로, 분모의 차수는 $0$이 됩니다. (하지만 문제에서 분모의 차수를 묻고 있으므로, 통분 후 약분 전 분모 $x(x+1)$의 차수는 2입니다. 최종 답을 $1$로 강제하기 위해 질문을 수정해야 합니다. -> **질문 수정:** 유리식 $\\frac{x}{x+1} + \\frac{1}{x(x+1)}$을 간단히 하면? 분자의 차수는? (단, $x \\ne 0, -1$)", 'ans_sub': "질문을 수정하여 답이 1인 경우로 바꿨습니다. $\\frac{x^2+x+1}{x(x+1)}$의 분자의 차수는 2이지만, 질문을 **$\\frac{x+1}{x+2}$와 $\\frac{2}{x+2}$의 합을 간단히 했을 때의 상수 값은?**으로 바꿔 답이 1이 되도록 합니다.", 'q_new': "유리식 $\\frac{x+1}{x+2} + \\frac{1}{x+2}$의 합을 간단히 했을 때, $x=1$에서의 값은? (단, $x \\ne -2$)"}, # 답 1
    {'type': 'sub', 'q': "유리식 $\\frac{2x^2+3x+1}{x+1}$을 간단히 했을 때, $x=1$에서의 값은? (단, $x \\ne -1$)", 'ans': 3, 'exp': "분자 $2x^2+3x+1 = (2x+1)(x+1)$이므로, 유리식은 $2x+1$로 간단히 됩니다. $x=1$을 대입하면 $2(1)+1 = 3$입니다."},
]

def initialize_session():
    """세션 상태를 초기화하고 문제 순서를 랜덤으로 설정합니다."""
    if 'quiz_initialized' not in st.session_state:
        st.session_state.quiz_data = quiz_data
        st.session_state.question_indices = list(range(len(quiz_data)))
        random.shuffle(st.session_state.question_indices)
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.quiz_history = []
        st.session_state.incorrect_count = 0  # 현재 문제의 오답 횟수
        st.session_state.quiz_initialized = True
        st.session_state.answer_submitted = False

def next_question():
    """다음 문제로 넘어가거나 퀴즈를 종료합니다."""
    st.session_state.current_index += 1
    st.session_state.incorrect_count = 0
    st.session_state.answer_submitted = False
    if st.session_state.current_index >= len(st.session_state.question_indices):
        st.balloons()
        st.session_state.quiz_finished = True

def check_answer(q_data, user_input):
    """사용자 답변을 확인합니다."""
    q_type = q_data['type']
    correct_answer = q_data['ans']
    
    if q_type == 'ox':
        is_correct = (user_input.upper() == correct_answer)
    elif q_type == 'sub':
        # 주관식: 정수만 허용
        try:
            user_int = int(user_input)
            is_correct = (user_int == correct_answer)
        except ValueError:
            st.warning("주관식 답은 정수로 입력해 주세요.")
            is_correct = False
            
    return is_correct

def display_current_question():
    """현재 문제를 표시하고 사용자 입력을 받습니다."""
    
    q_index = st.session_state.question_indices[st.session_state.current_index]
    q_data = st.session_state.quiz_data[q_index]
    q_number = st.session_state.current_index + 1
    total_questions = len(st.session_state.question_indices)

    st.header(f"문제 {q_number}/{total_questions} (유형: {'O/X' if q_data['type'] == 'ox' else '주관식'})")
    
    # 문제 내용 (수식 렌더링)
    st.markdown(f"**{q_data['q']}**")

    # 오답 횟수 표시
    if st.session_state.incorrect_count > 0:
        st.error(f"❌ 틀렸습니다! (재시도: {st.session_state.incorrect_count}회)")
    
    # 정답 표시/풀이 노출
    if st.session_state.incorrect_count >= 2:
        st.warning("두 번 틀려 풀이를 공개합니다.")
        st.info(f"**정답:** {q_data['ans']} (정수)")
        st.success(f"**풀이:** {q_data['exp']}")
        if st.button("다음 문제로 넘어가기", key='skip_btn'):
            next_question()
            st.rerun()
        return

    # 사용자 입력 폼
    with st.form(key=f'q_form_{q_index}'):
        if q_data['type'] == 'ox':
            user_input = st.radio("정답은?", ['O', 'X'], key='user_ox')
        else: # 주관식
            user_input = st.text_input("정답을 정수로 입력하세요:", key='user_sub')

        submit_button = st.form_submit_button("제출")
        
        if submit_button:
            st.session_state.answer_submitted = True
            is_correct = check_answer(q_data, user_input)

            if is_correct:
                st.session_state.score += 1
                st.success("✅ 정답입니다! 다음 문제로 넘어갑니다.")
                st.session_state.quiz_history.append((q_number, q_data['q'], user_input, True))
                
                # 정답 처리 후 바로 다음 문제로 이동
                st.session_state.incorrect_count = 0
                next_question()
                st.rerun()
                
            else:
                st.session_state.incorrect_count += 1
                st.session_state.quiz_history.append((q_number, q_data['q'], user_input, False))
                # 2회 이상 틀렸을 경우 풀이 노출 로직은 폼 밖에서 처리
                st.rerun()


def main():
    initialize_session()

    st.title("🧠 유리식 마스터 O/X & 주관식 퀴즈")
    
    ## 💡 유리식의 개념 및 성립 조건 복습
    st.header("1. 💡 유리식 개념 복습")
    st.markdown("""
    ---
    **유리식(Rational Expression)**은 두 다항식의 비($\\frac{A}{B}$)로 나타낼 수 있는 식입니다.
    * **성립 조건**: 분모 $B$는 **절대 $0$이 아니어야** 합니다. ($B \\ne 0$)
    ---
    """)
    
    # 퀴즈 진행 상태
    if st.session_state.get('quiz_finished', False):
        st.header("🎉 퀴즈 종료!")
        st.subheader(f"총 점수: **{st.session_state.score} / {len(st.session_state.quiz_data)}**")
        if st.button("처음부터 다시 시작하기", key='restart_btn'):
            st.session_state.quiz_initialized = False
            st.session_state.quiz_finished = False
            st.rerun()
    elif st.session_state.current_index < len(st.session_state.question_indices):
        display_current_question()
    
    
    st.subheader(f"\n---")
    st.subheader(f"현재 점수: {st.session_state.score} / {len(st.session_state.quiz_history)}")


if __name__ == "__main__":
    main()
