import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

# Streamlit 사이드바 입력
st.sidebar.header('시간표 조회 설정')

# 필수 입력 필드
atpt_ofcdc_sc_code = st.sidebar.text_input('ATPT_OFCDC_SC_CODE', value='D10', placeholder='D10')
sd_schul_code = st.sidebar.text_input('SD_SCHUL_CODE', value='7240060', placeholder='7240060')

# 날짜 입력 필드
today = datetime.today().strftime('%Y%m%d')
all_ti_ymd = st.sidebar.text_input('ALL_TI_YMD', value=today, placeholder=today)

# 조회 버튼
if st.sidebar.button('시간표 조회'):
    # 필수 필드 확인
    if not atpt_ofcdc_sc_code or not sd_schul_code:
        st.warning('ATPT_OFCDC_SC_CODE와 SD_SCHUL_CODE는 필수 입력 항목입니다. 기본 시간표가 출력됩니다.')
        st.stop()


    # NEIS API 요청
    def fetch_timetable(atpt_code, schul_code, date=None):
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
                grade = row.find('GRADE').text
                period = row.find('PERIO').text
                room_nm = row.find('CLRM_NM').text if row.find('CLRM_NM') is not None else '강의실 정보 없음'
                subject_nm = row.find('ITRT_CNTNT').text
                timetable_data.append((grade, period, room_nm, subject_nm))

            p_index += 1

        return timetable_data


    # 시간표 가져오기
    timetable = fetch_timetable(atpt_ofcdc_sc_code, sd_schul_code, all_ti_ymd)

    # DataFrame 생성
    df = pd.DataFrame(timetable, columns=['GRADE', 'PERIO', 'CLRM_NM', 'SUBJECT'])

    # 학년별로 데이터 분할
    grades = df['GRADE'].unique()

    for grade in grades:
        st.subheader(f'{grade}학년 시간표')

        # 해당 학년 데이터 필터링
        df_grade = df[df['GRADE'] == grade]

        # 중복된 항목 처리: 같은 교시, 같은 강의실에서 여러 수업이 있는 경우 수업명을 병합
        df_grouped = df_grade.groupby(['PERIO', 'CLRM_NM'])['SUBJECT'].apply(lambda x: ', '.join(x)).reset_index()

        # 피벗 테이블 생성
        df_pivot = df_grouped.pivot(index='PERIO', columns='CLRM_NM', values='SUBJECT')

        # 스크롤 가능한 테이블 출력
        st.dataframe(df_pivot)

else:
    st.info('시간표 조회를 위해 "시간표 조회" 버튼을 눌러주세요.')
