import streamlit as st
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

FONT_FILENAME = "GOWUNDODUM-REGULAR.TTF" 
font_path = os.path.join(os.path.dirname(__file__), FONT_FILENAME)

try:
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"폰트 파일 '{FONT_FILENAME}'을 코드 폴더에서 찾을 수 없습니다. 파일을 같은 폴더에 놓아주세요.")

    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)
    mpl.rcParams['axes.unicode_minus'] = False
    st.sidebar.success(f"✔️ {font_name} 폰트 적용 완료.")

except FileNotFoundError as e:
    try:
        font_path_auto = fm.findfont('NanumGothic', fallback_to_default=False)
        font_name_auto = fm.FontProperties(fname=font_path_auto).get_name()
        plt.rc('font', family=font_name_auto)
        mpl.rcParams['axes.unicode_minus'] = False
        st.sidebar.error(f"❌ 폰트 오류: {e}")
        st.sidebar.warning(f"⚠️ 시스템 폰트 {font_name_auto}로 대체됩니다.")
    except:
        plt.rc('font', family='sans-serif')
        mpl.rcParams['axes.unicode_minus'] = False
        st.sidebar.error("❌ 모든 폰트 로드 실패. 그래프 한글이 깨질 수 있습니다.")

except Exception:
    plt.rc('font', family='sans-serif')
    mpl.rcParams['axes.unicode_minus'] = False
    st.sidebar.warning("⚠️ 경고: 폰트 로드 중 예기치 않은 오류 발생. 기본 폰트로 대체됩니다.")
        
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0.0
if 'total_elapsed_sec' not in st.session_state:
    st.session_state.total_elapsed_sec = 0.0
if 'subject_times' not in st.session_state:
    st.session_state.subject_times = {} 
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = None
if 'notified_subjects' not in st.session_state:
    st.session_state.notified_subjects = set()
if 'goal_sec' not in st.session_state:
    st.session_state.goal_sec = 0
if 'labels2' not in st.session_state:
    st.session_state.labels2 = []
if 'sizes2' not in st.session_state:
    st.session_state.sizes2 = []

def update_subject_time(time_spent):
    if st.session_state.current_subject:
        subj = st.session_state.current_subject
        st.session_state.subject_times[subj] = st.session_state.subject_times.get(subj, 0.0) + time_spent

def start_stop_timer():
    selected_subject = st.session_state.subject_selector

    if st.session_state.is_running:
        time_spent = time.time() - st.session_state.start_time
        
        update_subject_time(time_spent)
        st.session_state.total_elapsed_sec += time_spent
        
        st.session_state.is_running = False
        st.session_state.current_subject = None
    else:
        if not selected_subject or selected_subject == "(과목 선택)":
             st.warning("공부를 시작하려면 먼저 과목을 선택해주세요.")
             return
             
        st.session_state.is_running = True
        st.session_state.start_time = time.time()
        st.session_state.current_subject = selected_subject

def reset_timer():
    st.session_state.is_running = False
    st.session_state.start_time = 0.0
    st.session_state.notified_subjects = set()
    st.session_state.total_elapsed_sec = 0.0
    st.session_state.subject_times = {} 
    st.session_state.current_subject = None
    st.session_state.goal_sec = 0
    st.session_state.labels2 = []
    st.session_state.sizes2 = []
