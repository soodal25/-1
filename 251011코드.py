import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import platform

# --------------------------------------------------
# ✅ 폰트 설정 (모든 플랫폼 대응, 한글 깨짐 완전 방지)
# --------------------------------------------------
font_candidates = [
    "C:/Windows/Fonts/malgun.ttf",  # Windows (맑은 고딕)
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux (나눔고딕)
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
]

font_path = None
for path in font_candidates:
    if os.path.exists(path):
        font_path = path
        break

if font_path:
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams["font.family"] = font_name
    plt.rcParams["axes.unicode_minus"] = False
else:
    st.warning("⚠️ 한글 폰트를 찾지 못했습니다. 기본 폰트로 표시됩니다.")

# --------------------------------------------------
# ✅ 세션 상태 관리
# --------------------------------------------------
if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0.0
if 'total_elapsed_sec' not in st.session_state:
    st.session_state.total_elapsed_sec = 0.0

# --------------------------------------------------
# ✅ 함수 정의
# --------------------------------------------------
def start_stop_timer():
    try:
        current_goal_sec = int(st.session_state.daily_goal) * 60 if 'daily_goal' in st.session_state else 0
    except ValueError:
        current_goal_sec = 0
        
    if st.session_state.running:
        st.session_state.running = False
        duration = time.time() - st.session_state.start_time
        st.session_state.total_elapsed_sec += duration
    else:
        if current_goal_sec <= 0:
            st.warning("먼저 목표 시간을 1분 이상으로 설정해주세요.")
            return
        st.session_state.running = True
        st.session_state.start_time = time.time()

def reset_timer():
    st.session_state.running = False
    st.session_state.total_elapsed_sec = 0.0
    st.session_state.start_time = 0.0

# --------------------------------------------------
# ✅ UI 구성
# --------------------------------------------------
st.title("수학과 코딩을 결합한 스터디 플래너")
st.markdown("---")

daily_goal = st.text_input("일일 목표 공부량을 입력하세요 (분):", value="60", key='daily_goal')
try:
    goal = int(daily_goal)
    goal_sec = 60 * goal
    st.info(f"오늘의 목표 공부 시간은 **{goal}분**입니다.")
except ValueError:
    st.error("목표 시간은 숫자로 입력해 주세요.")
    goal_sec = 0

col1, col2 = st.columns(2)
button_label = "일시 정지 ⏸" if st.session_state.running else "공부 시작/재개 ▶"
col1.button(button_label, on_click=start_stop_timer)
col2.button("종료 및 초기화 🔄", on_click=reset_timer)

if st.session_state.running:
    current_elapsed = st.session_state.total_elapsed_sec + (time.time() - st.session_state.start_time)
    time.sleep(1)
    st.rerun()
else:
    current_elapsed = st.session_state.total_elapsed_sec

elapsed_sec = int(current_elapsed)
minutes = elapsed_sec // 60
seconds = elapsed_sec % 60

st.subheader(f"총 공부 시간: {minutes}분 {seconds}초")
st.markdown("---")

# --------------------------------------------------
# ✅ 목표 달성률 계산 및 시각화
# --------------------------------------------------
if goal_sec > 0:
    try:
        result = (elapsed_sec * 100) / goal_sec
        st_result = round(result, 2)

        if elapsed_sec >= goal_sec:
            st.balloons()
            st.success("🎉 목표 달성! 축하해요!! :)")
        else:
            st.warning(f"아쉽지만 목표를 달성하지 못했어요ㅠㅠ 목표 달성률은 **{st_result}%**에요.")

        # ✅ 그래프 생성
        title_font = fm.FontProperties(fname=font_path, weight='bold')
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        # (1) 공부 목표 달성률
        labels1 = ['총 공부 시간', '남은 목표 시간']
        sizes1 = [st_result, max(0, 100 - st_result)]

        wedges1, texts1, autotexts1 = axs[0].pie(
            sizes1,
            labels=labels1,
            autopct="%1.1f%%",
            startangle=90,
            textprops={'fontproperties': fm.FontProperties(fname=font_path) if font_path else None}
        )
        axs[0].set_title(
    "목표 달성률",
    fontproperties=title_font,
    fontsize=24,   # 크게
    pad=25         # 여백 살짝
)
        axs[0].axis('equal')

        # ✅ 사이드바 과목 비율 입력
        with st.sidebar:
            st.header("과목별 비율 설정")
            subjects = st.number_input("오늘 공부할 과목의 수를 입력하세요:", min_value=1, value=1, step=1, key="num_subjects")

            labels2 = []
            sizes2 = []

            for i in range(subjects):
                col_name, col_percent = st.columns(2)
                subject_name = col_name.text_input(f"{i+1}번째 과목 이름:", key=f"subj_name_{i}")
                percent = col_percent.number_input(f"비율(%) 입력:", min_value=0.0, max_value=100.0, step=0.1, key=f"subj_percent_{i}")

                if subject_name and percent > 0:
                    labels2.append(subject_name)
                    sizes2.append(percent)

        # (2) 과목별 비율 파이차트
if sum(sizes2) > 0:
    # 색상 먼저 정의 (if 안쪽이지만 pie 전에)
    colors_goal = ["#B2CCFF", "#FAED7D"]

    wedges2, texts2, autotexts2 = axs[1].pie(
        sizes2,
        labels=labels2,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors_goal,  # ← 여기 색상 적용
        textprops={'fontproperties': fm.FontProperties(fname=font_path) if font_path else None}
    )

    axs[1].set_title(
        "과목별 공부 비율",
        fontproperties=title_font,
        fontsize=24,
        pad=25
    )
    axs[1].axis('equal')

        else:
            axs[1].set_title("과목 비율 정보를 입력하세요.", fontproperties=fm.FontProperties(fname=font_path) if font_path else None)

        plt.tight_layout()
        st.pyplot(fig)

    except ZeroDivisionError:
        st.error("목표 시간이 0분입니다.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")







