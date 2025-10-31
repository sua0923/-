import streamlit as st

# --- 정답 설정 ---
# 빈칸 채우기 정답 (대소문자 구분 없이 처리하기 위해 소문자로 저장)
FILL_IN_THE_BLANK_ANSWERS = {
    'A': '분수식',
    'B': '다항식',
    'C': '유리식',
    'D': '분모의 값'
}

# O/X 퀴즈 정답
OX_QUIZ_ANSWERS = {
    1: 'O',
    2: 'X',
    3: 'O'
}

# --- 전체 개념 설명 텍스트 (맨 처음에 표시됨) ---
FULL_CONCEPT_TEXT = """
# 고등 수학: I. 유리식과 무리식 - 유리식의 개념

## 1. 유리식이란 무엇일까요?

우리는 이미 숫자로 이루어진 분수 (1/2, 3/5)에 대해 잘 알고 있습니다. 유리식은 이러한 분수의 개념을 **'문자로 이루어진 식'**으로 확장한 것입니다.

**다항식**이란 x^2 + 3x - 1 또는 5y처럼 문자와 숫자의 곱으로 이루어진 항들의 합으로만 표현된 식을 말합니다.

유리식은 이 다항식을 사용하여 분수 형태로 나타내는 식을 의미하며, 크게 두 가지 종류로 나뉩니다.

---

### 핵심 개념 정리 (빈칸 채우기 대상)

1.  **분수식:**
    두 다항식 A와 B (B는 0이 아님)에 대하여, A/B 꼴로 나타낼 수 있는 식 중 **다항식이 아닌 식**을 **( A )** 이라고 합니다. (예: 1/x, (x-1)/(x^2+1))

2.  **유리식의 분류:**
    위에서 정의한 **( A )** 와 A, B를 다항식이라 할 때, B가 A의 약수가 되어 분수 형태가 사라지는 식(예: x+3)인 **( B )** 을 통틀어 **( C )** 이라고 부릅니다.

3.  **식의 성립 조건:**
    유리식의 값이 수학적으로 의미를 갖기 위해서는, 분모에 문자가 포함되어 있을 때 그 **( D )** 이 항상 **0이 아니어야** 합니다.

---
"""


def check_fill_in_the_blank_answers(answers):
    """빈칸 채우기 정답을 확인하고 결과를 반환합니다."""
    results = {}
    is_all_correct = True
    for key, correct_answer in FILL_IN_THE_BLANK_ANSWERS.items():
        user_answer = answers.get(key, '').strip().lower().replace(" ", "")
        correct_check = correct_answer.lower().replace(" ", "")
        
        if user_answer == correct_check:
            results[key] = (True, f"✅ 정답: **{correct_answer}**")
        else:
            results[key] = (False, f"❌ 오답입니다. 정답은 **{correct_answer}**입니다.")
            is_all_correct = False
    return results, is_all_correct

def check_ox_quiz_answers(answers):
    """O/X 퀴즈 정답을 확인하고 결과를 반환합니다."""
    results = {}
    is_all_correct = True
    for key, correct_answer in OX_QUIZ_ANSWERS.items():
        user_answer = answers.get(key)
        
        # 사용자가 아무것도 선택하지 않은 경우를 처리
        if user_answer is None:
            results[key] = (False, "❓ 답을 선택해주세요.")
            is_all_correct = False
        elif user_answer == correct_answer:
            results[key] = (True, f"✅ 정답입니다.")
        else:
            results[key] = (False, f"❌ 오답입니다.")
            is_all_correct = False
    return results, is_all_correct

# --- Streamlit 앱 본문 ---
st.set_page_config(layout="centered", page_title="유리식 개념 학습")
st.title("📚 고등 수학: 유리식 개념 및 퀴즈")
st.markdown("---")

# 1. 전체 개념 설명 (맨 처음에 표시)
st.markdown(FULL_CONCEPT_TEXT)

st.markdown("---")

# 2. 핵심 개념 정리 (빈칸 채우기)
st.header("📝 1단계: 핵심 개념 빈칸 채우기")
st.markdown("위 개념 설명을 참고하여 빈칸에 알맞은 단어를 채워보세요.")

# --- 빈칸 채우기 폼 ---
with st.form("fill_in_the_blank_form"):
    st.markdown("""
    - **( A )**
    - **( B )**
    - **( C )**
    - **( D )**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        ans_a = st.text_input("빈칸 ( A )", key='input_a', help="분모에 문자가 포함되어 다항식이 아닌 식")
        ans_b = st.text_input("빈칸 ( B )", key='input_b', help="분수 형태가 아닌, 순수한 문자와 숫자의 곱의 합")
    with col2:
        ans_c = st.text_input("빈칸 ( C )", key='input_c', help="분수식과 다항식을 통틀어 이르는 말")
        ans_d = st.text_input("빈칸 ( D )", key='input_d', help="0이 아니어야 하는 부분")
    
    submitted_fill = st.form_submit_button("빈칸 정답 및 해설 확인하기")

if submitted_fill:
    user_answers = {'A': ans_a, 'B': ans_b, 'C': ans_c, 'D': ans_d}
    results, all_correct = check_fill_in_the_blank_answers(user_answers)
    
    st.markdown("---")
    st.subheader("💡 빈칸 채우기 정답 및 해설")
    
    # 결과 및 해설 출력
    st.write(f"**( A )**: {results['A'][1]}")
    st.caption("✅ **해설:** 두 다항식의 비로 표현된 식 중 다항식이 아닌 것을 **분수식**이라고 합니다.")
    
    st.write(f"**( B )**: {results['B'][1]}")
    st.caption("✅ **해설:** 문자와 숫자의 곱으로 이루어진 항들의 합으로만 표현된 식을 **다항식**이라고 합니다.")
    
    st.write(f"**( C )**: {results['C'][1]}")
    st.caption("✅ **해설:** 분수식과 다항식을 모두 포함하는 가장 큰 개념이 **유리식**입니다.")
    
    st.write(f"**( D )**: {results['D'][1]}")
    st.caption("✅ **해설:** 유리식 $A/B$에서 $B$가 0이 되면 값이 정의되지 않으므로, **분모의 값**은 항상 0이 아니어야 합니다.")

    if all_correct:
        st.balloons()
        st.success("🎉 모든 빈칸을 완벽하게 채우셨습니다! 개념을 정확히 이해했네요.")
    else:
        st.error("아직 헷갈리는 부분이 있어요. 해설을 다시 확인하고 넘어가세요.")

st.markdown("---")

# 3. O/X 퀴즈 (개념 확인)
st.header("🎯 2단계: O/X 퀴즈 (개념 확인)")

# --- O/X 퀴즈 폼 ---
with st.form("ox_quiz_form"):
    st.markdown("""
    다음 문장이 옳으면 **O**, 틀리면 **X**를 선택하세요.
    """)
    
    ox1 = st.radio(
        "1. 다항식 `3x^2 - 2x + 5`는 유리식이다.", 
        ('O', 'X'), 
        key='ox_q1', 
        index=None
    )
    
    ox2 = st.radio(
        "2. 유리식 `(x+1)/(x-2)`에서 x=2일 때의 식의 값은 3이다.", 
        ('O', 'X'), 
        key='ox_q2', 
        index=None
    )
    
    ox3 = st.radio(
        "3. `x/y + y/x`는 유리식이다. (단, x는 0이 아니고, y는 0이 아니다)", 
        ('O', 'X'), 
        key='ox_q3', 
        index=None
    )
    
    submitted_ox = st.form_submit_button("O/X 정답 및 해설 확인하기")

if submitted_ox:
    user_answers = {1: ox1, 2: ox2, 3: ox3}
    results, all_correct = check_ox_quiz_answers(user_answers)
    
    st.markdown("---")
    st.subheader("💡 O/X 퀴즈 정답 및 해설")
    
    # 결과 출력 및 해설 추가
    st.write(f"**1. 다항식은 유리식이다. ->** {results[1][1]} **(정답: O)**")
    st.caption("✅ **해설:** 다항식은 분모가 1인 분수식으로 생각할 수 있으므로, 유리식에 포함되는 것이 맞습니다. (유리식 = 다항식 + 분수식)")

    st.write(f"**2. x=2일 때 (x+1)/(x-2)의 값은 3이다. ->** {results[2][1]} **(정답: X)**")
    st.caption("❌ **해설:** $x=2$를 대입하면 분모가 $2-2=0$이 되므로, 식의 값이 **정의되지 않습니다**. 분모는 항상 0이 아니어야 합니다.")
    
    st.write(f"**3. x/y + y/x는 유리식이다. ->** {results[3][1]} **(정답: O)**")
    st.caption("✅ **해설:** 유리식끼리의 덧셈과 뺄셈의 결과 역시 유리식입니다. 이를 통분하면 $(x^2 + y^2) / (xy)$ 꼴이 되며, 이는 유리식의 정의를 만족합니다.")
    
    if all_correct:
        st.success("💯 O/X 퀴즈도 모두 맞혔습니다! 완벽해요!")
    else:
        st.warning("일부 오답이 있습니다. 해설을 통해 틀린 부분을 확인하고 넘어가세요.")

st.markdown("---")
st.markdown("##### 💡 다음 학습 내용: 유리식은 분수와 마찬가지로 약분하거나 통분하여 더하거나 뺄 수 있습니다. 다음에는 유리식의 사칙연산을 학습해 봅시다.")
