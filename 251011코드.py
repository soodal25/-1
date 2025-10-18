import streamlit as st
import time
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# --- 폰트 파일 설정 (NanumGothic.ttf 파일이 앱 폴더에 있다고 가정) ---
# 폰트 파일 경로 설정 (Streamlit Cloud에서 현재 디렉토리에 업로드한 파일)
# 🚨🚨 NanumGothic.ttf 파일이 반드시 이 코드 파일과 함께 업로드되어야 합니다.
FONT_PATH = 'NanumGothic.ttf' 

# 폰트 파일이 존재하는지 확인하고 폰트 속성 로드
if os.path.exists(FONT_PATH):
    fontprop = fm.FontProperties(fname=FONT_PATH, size=10)
    plt.rcParams['font.family'] = fontprop.get_name()
    plt.rcParams['axes.unicode_minus'] = False 
    
    # 폰트 캐시 갱신 (필수)
    try:
        fm._rebuild() 
    except Exception:
        pass
else:
    # 폰트 파일이 없을 경우 경고 메시지 출력 (대비책)
    st.warning(f"경고: {FONT_PATH} 파일을 찾을 수 없습니다. 폰트가 깨질 수 있습니다.")
    plt.rcParams['font.family'] = 'sans-serif' # 기본 폰트로 설정

# -------------------- Streamlit 앱의 메인 함수 정의 --------------------
def main():
    
    # ... (Session State 초기화 코드는 동일하게 유지) ...
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'total_elapsed_sec' not in st.session_state:
        st.session_state.total_elapsed_sec = 0.0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0.0
    if 'daily_goal' not in st.session_state:
        st.session_state.daily_goal = "60" 

    # (이하 생략: start_stop_timer, reset_timer 함수 및 UI 로직은 이전 코드와 동일합니다.)
    
    # ... (이전 코드의 UI 및 타이머, 그래프 로직을 여기에 넣으시면 됩니다.)
    
    # 타이머 함수 정의 (간결화를 위해 다시 한 번 포함)
    def start_stop_timer():
        try:
            current_goal_sec = int(st.session_state.daily_goal) * 60 
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

    st.title("수학과 코딩을 결합한 스터디 플래너")
    st.markdown("---")
    # ... (중략: UI 로직) ...
    daily_goal = st.text_input("일일 목표 공부량을 입력하세요 (분):", key='daily_goal') 
    
    # ... (중략: 타이머, 버튼, 그래프 로직) ...

    # Streamlit 앱 실행 시작점
if __name__ == '__main__':
    main()
