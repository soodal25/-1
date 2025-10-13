import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm # 필수: 폰트 관리를 위한 모듈
import os # 필수: 상대 경로 설정을 위한 모듈

# ----------------------------------------------------------------------
# ⭐️ 폰트 로드 및 설정 (Nanum Gothic 강제 적용 버전) ⭐️
# 서버 환경에서 가장 잘 작동하는 방식으로 Matplotlib 폰트를 설정합니다.
# ----------------------------------------------------------------------

# NanumGothic 또는 Malgun Gothic 폰트를 시스템에서 찾으려 시도
def set_nanum_or_malgun():
    fallback_fonts = ['NanumGothic', 'Malgun Gothic', 'sans-serif']
    
    for font_name_str in fallback_fonts:
        try:
            # 시스템에서 폰트 찾기 시도
            font_path_auto = fm.findfont(font_name_str, fallback_to_default=False)
            font_name_auto = fm.FontProperties(fname=font_path_auto).get_name()
            plt.rcParams['font.family'] = font_name_auto
            mpl.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
            st.sidebar.success(f"✔️ 시스템 폰트 **{font_name_auto}** 적용 완료.")
            return
        except:
            continue
    
    plt.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['axes.unicode_minus'] = False
    st.sidebar.error("❌ 모든 한글 폰트 로드 실패. 그래프 한글이 깨질 수 있습니다.")

set_nanum_or_malgun()
# ----------------------------------------------------------------------


if 'running' not in st.session_state:
    st.session_state.running = False
# ... (중략: 나머지 코드는 동일하게 사용)



