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
# time.sleep(1)   # 에러 대처 방안1 : 강제 delay 부여

# 법인 > 열람/발급(출력) click    
 
# 에러 대처 방안2 : element_to_click 활용
element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cenS"]/div/ul/li[2]/a/img')))
driver.execute_script("arguments[0].click();", element_to_click)
# driver.find_element(By.XPATH, '//*[@id="cenS"]/div/ul/li[2]/a/img').click()   # 에러 발생하는 기존 코드
driver.find_element(By.XPATH, '//*[@id="cenS"]/div/ul/li[2]/div/ul/li[1]/a').click()


# 상호로 찾기
driver.switch_to.frame("inputFrame") # iframe 내에서 작업 처리
# dropList_RegistryOffice 등기소
driver.find_element(By.ID, 'DropList').click()
driver.find_element(By.XPATH, '//*[@id="DropList"]/option[2]').click()  # "전체등기소" 선택
# dropList_CorporationClassification 법인구분
driver.find_element(By.ID, 'SGC_RTVBUBINGB').click()
driver.find_element(By.XPATH, '//*[@id="SGC_RTVBUBINGB"]/option[2]').click()    # "전체 법인(지배인, 미성년자, 법정대리인 제외)" 선택
# 상호 입력
input_corporationName = driver.find_element(By.ID, "SANGHO_NUM")
input_corporationName.send_keys("숭실대학교")
# 검색 버튼 클릭
driver.find_element(By.XPATH, '//*[@id="searchArea"]/form[1]/div/div/div/div/fieldset/div/table/tbody/tr[9]/td[2]/button').click()
# iframe -> 기본 콘텐츠로 되돌리기
driver.switch_to.default_content()


# 검색된 'list_table 작업하기
driver.switch_to.frame("resultFrame")
driver.switch_to.frame("frmOuterModal")


list_table = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div')))
tbody = list_table.find_element(By.XPATH, "//div[2]/table[2]/tbody")
rows = tbody.find_elements(By.TAG_NAME, 'tr')

rows = rows[1:]
for row in rows:
    registoryOffice = row.find_element(By.XPATH, './/td[1]').text
    division = row.find_element(By.XPATH, './/td[2]').text
    num = row.find_element(By.XPATH, './/td[4]').text
    corporation_name = row.find_element(By.XPATH, './/td[5]/a').text

    print('관할등기소 : ', registoryOffice)
    print('법인구분 : ', division)
    print('등기번호 : ', num)
    print('상호 : ', corporation_name)
    print('\n')

driver.switch_to.default_content()

time.sleep(2000)