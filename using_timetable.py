import requests
import xml.etree.ElementTree as ET


def fetch_timetable(date=None):
    # NEIS API 기본 정보
    api_key = 'f142b5caa822427392fb60899130ab0b'
    api_url = 'https://open.neis.go.kr/hub/hisTimetable'
    params = {
        'KEY': api_key,
        'ATPT_OFCDC_SC_CODE': 'D10',
        'SD_SCHUL_CODE': '7240060',
        'Type': 'xml'
    }

    # 날짜가 지정되었을 경우, 날짜를 파라미터에 추가
    if date:
        params['ALL_TI_YMD'] = date

    # API 요청 (SSL 인증서 검증 비활성화)
    response = requests.get(api_url, params=params, verify=False)
    response_content = response.content

    # XML 파싱
    root = ET.fromstring(response_content)

    # 학급별 시간표 출력
    for row in root.findall('.//row'):
        grade = row.find('GRADE').text  # 학년
        class_nm = row.find('CLASS_NM').text  # 반 이름
        period = row.find('PERIO').text  # 교시
        subject_nm = row.find('ITRT_CNTNT').text  # 과목명
        room_nm = row.find('CLRM_NM').text if row.find('CLRM_NM') is not None else '강의실 정보 없음'  # 강의실 명

        print(f"{grade}학년 {class_nm}반 - {period}교시: {subject_nm} (강의실: {room_nm})")


# 날짜 입력 (예: '20240306'). 비워두면 전체 시간표가 출력됨.
date_input = input("원하는 날짜를 입력하세요 (예: 20240306). 비워두면 전체 시간표를 출력합니다: ").strip()

# 시간표 출력
fetch_timetable(date_input)
