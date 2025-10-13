import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm # ⭐️ 필수: fm 모듈 추가 ⭐️
import os # ⭐️ 필수: os 모듈 추가 ⭐️

# ----------------------------------------------------------------------
# ⭐️ 폰트 로드 및 설정 (폰트 깨짐 및 경로/문법 오류 해결) ⭐️
# 이 블록 전체가 코드 맨 위에 있어야 안전합니다.
# ----------------------------------------------------------------------
FONT_FILENAME = "GOWUNDODUM-REGULAR.TTF" 

# 폰트 경로 설정 (상대 경로)
try:
    # 현재 스크립트의 절대 경로를 기준으로 폰트를 찾습니다.
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FONT_FILENAME)
except NameError:
    # Streamlit Cloud 환경에서 __file__이 없을 때 대비
    font_path = FONT_FILENAME 

def set_font_fallback():
    # 시스템 내에서 대체 폰트(한글 지원)를 찾아 설정합니다.
    fallback_fonts = ['NanumGothic', 'Malgun Gothic', 'sans-serif']
    
    for font_name_str in fallback_fonts:
        try:
            font_path_auto = fm.findfont(font_name_str, fallback_to_default=False)
            font_name_auto = fm.FontProperties(fname=font_path_auto).get_name()
            plt.rcParams['font.family'] = font_name_auto
            mpl.rcParams['axes.unicode_minus'] = False
            return True, font_name_auto
        except:
            continue
    
    plt.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['axes.unicode_minus'] = False
    return False, 'sans-serif'

try:
    if not os.path.exists(font_path):
        # 폰트 파일이 코드 폴더에 없을 경우 FileNotFoundError 발생
        raise FileNotFoundError(f"폰트 파일 '{FONT_FILENAME}'을 코드 폴더에서 찾을 수 없습니다.")

    # 1. GOWUNDODUM 폰트 로드 성공 시
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = font_name
    mpl.rcParams['axes.unicode_minus'] = False
    st.sidebar.success(f"✔️ {font_name} 폰트 적용 완료.")

except FileNotFoundError as e:
    # 2. GOWUNDODUM 파일 없을 시 대체 폰트 로드 시도
    success, fallback_name = set_font_fallback()
    if success:
        st.sidebar.error(f"❌ 폰트 오류: {e}")
        st.sidebar.warning(f"⚠️ 시스템 폰트 **{fallback_name}**로 대체되어 한글이 표시됩니다.")
    else:
        st.sidebar.error("❌ 모든 폰트 로드 실패
