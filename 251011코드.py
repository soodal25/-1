import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import platform
import matplotlib.font_manager as fm
from matplotlib import rc

# -------------------------------
# ✅ 폰트 설정 (한글 깨짐 방지 핵심 부분)
# -------------------------------
font_path = os.path.join(os.path.dirname(__file__), "custom_fonts", "MALGUN.TTF")

if os.path.exists(font_path):
    try:
        fm.fontManager.addfont(font_path)  # matplotlib에 폰트 등록
        font_prop = fm.FontProperties(fname=font_path, size=12)
        font_name = font_prop.get_name()

        plt.rcParams['font.family'] = font_name
        plt.rcParams['font.sans-serif'] = [font_name]
        plt.rcParams['axes.unicode_minus'] = False

        print(f"✅ 폰트 등록 성공: {font_name}")
    except Exception as e:
        print("❌ 폰트 등록 실패:", e)
        font_prop = None
else:
    print("⚠️ 폰트 파일을 찾을 수 없습니다:", font_path)
    font_prop = None

# -------------------------------
# ✅ Streamlit 상태 관리
# -------------------------------
if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0.0
if 'total_elapsed_sec' not in st.session_state:
    st.session_state.total_elapsed_sec = 0.0

# -------------------------------
# ✅ 타이머 제어 함수
# -------------------------------
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

# -------------------------------
# ✅ UI 구성
# -------------------------------
st.title("📘 수학과 코딩을 결합한 스터디 플래너")
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

st.subheader(f"⏰ 총 공부 시간: {minutes}분 {seconds}초")
st.markdown("---")

# -------------------------------
# ✅ 목표 달성률 계산 및 시각화
# -------------------------------
if goal_sec > 0:
    try:
        result = (elapsed_sec * 100) / goal_sec
        st_result = round(result, 2)

        if elapsed_sec >= goal_sec:
            st.balloons()
            st.success("🎉 목표 달성! 축하해요!! :)")
        else:
            st.warning(f"아쉽지만 목표를 달성하지 못했어요ㅠㅠ 목표 달성률은 **{st_result}%**에요.")

        # -------------------------------
        # ✅ 그래프 생성
        # -------------------------------
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        # 첫 번째 파이차트 - 공부 목표 달성률
        labels1 = ['총 공부 시간', '남은 목표 시간']
        sizes1 = [st_result, max(0, 100 - st_result)]

        def make_pumpkin(labels):
            def my_pumpkin(pct):
                total = sum(sizes1)
                value = pct * total / 100.0
                label = labels[my_pumpkin.index]
                my_pumpkin.index += 1
                return f"{label}\n{value:.1f}%"
            my_pumpkin.index = 0
            return my_pumpkin

        axs[0].pie(
            sizes1,
            labels=labels1,
            autopct=make_pumpkin(labels1),
            startangle=90,
            textprops={'fontproperties': font_prop} if font_prop else {}
        )
        axs[0].set_title("공부 목표 달성률", fontproperties=font_prop if font_prop else None)
        axs[0].axis('equal')

        # -------------------------------
        # ✅ 사이드바 - 과목별 비율 입력
        # -------------------------------
        with st.sidebar:
            st.header("📚 과목별 비율 설정")
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

        # 두 번째 파이차트 - 과목별 비율
        if sum(sizes2) > 0:
            def make_potato(labels):
                def my_potato(pct):
                    total = sum(sizes2)
                    value = pct * total / 100.0
                    label = labels[my_potato.index]
                    my_potato.index += 1
                    return f"{label}\n{value:.1f}%"
                my_potato.index = 0
                return my_potato

            axs[1].pie(
                sizes2,
                labels=labels2,
                autopct=make_potato(labels2),
                startangle=90,
                textprops={'fontproperties': font_prop} if font_prop else {}
            )
            axs[1].set_title("과목별 공부 시간 비율", fontproperties=font_prop if font_prop else None)
            axs[1].axis('equal')
        else:
            axs[1].set_title("과목 비율 정보를 입력하세요.", fontproperties=font_prop if font_prop else None)

        plt.tight_layout()
        st.pyplot(fig)

    except ZeroDivisionError:
        st.error("목표 시간이 0분입니다.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")



