import streamlit as st
import time
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.pyplot as plt

if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'paused_duration' not in st.session_state:
    st.session_state.paused_duration = 0.0
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0.0
if 'notified_subjects' not in st.session_state:
    st.session_state.notified_subjects = set()
if 'total_elapsed_sec' not in st.session_state:
    st.session_state.total_elapsed_sec = 0.0
if 'goal_sec' not in st.session_state:
    st.session_state.goal_sec = 0
if 'labels2' not in st.session_state:
    st.session_state.labels2 = []
if 'sizes2' not in st.session_state:
    st.session_state.sizes2 = []

try:
    # 맑은 고딕 시도 (로컬 Windows 환경용)
    font_path = "C:/Windows/Fonts/malgun.ttf"
    fontprop = fm.FontProperties(fname=font_path)
    mpl.rc('font', family=fontprop.get_name())
except Exception:
    # 폰트 로딩 실패 시 기본 Sans-serif 설정
    mpl.rc('font', family='sans-serif')
    # st.sidebar.warning("경고: 폰트 설정 오류. 한글이 깨질 수 있습니다.")
finally:
    mpl.rcParams['axes.unicode_minus'] = False

def start_stop_timer():
    if st.session_state.is_running:
        st.session_state.is_running = False
        st.session_state.paused_duration = st.session_state.total_elapsed_sec
    else:
        st.session_state.is_running = True
        st.session_state.start_time = time.time()

def reset_timer():
    st.session_state.is_running = False
    st.session_state.paused_duration = 0.0
    st.session_state.start_time = 0.0
    st.session_state.notified_subjects = set()
    st.session_state.total_elapsed_sec = 0.0
    st.session_state.goal_sec = 0
    st.session_state.labels2 = []
    st.session_state.sizes2 = []

st.title("📚 수학적 스터디 플래너 (Streamlit)")
st.markdown("---")

daily_goal = st.number_input("일일 총 목표 공부량 (분):", min_value=0, value=60, step=5, key='goal_min')
st.session_state.goal_sec = 60 * daily_goal

col_start, col_reset = st.columns(2)
button_label = "일시 정지 ⏸️" if st.session_state.is_running else "공부 시작/재개 ▶️"
col_start.button(button_label, on_click=start_stop_timer)
col_reset.button("종료 및 초기화 🔄", on_click=reset_timer)

total_elapsed_sec = st.session_state.total_elapsed_sec

if st.session_state.is_running:
    current_duration = time.time() - st.session_state.start_time
    total_elapsed_sec = st.session_state.paused_duration + current_duration
    st.session_state.total_elapsed_sec = total_elapsed_sec
    
    time.sleep(1)
    st.rerun()

elif not st.session_state.is_running:
    total_elapsed_sec = st.session_state.paused_duration
    st.session_state.total_elapsed_sec = total_elapsed_sec

elapsed_sec = int(total_elapsed_sec)
minutes = elapsed_sec // 60
seconds = elapsed_sec % 60

st.subheader(f" 총 공부 시간: {minutes}분 {seconds}초")

with st.sidebar:
    st.header("과목별 비율 설정")
    subjects = st.number_input("오늘 공부할 과목의 수:", min_value=1, value=1, step=1, key="num_subjects")
    
    current_labels2 = []
    current_sizes2 = []
    
    for i in range(subjects):
        col_name, col_percent = st.columns(2)
        subject_name = col_name.text_input(f"{i+1} 과목 이름:", key=f"subj_name_{i}")
        percent = col_percent.number_input("비율(%)", min_value=0.0, max_value=100.0, step=0.1, key=f"subj_percent_{i}")

        if subject_name and percent > 0:
            current_labels2.append(subject_name)
            current_sizes2.append(percent)

    st.session_state.labels2 = current_labels2
    st.session_state.sizes2 = current_sizes2

subject_goal_times = []
labels2 = st.session_state.labels2
sizes2 = st.session_state.sizes2
goal_sec = st.session_state.goal_sec

if sum(sizes2) > 0 and goal_sec > 0:
    total_percent = sum(sizes2)
    subject_goal_times = [goal_sec * (p / total_percent) for p in sizes2]

if st.session_state.is_running and len(labels2) > 0:
    for i, label in enumerate(labels2):
        # 배열 인덱스 체크를 추가하여 안전하게 접근
        if i < len(subject_goal_times) and total_elapsed_sec >= subject_goal_times[i] and i not in st.session_state.notified_subjects:
            st.toast(f"📢 {label} 과목 목표 시간 도달! 축하해요!! :)", icon='🎉')
            st.session_state.notified_subjects.add(i)

if goal_sec > 0:
    result = (elapsed_sec * 100) / goal_sec
    st_result = round(result, 2)
    
    if elapsed_sec >= goal_sec:
        st.balloons()
        st.success(f"🎉 목표 달성! 총 달성률: {st_result}%")
    else:
        st.info(f"아쉽지만 목표를 달성하지 못했어요. 목표 달성률은 **{st_result}%**에요.")

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    plot_st = min(st_result, 100)
    labels1 = ['총 공부 시간', '남은 목표 시간']
    sizes1 = [plot_st, max(0, 100 - plot_st)]

    def make_pumpkin(labels):
        def my_pumpkin(pct):
            value = pct * sum(sizes1) / 100.0
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


    def make_potato(labels):
        def my_potato(pct):
            value = pct * sum(sizes2) / 100.0
            label = labels[my_potato.index]
            my_potato.index += 1
            return f"{label}\n{value:.1f}%"
        my_potato.index = 0
        return my_potato

    if len(sizes2) > 0 and sum(sizes2) > 0:
        axs[1].pie(
            sizes2,
            labels=labels2,
            autopct=make_potato(labels2),
            startangle=90
        )
        axs[1].set_title("과목별 공부 시간 비율")
        axs[1].axis('equal')
    else:
        axs[1].set_title("과목 비율 정보 없음")


    plt.tight_layout()
    st.pyplot(fig) # Streamlit에 Matplotlib 그래프 표시

else:
    st.error("목표 시간이 0이어서 달성률을 계산할 수 없습니다. 목표를 1분 이상으로 설정해주세요.")
