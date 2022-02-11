
#%%
from selenium import webdriver

# selenium에서 사용할 웹 드라이버 절대 경로 정보
chromedriver = './chromedriver.exe'
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver = webdriver.Chrome(chromedriver)
# driver로 특정 페이지를 크롤링한다.
driver.get('https://movie.naver.com/movie/bi/mi/basic.naver?code=144906')
# %%
man = driver.find_element_by_css_selector('#actualGenderGraph > svg > text:nth-child(4) > tspan').text
woman = driver.find_element_by_css_selector('#actualGenderGraph > svg > text:nth-child(6) > tspan').text

# %%
try:
    man = driver.find_element_by_css_selector('#actualGenderGraph > svg > text:nth-child(4) > tspan').text
    woman = driver.find_element_by_css_selector('#actualGenderGraph > svg > text:nth-child(6) > tspan').text

except:
    man = '데이터 없음'
    woman = '데이터 없음'
    
