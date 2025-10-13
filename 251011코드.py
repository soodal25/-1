import streamlit as st
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = "C:Users\\USER\\Desktop\\GowunDodum-Regular (1).ttf"
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)

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


st.title("수학과 코딩을 결합한 스터디 플래너")
st.markdown("---")

daily_goal = st.number_input("일일 총 목표 공부량 (분):", min_value=0, value=60, step=5, key='goal_min')
st.session_state.goal_sec = 60 * daily_goal

col_selector, col_start, col_reset = st.columns([2, 1, 1])

subject_options = ["(과목 선택)"] + st.session_state.labels2
selected_subject_name = col_selector.selectbox("현재 공부할 과목:", options=subject_options, key="subject_selector")

button_label = f"중지 ⏸️" if st.session_state.is_running else f"시작 ▶️"
col_start.button(button_label, on_click=start_stop_timer)
col_reset.button("전체 초기화 🔄", on_click=reset_timer)

if st.session_state.is_running:
    time_spent_since_start = time.time() - st.session_state.start_time
    time_to_add = 1.0 
    

    update_subject_time(time_to_add)
    

    st.session_state.total_elapsed_sec += time_to_add
    

    st.session_state.start_time = time.time()

    time.sleep(1)
    st.rerun() 

elapsed_sec = int(st.session_state.total_elapsed_sec)
minutes = elapsed_sec // 60
seconds = elapsed_sec % 60

st.subheader(f"⏱️ 총 공부 시간: {minutes}분 {seconds}초")


subject_time_data = []
if st.session_state.subject_times:
    st.markdown("### 과목별 누적 시간")
    for subj, sec in st.session_state.subject_times.items():
        if sec > 0:
            sub_min = int(sec) // 60
            sub_sec = int(sec) % 60
            st.write(f"- **{subj}**: {sub_min}분 {sub_sec}초")
            subject_time_data.append((subj, sec)) 


with st.sidebar:
    st.header("과목별 계획 비율 설정")
    subjects = st.number_input("오늘 공부할 과목의 수:", min_value=0, value=3, step=1, key="num_subjects")
    
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


labels2 = st.session_state.labels2
sizes2 = st.session_state.sizes2
goal_sec = st.session_state.goal_sec
total_elapsed_sec = st.session_state.total_elapsed_sec

if sum(sizes2) > 0 and goal_sec > 0:
    total_percent = sum(sizes2)
    subject_goal_times = [goal_sec * (p / total_percent) for p in sizes2]

if st.session_state.is_running and len(labels2) > 0:
    for i, label in enumerate(labels2):
        subject_current_time = st.session_state.subject_times.get(label, 0.0)
        if i < len(subject_goal_times) and subject_current_time >= subject_goal_times[i] and label not in st.session_state.notified_subjects:
            st.toast(f" {label} 과목 목표 시간 도달! 축하해요!! 🎉", icon='🎉')
            st.session_state.notified_subjects.add(label) 


if goal_sec > 0:
    result = (elapsed_sec * 100) / goal_sec
    st_result = round(result, 2)
    
    if elapsed_sec >= goal_sec:
        st.balloons()
        st.success(f"🎉 총 목표 달성! 달성률: {st_result}%")
    elif elapsed_sec > 0:
        st.info(f"아쉽지만 총 목표를 달성하지 못했어요. 달성률은 **{st_result}%**에요.")

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
    axs[0].set_title("총 공부 목표 달성률")
    axs[0].axis('equal')

 
    actual_labels = [item[0] for item in subject_time_data]
    actual_times = [item[1] for item in subject_time_data]

    def make_actual_pie(labels):
        def my_actual_pie(pct):
            value = pct * sum(actual_times) / 100.0 / 60
            label = labels[my_actual_pie.index]
            my_actual_pie.index += 1
            return f"{label}\n{value:.1f}분"
        my_actual_pie.index = 0
        return my_actual_pie

    if len(actual_times) > 0 and sum(actual_times) > 0:
        axs[1].pie(
            actual_times,
            labels=actual_labels,
            autopct=make_actual_pie(actual_labels),
            startangle=90
        )
        axs[1].set_title("과목별 실제 공부 시간")
        axs[1].axis('equal')
    else:
        axs[1].set_title("과목별 실제 공부 시간 (데이터 없음)")

    plt.tight_layout()
    st.pyplot(fig)

elif daily_goal > 0 and elapsed_sec > 0:
    st.warning("목표 달성률을 계산하려면 목표 시간이 1분 이상이어야 합니다.")










