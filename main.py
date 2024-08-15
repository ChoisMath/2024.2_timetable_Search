from PyPDF2 import PdfReader
import re
import pandas as pd
def extract_text_from_pdf(pdf_path):
    # PDF 파일 열기
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        # 모든 페이지의 텍스트 추출
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

def parse_table_from_text(text):
    # 텍스트에서 테이블 데이터 파싱 (간단한 예제)
    # 줄 단위로 텍스트를 나눔
    lines = text.split('\n')
    table_data = []
    for line in lines:
        # 특정 패턴을 기준으로 라인을 분할하여 테이블 행으로 간주 (여기서는 탭을 기준으로 함)
        columns = re.split(r'\s{2,}', line.strip())
        if len(columns) > 1:
            table_data.append(columns)
    return table_data

# 사용 예제
pdf_path = "현장적합성 점검용 계정_240719.pdf"  # 분석할 PDF 파일 경로

# PDF에서 텍스트 추출
pdf_text = extract_text_from_pdf(pdf_path)
pdf_text = pdf_text.replace('활동기간', '활동기간\n')
pdf_text = pdf_text.replace('test', '  test')
pdf_text = pdf_text.replace('선생님', '  선생님  ')
pdf_text = pdf_text.replace('t01', 't01  ')
pdf_text = pdf_text.replace('(G', '  (G')
pdf_text = pdf_text.replace('개발', '  개발  ')
pdf_text = pdf_text.replace('개발', '  개발  ')
pdf_text = pdf_text.replace(')G', ')\nG')

for i in range(1,26):
    pdf_text = pdf_text.replace(f's{i:02d}', f's{i:02d}  ')
    pdf_text = pdf_text.replace(f'학생{i:02d}', f'  학생{i:02d}  ')

pdf_text = pdf_text.replace('s18  Ac', 's18Ac')

# 추출된 텍스트에서 테이블 데이터 파싱
table_data = parse_table_from_text(pdf_text)
print(pdf_text)
# 파싱된 테이블 데이터 출력
df = pd.DataFrame(table_data, columns=['익명코드','아이디','비밀번호','사용자','이름','학급명','검토단계','활동기간'], index=range(1, len(table_data)+1))

output_excel_path = "output.xlsx"
df.to_excel(output_excel_path, index=False)

