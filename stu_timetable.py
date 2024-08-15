import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

st.header('시간표 확인')
# 1. 학생별 강의실 정보 로드
file_path = '2024.2학기 학생별 강의실.xlsx'
student_data = pd.read_excel(file_path, dtype={'학번': str})

# Streamlit 사이드바 입력
st.sidebar.header('2024.2학기 대구과학고')

# 학생 학번 입력
student_id = st.sidebar.text_input('학생 학번을 입력하세요')

# 날짜 입력 필드
today = datetime.today().strftime('%Y%m%d')
all_ti_ymd = st.sidebar.text_input('ALL_TI_YMD', value=today, placeholder=today)

# 학교코드 입력 필드
atpt_ofcdc_sc_code = st.sidebar.text_input('교육청코드', value='D10', placeholder='D10')
sd_schul_code = st.sidebar.text_input('학교번호', value='7240060', placeholder='7240060')

st.sidebar.text("학생의 강의실 정보는 학교코드변경 시 수정해주어야 합니다.")

# 조회 버튼
if st.sidebar.button('시간표 조회'):
    # 학번으로 강의실 정보 찾기
    if '학번' not in student_data.columns:
        st.error('학번 열을 찾을 수 없습니다. 열 이름을 확인해주세요.')
        st.stop()

    student_info = student_data[student_data['학번'] == student_id]

    if student_info.empty:
        st.warning('해당 학번의 학생 정보를 찾을 수 없습니다.')
        st.stop()

    # 학생이 듣는 강의실 목록 가져오기
    room_list = student_info.dropna(axis=1).iloc[0].tolist()


    # NEIS API 요청
    def fetch_timetable(atpt_code, schul_code, date=None, room_list=None):
        api_key = 'f142b5caa822427392fb60899130ab0b'
        api_url = 'https://open.neis.go.kr/hub/hisTimetable'
        p_index = 1
        p_size = 100
        timetable_data = []

        while True:
            params = {
                'KEY': api_key,
                'ATPT_OFCDC_SC_CODE': atpt_code,
                'SD_SCHUL_CODE': schul_code,
                'Type': 'xml',
                'pIndex': p_index,
                'pSize': p_size
            }

            if date:
                params['ALL_TI_YMD'] = date

            response = requests.get(api_url, params=params, verify=False)
            response_content = response.content
            root = ET.fromstring(response_content)

            rows = root.findall('.//row')
            if not rows:
                break

            for row in rows:
                period = row.find('PERIO').text
                room_nm = row.find('CLRM_NM').text if row.find('CLRM_NM') is not None else '강의실 정보 없음'
                subject_nm = row.find('ITRT_CNTNT').text
                if room_nm in room_list:
                    timetable_data.append((period, room_nm, subject_nm))

            p_index += 1

        return timetable_data


    # 시간표 가져오기
    timetable = fetch_timetable(atpt_ofcdc_sc_code, sd_schul_code, all_ti_ymd, room_list)

    # DataFrame 생성
    df = pd.DataFrame(timetable, columns=['교시', '강의실', '과목'])

    # 교시별 데이터 병합
    df_grouped = df.groupby('교시')['과목'].apply(lambda x: ', '.join(x)).reset_index()

    # 시간표 출력
    st.subheader(f"{student_id} 학생의 {all_ti_ymd} 시간표")
    st.dataframe(df_grouped)

else:
    st.info('학생 학번과 날짜를 입력하고 "시간표 조회" 버튼을 눌러주세요.')
