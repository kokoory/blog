# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import datetime

driver = webdriver.Chrome()
driver.get("https://www.gov.kr/portal/ntcItm")

soup = BeautifulSoup(driver.page_source, 'html.parser')
titles_dates = soup.find_all('td', {'class':'m-show'})

#새로운 공지사항의 여부를 체크하기 위해
new = False

#오늘 올라온 공지인지 날짜를 확인하기 위해
today = datetime.datetime.now()

#게시물은 하나보다 더 많을 수 있으니까. 없을 수도 있으니까.
for i in range(len(titles_dates)):
	# 인덱스 홀수는 날짜, 짝수(0포함)는 제목(링크)
	if i%2 == 0:
		continue

	# eraser html tag
	string_dates = titles_dates[i].text.strip()

	#convert to date type
	convert_to_date = datetime.datetime.strptime(string_dates, "%Y.%m.%d") 

    #게시일이 오늘날짜면 새로운 공지!
	if convert_to_date.strftime("%Y%m%d") == today.strftime("%Y%m%d"):
		new = True

        #새 공지 제목
	 	current_title = titles_dates[(i-1)]
        
        #새 공지사항의 본문 링크
	 	title_link = current_title.find('a')

	 	#새로운 공지사항의 내용을 보러가자
	 	driver.get("https://www.gov.kr"+title_link['href'])

        #새로운 페이지에 접속했으니 다시 한번 소스를 숲숲
	 	html = driver.page_source
	 	soup = BeautifulSoup(html, 'html.parser')
        
        #공지 내용은 클래스가 view-contents 인 div 태그 안에 있다
	 	content = soup.find('div',{'class':'view-contents'})
	 	print content.prettify()

# close driver
driver.quit()

if bool(new == False):
	print "새로운 공지사항이 없습니다."
