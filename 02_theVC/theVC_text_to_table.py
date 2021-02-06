import pandas as pd 


# text 파일 읽어오기
path = "data.txt"

with open(path, "r", encoding='UTF8') as file:
    strings = file.readlines()
    print(strings)


# 개행문자 제거 
test = []

for item in strings:
    test.append(item.rstrip('\n'))
    
# 잘못 들어간 값 제거
try: 
    test.remove('더보기')
except Exception:
    pass
   
   
# 회사,서비스,설명,상세정보 추출
company = []
service = []
description = []
detail = []

for i in range(0, len(test)):
    if i % 5 == 0:
        company.append(test[i])
    elif i % 5 == 2:
        service.append(test[i])
    elif i % 5 == 3:
        description.append(test[i])
    elif i % 5 == 4:
        detail.append(test[i])
    else:
        pass

print("회사명을 추출합니다")
print(company)


# 데이터프레임으로 저장하기
df = []
zippedList = list(zip(company, service, description, detail))
df= pd.DataFrame(zippedList, columns = ['company', 'service', 'description', 'detail'])


# 중복된 업체 제거하기
df = df.drop_duplicates()
print("회사 개수 : ")
df.shape[0]


## detail 정보 분리하기

# 대분류
def split_desc(detail):
    return detail.split("\t")[1]

df['category1'] = df['detail'].apply(split_desc)


# 소분류
def split_desc(detail):
    return detail.split("\t")[2]

df['category2'] = df['detail'].apply(split_desc)


# 총 투자금액
def split_desc(detail):
    return detail.split("\t")[8]

df['ir_total_amount'] = df['detail'].apply(split_desc)


# 현재 투자단계
def split_desc(detail):
    return detail.split("\t")[9]

df['ir_stage'] = df['detail'].apply(split_desc)


# 최근 투자날짜
def split_desc(detail):
    return detail.split("\t")[10]

df['ir_date'] = df['detail'].apply(split_desc)

# 연도만 추출
df['funding_year_month'] = df['ir_date'].str[0:7]
df['funding_year'] = df['ir_date'].str[0:4]


# 기술 추출
def split_desc(detail):
    return detail.split("\t")[0]

df['tech'] = df['detail'].apply(split_desc)


# 서비스 형태 추출
def split_desc(detail):
    return detail.split("\t")[3]

df['service_type'] = df['detail'].apply(split_desc)


# detail, 투자날짜 컬럼 지우기
df.drop('detail', axis=1, inplace=True)
df.drop('ir_date', axis=1, inplace=True)


## 투자금액 전처리
# '억' 텍스트 제거 
df['ir_total_amount'] = df['ir_total_amount'].str.replace("억", "")


# O천만원 -> 억으로 변환
def transform(amount):
    if "천만원" in amount:
        amount = amount.replace("천만원", "")
        amount = int(amount) * 0.1
    return amount
        
df['ir_total_amount'] = df['ir_total_amount'].apply(transform)


# 서비스 타입 전처리
df['service_type'] = df['service_type'].str.replace("-iOS","")
df['service_type'] = df['service_type'].str.replace("-Android","")


# 파일로 저장하기
print("data_table.xlsx 파일로 저장합니다.")
label = ["회사명","제품/서비스명","설명","대분류","소분류","총 투자금액","투자단계","투자연월","투자연도","기술","서비스 타입"]

df.to_excel("data_table.xlsx", index=False, header=label)

