import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 🎨 Streamlit 페이지 설정
st.set_page_config(
    page_title="이차함수 그래프 기본형 분석",
    layout="centered"
)

## 📌 이차함수 그래프 기본형 (y=ax^2) 분석하기

st.title('이차함수 그래프 기본형 ($y=ax^2$) 분석하기')

# ---

### 계수 'a' 값 선택 위젯

st.header('1. 계수 $a$ 값 선택')

# a 값 조절을 위한 슬라이더 생성. 0은 제외하도록 min_value, max_value, step 설정
# a가 0일 때 오류를 피하기 위해, 0 근처에서 'a'가 0이 아닌 값을 선택하게 유도
a = st.slider(
    '계수 $a$ 값 (0 제외)',
    min_value=-5.0,  # 최소값
    max_value=5.0,   # 최대값
    value=1.0,       # 기본값
    step=0.1,        # 단계
    format='%.1f'    # 소수점 한 자리 표시
)

# a가 0인 경우 경고 메시지 표시
if abs(a) < 0.05: # a가 거의 0에 가까우면 0으로 간주하고 경고
    st.warning("경고! 계수 $a$는 0이 될 수 없습니다. $y=0$은 이차함수가 아닙니다.")
    # 그래프를 그릴 때 오류를 피하기 위해 작은 값으로 대체 (시각적 피드백)
    a = 0.001 if a >= 0 else -0.001 


st.markdown(f"**선택된 이차함수:** $\mathbf{{y = {a:.1f}x^2}}$")

# ---

### 그래프 그리기

st.header('2. 그래프 시각화')

# x 범위 설정 (예: -5부터 5까지)
x = np.linspace(-5, 5, 400)
# y = ax^2 계산
y = a * (x**2)

# Matplotlib으로 그래프 생성
fig, ax = plt.subplots(figsize=(8, 6))

# 그래프 그리기
ax.plot(x, y, label=f'$y = {a:.1f}x^2$', color='blue')

# 축 설정
ax.set_title(f'이차함수 그래프: $y = {a:.1f}x^2$')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')

# x축과 y축이 0을 포함하도록 설정
ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax.axvline(0, color='gray', linewidth=0.8, linestyle='--')

# 축 범위 설정 (y축은 a값의 변화를 잘 보여주기 위해 -25부터 25까지 설정)
ax.set_xlim([-5, 5])
ax.set_ylim([-25, 25])
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper center')
ax.set_aspect('equal', adjustable='box') # 그래프의 비율을 맞춤

# Streamlit에 그래프 표시
st.pyplot(fig)

# ---

### 그래프 분석 및 추론 💡

st.header('3. $a$ 값에 따른 그래프 특징 분석')

st.markdown("슬라이더를 움직여 $a$ 값을 바꿔가며 그래프의 모양을 관찰하고 아래 내용을 확인하세요.")

if a > 0.05:
    # a가 양수일 때
    st.success(f"✅ **$a = {a:.1f}$ (양수):** 그래프는 **아래로 볼록**하며, 꼭짓점은 원점 (0, 0)입니다.")
    st.markdown(" ($x=0$ 일 때 최솟값 $y=0$을 가집니다.)")
elif a < -0.05:
    # a가 음수일 때
    st.error(f"❌ **$a = {a:.1f}$ (음수):** 그래프는 **위로 볼록**하며, 꼭짓점은 원점 (0, 0)입니다.")
    st.markdown(" ($x=0$ 일 때 최댓값 $y=0$을 가집니다.)")


st.markdown("---")

# 폭 분석
abs_a = abs(a)
st.subheader('**$|a|$ 값과 그래프의 폭**')

st.markdown(f"현재 $|a| = |{a:.1f}| = **{abs_a:.1f}**$ 입니다.")

if abs_a > 1.5:
    st.info("🔥 $\mathbf{|a|}$의 값이 **클수록** ($\mathbf{|a|>1}$), 그래프는 **y축에 가까워져 폭이 좁아집니다**.")
elif abs_a < 0.5:
    st.warning("💧 $\mathbf{|a|}$의 값이 **작을수록** ($\mathbf{0<|a|<1}$), 그래프는 **x축에 가까워져 폭이 넓어집니다**.")
else:
    st.info("✨ $\mathbf{|a|}$의 값이 중간 정도이므로, 폭은 적당합니다.")

st.markdown(
    """
    * **핵심 정리:** $|a|$가 **1보다 크면** 폭이 좁고, **1보다 작으면** 폭이 넓어집니다.
    """
)
