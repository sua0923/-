import streamlit as st
import random

# --- 최근 당첨 번호 설정 (2025년 10월 25일, 1195회차 기준) ---
# 실제로 당첨 번호는 매주 변경되므로, 사용자가 직접 최신 정보를 업데이트해야 합니다.
# 보너스 번호는 2등 비교를 위해 따로 지정합니다.
RECENT_WINNING_NUMBERS = [3, 15, 27, 33, 34, 36]
BONUS_NUMBER = 37

def generate_numbers(num_sets):
    """
    1부터 45 사이의 숫자 중 6개를 무작위로 추출하여 원하는 세트 수만큼 반환합니다.
    """
    results = []
    for _ in range(num_sets):
        # 1부터 45까지의 숫자 중 6개를 중복 없이 무작위로 선택하고 정렬합니다.
        numbers = sorted(random.sample(range(1, 46), 6))
        results.append(numbers)
    return results

def compare_numbers(my_numbers, winning_numbers, bonus_number):
    """
    내가 생성한 번호와 당첨 번호를 비교하여 일치 개수를 반환합니다.
    """
    # 집합(set)을 사용해 교집합(일치하는 번호)의 개수를 쉽게 구합니다.
    my_set = set(my_numbers)
    winning_set = set(winning_numbers)

    # 1. 일반 번호 일치 개수
    matches = len(my_set.intersection(winning_set))

    # 2. 보너스 번호 일치 여부
    bonus_match = bonus_number in my_set

    return matches, bonus_match

# --- Streamlit 앱 인터페이스 설정 ---
st.title("🎲 랜덤 숫자 6개 생성 및 비교기")
st.markdown("1부터 45 사이의 숫자 중 **6개의 무작위 숫자**를 생성하고, 최근 추첨 번호와 비교합니다.")

# 최근 당첨 번호 표시
st.subheader("최근 추첨 번호 (1195회 기준)")
winning_numbers_str = ", ".join(map(str, RECENT_WINNING_NUMBERS))
st.info(f"**일반 번호**: {winning_numbers_str} | **보너스 번호**: {BONUS_NUMBER}")
st.write("*(참고: 이 번호는 2025년 10월 25일 1195회차 당첨 정보입니다. 실제 사용 시 최신 정보로 업데이트해주세요.)*")

st.markdown("---")

# 사용자로부터 생성할 세트 수를 입력받습니다.
num_sets = st.slider(
    '몇 세트의 숫자를 생성하시겠어요?',
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

# 생성 버튼
if st.button('✨ 랜덤 숫자 생성 및 비교'):
    # 숫자를 생성합니다.
    random_numbers = generate_numbers(num_sets)

    st.subheader(f"✅ 생성 결과 및 비교 ({num_sets} 세트)")

    # 생성된 숫자를 화면에 표시하고 비교 결과를 보여줍니다.
    for i, numbers in enumerate(random_numbers, 1):
        numbers_str = ", ".join(map(str, numbers))
        
        # 비교 함수 실행
        matches, bonus_match = compare_numbers(numbers, RECENT_WINNING_NUMBERS, BONUS_NUMBER)
        
        # 결과 표시
        st.write(f"**세트 {i}:** {numbers_str}")
        
        comparison_result = f"**일치 개수**: **{matches}**개"
        if matches == 5 and bonus_match:
            comparison_result += " (보너스 번호 일치!)"
        elif matches < 6 and matches >= 3:
             comparison_result += " (3~5개 일치)"
        elif matches == 6:
             comparison_result += " (6개 일치!)"

        if matches >= 3:
            st.success(comparison_result)
        else:
            st.warning(comparison_result)
        
        st.markdown("---")
