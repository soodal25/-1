import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm

if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0.0
if 'total_elapsed_sec' not in st.session_state:
    st.session_state.total_elapsed_sec = 0.0

def start_stop_timer():
    if st.session_state.running:
        st.session_state.running = False
        duration = time.time() - st.session_state.start_time
        st.session_state.total_elapsed_sec += duration
    else:
        st.session_state.running = True
        st.session_state.start_time = time.time()

def reset_timer():
    st.session_state.running = False
    st.session_state.total_elapsed_sec = 0.0
    st.session_state.start_time = 0.0

st.title("수학과 코딩을 결합한 스터디 플래너")
st.markdown("---")

daily_goal = st.text_input("일일 목표 공부량을 입력하세요 (분):", value="60")
try:
    goal = int(daily_goal)
    goal_sec = 60 * goal
    st.info(f"오늘의 목표 공부 시간은 **{goal}분**입니다.")
except ValueError:
    st.error("목표 시간은 숫자로 입력해 주세요.")
    goal_sec = 0 # [수정] 변수 이름 goal_sec으로 통일

col1, col2 = st.columns(2)

button_label = "일시 정지 ⏸️" if st.session_state.running else "공부 시작/재개 ▶️"
col1.button(button_label, on_click=start_stop_timer)
col2.button("종료 및 초기화 🔄", on_click=reset_timer)

if st.session_state.running:
    current_elapsed = st.session_state.total_elapsed_sec + (time.time() - st.session_state.start_time)
    time.sleep(1)
    st.rerun() # [수정] st.experimental_rerun() -> st.rerun()
else:
    current_elapsed = st.session_state.total_elapsed_sec

elapsed_sec = int(current_elapsed)
minutes = elapsed_sec // 60
seconds = elapsed_sec % 60

st.subheader(f"총 공부 시간: {minutes}분 {seconds}초")
st.markdown("---")

if goal_sec > 0:
    try:
        result = (elapsed_sec * 100) / goal_sec
        st_result = round(result, 2)

        if elapsed_sec >= goal_sec:
            st.balloons()
            st.success("🎉 목표 달성! 축하해요!! :)")
        else:
            st.warning(f"아쉽지만 목표를 달성하지 못했어요ㅠㅠ 목표 달성률은 **{st_result}%**에요.")

        # 4. 그래프 생성 및 표시 (st.pyplot 사용)
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        # --- [수정] 폰트 설정 부분: GitHub 파일 이름을 사용합니다. ---
        font_path = 'MALGUN.TTF'  # GitHub에 올린 폰트 파일 이름
        try:
            fontprop = fm.FontProperties(fname=font_path)
            mpl.rc('font', family=fontprop.get_name())
            mpl.rcParams['axes.unicode_minus'] = False
 
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
            startangle=90
        )
        axs[0].set_title("공부 목표 달성률")
        axs[0].axis('equal')
        
        with st.sidebar:
            st.header("과목별 비율 설정")
            subjects = st.number_input("오늘 공부할 과목의 수를 입력하세요:", min_value=1, value=1, step=1, key="num_subjects")

            labels2 = []
            sizes2 = []

            for i in range(subjects):
                col_name, col_percent = st.columns(2)
                # key가 중복되지 않도록 session_state를 사용하거나 고유 키를 만듭니다.
                subject_name = col_name.text_input(f"{i+1}번째 과목 이름:", key=f"subj_name_{i}")
                percent = col_percent.number_input(f"비율(%) 입력:", min_value=0.0, max_value=100.0, step=0.1, key=f"subj_percent_{i}")

                if subject_name and percent > 0:
                    labels2.append(subject_name)
                    sizes2.append(percent)

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
                startangle=90
            )
            axs[1].set_title("과목별 공부 시간 비율")
            axs[1].axis('equal')
        else:
             axs[1].set_title("과목 비율 정보를 입력하세요.")

        plt.tight_layout()
        st.pyplot(fig)

    except ZeroDivisionError:
        st.error("목표 시간을 1분 이상으로 설정해주세요.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

