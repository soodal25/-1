import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm # 필수: 폰트 관리를 위한 모듈
import os # 필수: 상대 경로 설정을 위한 모듈

# ----------------------------------------------------------------------
# ⭐️ 폰트 로드 및 설정 (폰트 깨짐 및 모든 오류 해결 로직) ⭐️
# 이 블록 전체가 코드 맨 위에 있어야 합니다.
# ----------------------------------------------------------------------
FONT_FILENAME = "GOWUNDODUM-REGULAR.TTF" 

# 폰트 경로 설정 (상대 경로 사용)
try:
    # 현재 스크립트 파일이 있는 디렉토리를 기준으로 폰트 파일을 찾습니다.
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FONT_FILENAME)
except NameError:
    # Streamlit Cloud 환경 등에서 __file__이 정의되지 않은 경우 대비
    font_path = FONT_FILENAME 

def set_font_fallback():
    # 시스템 내에서 대체 폰트(한글 지원)를 찾아 설정합니다.
    fallback_fonts = ['NanumGothic', 'Malgun Gothic', 'sans-serif']
    
    for font_name_str in fallback_fonts:
        try:
            font_path_auto = fm.findfont(font_name_str, fallback_to_default=False)
            font_name_auto = fm.FontProperties(fname=font_path_auto).get_name()
            plt.rcParams['font.family'] = font_name_auto
            mpl.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
            return True, font_name_auto
        except:
            continue
    
    plt.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['axes.unicode_minus'] = False
    return False, 'sans-serif'

try:
    # 1. 폰트 파일 존재 여부 확인
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"폰트 파일 '{FONT_FILENAME}'을 코드 폴더에서 찾을 수 없습니다.")

    # 2. GOWUNDODUM 폰트 로드 및 적용
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = font_name
    mpl.rcParams['axes.unicode_minus'] = False
    st.sidebar.success(f"✔️ {font_name} 폰트 적용 완료.")

except FileNotFoundError as e:
    # 3. GOWUNDODUM 파일 없을 시 대체 폰트 로드 시도
    success, fallback_name = set_font_fallback()
    if success:
        st.sidebar.error(f"❌ 폰트 파일 오류: {e}")
        st.sidebar.warning(f"⚠️ 시스템 폰트 **{fallback_name}**로 대체되어 한글이 표시됩니다.")
    else:
        st.sidebar.error("❌ 모든 폰트 로드 실패. 그래프 한글이 깨질 수 있습니다.")

except Exception:
    # 4. 기타 폰트 로드 오류 시 대체 폰트 로드 시도
    success, fallback_name = set_font_fallback()
    if success:
        st.sidebar.warning(f"⚠️ 폰트 로드 중 예기치 않은 오류 발생. 시스템 폰트 **{fallback_name}**로 대체됩니다.")
    else:
        st.sidebar.error("❌ 폰트 로드 중 예기치 않은 오류 발생. 기본 폰트로 대체됩니다.")
# ----------------------------------------------------------------------


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
        if goal_sec <= 0:
            st.warning("먼저 목표 시간을 1분 이상으로 설정해주세요.")
            return
        st.session_state.running = True
        st.session_state.start_time = time.time()

def reset_timer():
    st.session_state.running = False
    st.session_state.total_elapsed_sec = 0.0
    st.session_state.start_time = 0.0

st.title("📚 Streamlit 공부 시간 측정 및 분석")
st.markdown("---")

# 1. 목표 시간 입력 (st.input 사용)
daily_goal = st.text_input("일일 목표 공부량을 입력하세요 (분):", value="60")
try:
    goal = int(daily_goal)
    goal_sec = 60 * goal
    st.info(f"오늘의 목표 공부 시간은 **{goal}분**입니다.")
except ValueError:
    st.error("목표 시간은 숫자로 입력해 주세요.")
    goal_sec = 0

# 2. 타이머 위젯 및 로직
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
seconds = elapsed_sec % 60

st.subheader(f"총 공부 시간: {minutes}분 {seconds}초")
st.markdown("---")

# 3. 목표 달성률 계산 및 결과 출력
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
        
        # 공부 목표 달성률 파이 차트
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

        # 5. 과목별 비율 입력 (사이드바 사용)
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

        # 과목별 공부 시간 비율 파이 차트
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
        st.error("목표 시간이 0분입니다.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
