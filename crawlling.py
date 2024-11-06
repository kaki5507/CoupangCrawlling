import time
import random
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import chromedriver_autoinstaller

# 크롬 드라이버 설치
chromedriver_autoinstaller.install()

# 랜덤 User-Agent 리스트
user_agents = UserAgent()

# 랜덤으로 User-Agent 선택
random_user_agent = user_agents.random

# Selenium WebDriver 설정
options = webdriver.ChromeOptions()
# 봇 감지 쿠팡-> headless?
options.add_argument("--headless=new ") #일부페이지 headless 모드로 안보일 수 있음
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-agent={random_user_agent}")
#options.add_experimental_option("detach", True)  # 브라우저 자동 종료 방지
#options.add_argument("--disable-blink-features=AutomationControlled") # Selenium의 자동화 탐지를 우회하기 위한 옵

# 위에 설정한 옵션들로 Chrome브라우저 인스턴스 생성
driver = webdriver.Chrome(options=options)

#driver.get("https://www.coupang.com/") #랜더링이 전체가 되지않고 카테고리까지 돼서 수정
#쿠팡 channel이 recent랑 user로 계속 바뀜
#동적인 url 
#https://www.coupang.com/np/search?component=&q=%EA%B3%BC%EC%9E%90&channel=user
#https://www.coupang.com/np/search?q=%EA%B3%BC%EC%9E%90&channel=recent

driver.get("https://www.coupang.com/np/search?q=%EA%B3%BC%EC%9E%90&channel=recent")

time.sleep(random.uniform(3, 7)) # 랜더링 대기시간 랜덤(봇 감지 피하기 위함)

#print(" ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★ ") 
#print(driver.page_source) # 현재 DOM 페이지 표시
#print(" ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★ // ")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#searchBox = WebDriverWait(driver, 100).until(
#    EC.presence_of_element_located((By.XPATH, '//*[@id="headerSearchKeyword"]'))
#)
#searchBox.send_keys("과자")
#searchBox.send_keys(Keys.RETURN)

#print(driver.page_source) # 현재 DOM 페이지 표시

total_price = 200000 # 토탈 금액 인원 변동 시 변경
now_price = 0
product_list = []
print(1)
while now_price < total_price:
    time.sleep(random.uniform(3, 7)) # 랜더링 대기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 페이지 끝까지 스크롤
    items_cnt = 0
    print(now_price)
    while items_cnt < 2:
        time.sleep(random.uniform(3, 6)) # 랜더링 대기
        price_wraps = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#productList .search-product'))
        )
        # 랜덤으로 상품 선택
        selected_price_wraps = random.sample(price_wraps, 2)
        print(selected_price_wraps)
        # 2개 뽑은 것에서 반복문
        for price_wrap in selected_price_wraps: 
            try:
                # 상품 이름 추출
                item_name = WebDriverWait(price_wrap, 30).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.name"))
                ).text
                # 상품 가격 추출
                item_price_txt = WebDriverWait(price_wrap, 30).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "strong.price-value"))
                ).text
                print("★★★★★★★★")
                print(item_name)
                print(item_price_txt)
                print("★★★★★★★★")
                # int로 변환 (가격에서 ',' 제거)
                item_price = int(item_price_txt.replace(",", ""))

                # total_price를 넘지 않도록 체크
                product_list.append({"name": item_name, "price": item_price})
                now_price += item_price
                items_cnt += 1

                price_wraps.remove(price_wrap)  # 선택된 요소를 리스트에서 제거
            except Exception as e:
                print("1번에서 예외" , e)

    try:
        time.sleep(random.uniform(1, 3))
        next_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn-next"))
        )
        next_button.click()
        time.sleep(random.uniform(3, 10)) # 랜더링 대기
    except Exception as e:
        print("2번에서 예외" , e)

print("종료")
# WebDriver 종료
driver.quit()

# 총합 값
sum_row = pd.DataFrame([{"name": "총합", "price": now_price}])

print("★★★★★★★★")
file_path = 'product_list.xlsx'
df = pd.DataFrame(product_list)  # product_list를 DataFrame으로 변환
df = pd.concat([df, sum_row], ignore_index=False)
df.to_excel(file_path, index=False)  # 엑셀 파일로 저장

# 파일이 생성되었는지 확인
if os.path.exists(file_path):
    print(f"파일 생성 성공: {file_path}")
else:
    print("파일 생성 실패")