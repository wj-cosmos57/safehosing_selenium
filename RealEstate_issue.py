from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

import time
import pyautogui

# 쿠키 제거
# options = webdriver.ChromeOptions()
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--disable-notifications")
# options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])

# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()
driver.maximize_window()  # 브라우저 창을 최대화합니다.

url = 'http://www.iros.go.kr/PMainJ.jsp'
driver.get(url)
wait = WebDriverWait(driver, 5)

# 로딩 오버레이가 사라질 때까지 대기
wait.until(EC.invisibility_of_element_located((By.ID, "AnySign4PCLoadingImg_overlay")))

# 1번 팝업 제거
pyautogui.moveTo(1406, 80)
pyautogui.click()
# 2번 팝업 제거
pyautogui.moveTo(1415, 482)
pyautogui.click()
# 3번 팝업 제거
pyautogui.moveTo(826, 295)
pyautogui.click()


# 로그인
wait.until(EC.visibility_of_element_located((By.ID, 'id_user_id')))
login_input = driver.find_element(By.ID, 'id_user_id')
driver.execute_script("arguments[0].value = 'wooju57';", login_input)
wait.until(EC.visibility_of_element_located((By.ID, 'password')))
password_input = driver.find_element(By.ID, 'password')
driver.execute_script("arguments[0].value = 'Wooju301806';", password_input)
element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="leftS"]/div[2]/form/div[1]/ul/li[4]/a')))
# 로그인 버튼 클릭
# driver.find_element(By.XPATH, '//*[@id="leftS"]/div[2]/form/div[1]/ul/li[4]/a').click()
login_button = driver.find_element(By.XPATH, '//*[@id="leftS"]/div[2]/form/div[1]/ul/li[4]/a')
driver.execute_script("arguments[0].click();", login_button)

# 로그인 후 로그아웃 버튼이 뜰 때까지 대기
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="leftS"]/div[2]/div[1]')))


# 부동산 > 열람/발급(출력) click
element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cenS"]/div/ul/li[1]/div/ul/li[1]/a')))
driver.execute_script("arguments[0].click();", element_to_click)
# driver.find_element(By.XPATH, '//*[@id="cenS"]/div/ul/li[1]/div/ul/li[1]/a').click()

# 팝업 한번 더 제거
# 1번 팝업 제거
pyautogui.moveTo(1406, 80)
pyautogui.click()
# 2번 팝업 제거
pyautogui.moveTo(1415, 482)
pyautogui.click()
# 3번 팝업 제거
pyautogui.moveTo(826, 295)
pyautogui.click()

# 등기 열람/발급 > 고유번호로 찾기
# wait.until(EC.invisibility_of_element_located((By.ID, "AnySign4PCLoadingImg_overlay")))
driver.switch_to.frame("inputFrame") # iframe 내에서 작업 처리
wait.until(EC.presence_of_element_located((By.ID, 'search04Tab')))
search_tab = driver.find_element(By.ID, 'search04Tab')
driver.execute_script("arguments[0].click();", search_tab)


driver.switch_to.default_content()
driver.switch_to.frame("resultFrame")
driver.switch_to.frame("frmOuterModal")
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inpPinNo"]')))
input_serialNum = driver.find_element(By.ID, "inpPinNo")
# 전달받은 고유번호 send_keys에 전달 !!!
input_serialNum.send_keys("1144-2010-000135")

# 1. <고유번호로 부동산 등기 검색> 버튼 클릭
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/form/div/div/div/div/fieldset/div/table/tbody/tr[3]/td[3]/button')))
search_button = driver.find_element(By.XPATH, '/html/body/div/form/div/div/div/div/fieldset/div/table/tbody/tr[3]/td[3]/button')
driver.execute_script("arguments[0].click();", search_button)

# 2. <건물 부동산 소재번 선택> 버튼 클릭
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/table/tbody/tr[2]/td[5]/button')))
select_property_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/table/tbody/tr[2]/td[5]/button')
driver.execute_script("arguments[0].click();", select_property_button)

# 3. <등기기록 유형 선택> 다음 버튼 클릭
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/form/div[4]/button')))
next_button = driver.find_element(By.XPATH, '/html/body/div/form/div[4]/button')
driver.execute_script("arguments[0].click();", next_button)

# 4. <주민등록번호 공개여부 검증> 다음 버튼 클릭
try:
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/form/div[5]/button')))
except:
    skip_button = driver.find_element(By.CLASS_NAME, "btn_bg02_action")
    skip_button.click()

verify_button = driver.find_element(By.XPATH, '/html/body/div/form/div[5]/button')
driver.execute_script("arguments[0].click();", verify_button)

# 결제 버튼 클릭은 frmOuterModal 밖, resultFrame 안에 있기 때문에 iframe을 조정
driver.switch_to.default_content()
driver.switch_to.frame("resultFrame")
# 5. <결제 대상 부동산> 결제 버튼 클릭
# wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/form[2]/div[1]/table/tbody/tr[3]/td[3]/button')))
time.sleep(1)   # "AnySign 이 아직 로딩되지 않았습니다. 잠시만 기다려 주십시요." 예외처리
pay_button = driver.find_element(By.XPATH, '/html/body/div/form[2]/div[1]/table/tbody/tr[3]/td[3]/button')
driver.execute_script("arguments[0].click();", pay_button)


driver.switch_to.default_content()
# 6. 결제진행과정

# 결제 방식 선택 버튼이 나타날 때까지 기다립니다.
paymentway_button_xpath = '//*[@id="inpMtdCls3"]'
wait.until(EC.visibility_of_element_located((By.XPATH, paymentway_button_xpath)))
# 선불지급수단 결제방식 선택
paymentway_button = driver.find_element(By.XPATH, '//*[@id="inpMtdCls3"]')
driver.execute_script("arguments[0].click();", paymentway_button)

wait.until(EC.visibility_of_element_located((By.ID, 'inpEMoneyNo1')))
paymentTokenFirst8 = driver.find_element(By.ID, 'inpEMoneyNo1')
driver.execute_script("arguments[0].value = 'X3263838';", paymentTokenFirst8)

wait.until(EC.visibility_of_element_located((By.ID, 'inpEMoneyNo2')))
paymentTokenLast4 = driver.find_element(By.ID, 'inpEMoneyNo2')
driver.execute_script("arguments[0].value = '3664';", paymentTokenLast4)

wait.until(EC.visibility_of_element_located((By.ID, 'inpEMoneyPswd')))
paymentTokenPswd = driver.find_element(By.ID, 'inpEMoneyPswd')
driver.execute_script("arguments[0].value = 'UJXJxYz5';", paymentTokenPswd)

agreeCheckBox = driver.find_element(By.XPATH, '//*[@id="chk_term_agree_all_emoney"]')
driver.execute_script("arguments[0].click();", agreeCheckBox)

wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="EMO"]/div[5]/button[1]')))
payButton = driver.find_element(By.XPATH, '//*[@id="EMO"]/div[5]/button[1]')
driver.execute_script('arguments[0].click();', payButton)

# 결제확인 팝업 클릭
time.sleep(3)   # 여기 'AnySign' 이라는 보안 팝업과 관련된 문제가 해결되지 않아 어쩔 수 없이 delay를 줌.
pyautogui.moveTo(821, 339)
pyautogui.click()

# 팝업 대기 및 처리
try:
    alert = driver.switch_to.alert
    alert.accept()  # 팝업 확인 버튼 클릭
    # alert.dismiss()  # 팝업 취소 버튼 클릭 (필요한 경우)
except:
    print("No alert present.")

# 결제 성공 확인 버튼 클릭
time.sleep(5)   # 여기 'AnySign' 이라는 보안 팝업과 관련된 문제가 해결되지 않아 어쩔 수 없이 delay를 줌.
pyautogui.moveTo(889, 629)
pyautogui.click()

###########################################################
# "미열람/미발급 보기" page
wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Lcontent"]/form[1]/div[5]/table/tbody/tr[2]/td[11]/button')))
open_Button = driver.find_element(By.XPATH, '//*[@id="Lcontent"]/form[1]/div[5]/table/tbody/tr[2]/td[11]/button')
driver.execute_script('arguments[0].click();', open_Button)

try:
    alert = driver.switch_to.alert
    alert.accept()  # 팝업 확인 버튼 클릭
    # alert.dismiss()  # 팝업 취소 버튼 클릭 (필요한 경우)
except:
    print("No alert present.")

pyautogui.moveTo(889, 629)
pyautogui.click()

# position = pyautogui.position()
# print(position)






time.sleep(2000)