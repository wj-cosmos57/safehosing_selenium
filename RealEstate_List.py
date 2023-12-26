from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

# 쿠키 제거
options = webdriver.ChromeOptions()
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-notifications")
options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])

driver = webdriver.Chrome(options=options)
driver.maximize_window()  # 브라우저 창을 최대화합니다.

url = 'http://www.iros.go.kr/PMainJ.jsp'
driver.get(url)
wait = WebDriverWait(driver, 10)

# 로딩 오버레이가 사라질 때까지 대기
wait.until(EC.invisibility_of_element_located((By.ID, "AnySign4PCLoadingImg_overlay")))

# 부동산 > 열람/발급(출력) click
element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cenS"]/div/ul/li[1]/div/ul/li[1]/a')))
driver.execute_script("arguments[0].click();", element_to_click)
# driver.find_element(By.XPATH, '//*[@id="cenS"]/div/ul/li[1]/div/ul/li[1]/a').click()


# 등기 열람/발급 > 주소 검색 이후 
driver.switch_to.frame("inputFrame") # iframe 내에서 작업 처리
input_address = driver.find_element(By.ID, "txt_simple_address")
input_address.send_keys("서울시 동작구 상도동 509")
driver.find_element(By.XPATH, '//*[@id="btnSrchSojae"]').click()
# iframe -> 기본 콘텐츠로 되돌리기
driver.switch_to.default_content()


# 검색된 'list_table 작업하기
driver.switch_to.frame("resultFrame")
driver.switch_to.frame("frmOuterModal")

# 총 검색된 건수(전처리전)
total_count_text = driver.find_element(By.XPATH, '//*[@id="simpleResult"]/div[3]/div[1]').text
# 총 검색된 건수(전처리후)
total_count = int(total_count_text.split()[1].split()[0])
# 총 검색된 페이지수(전처리전)
total_pages_text = driver.find_element(By.CSS_SELECTOR, "div.paginate span.pg2").text   # ( 1 / 4 )페이지
# 총 검색된 페이지수(전처리후)
total_pages = int(total_pages_text.split('/')[1].strip().split()[0])    
current_page = 1

print('총 검색 건수 : ', total_count)
print('총 검색 페이지수 : ', total_pages)
print('\n')

list_table = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="simpleResult"]/div[2]')))
tbody = list_table.find_element(By.XPATH, "//table/tbody")
rows = tbody.find_elements(By.TAG_NAME, 'tr')

# 검색 결과 리스트 출력하기
for row in rows:
    # print(row.text)
    num = row.find_element(By.XPATH, './/td[1]').text
    division = row.find_element(By.XPATH, './/td[2]').text
    address = row.find_element(By.XPATH, './/td[3]').text
    state_element = row.find_element(By.XPATH, './/td[5]/img')
    state = state_element.get_attribute('alt')

    print('부동산 고유번호 : ', num)
    print('구분 : ', division)
    print('부동산 소재지번 : ', address)
    print('상태 : ', state)
    print('\n')

driver.switch_to.default_content()

time.sleep(2000)