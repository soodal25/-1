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


daily_goal = st.text_input("일일 목표 공부량을 입력하세요 (분):", value="60")
try:
    goal = int(daily_goal)
    goal_sec = 60 * goal
    st.info(f"오늘의 목표 공부 시간은 **{goal}분**입니다.")
except ValueError:
    st.error("목표 시간은 숫자로 입력해 주세요.")
    goal_se= 0c 

col1, col2 = st.columns(2)

button_label = "일시 정지 ⏸️" if st.session_state.running else "공부 시작/재개 ▶️"
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
seconds = elapsed_sec % 60요.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
