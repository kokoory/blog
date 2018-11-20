# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
import time
from time import gmtime, strftime
import datetime
import autoit

class IssueInvoice:


	def __init__(self):

		#get today
		self.dt = datetime.datetime.now()
		self.year = self.dt.strftime("%Y")
		self.month = self.dt.strftime("%m")
		self.day = self.dt.strftime("%d")

		#청구월 (이전달)
		self.first = self.dt.replace(day=1)
		self.last = self.first - datetime.timedelta(days=1)
		self.prevmonth = self.last.strftime("%m")

		#드라이버 세팅
		self.driver = webdriver.Chrome()
		self.driver.get('https://www.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml')
		self.main = self.driver.window_handles[0]

		#공인인증서 비밀번호를 넣어주세요
		self.pwd = " "
		time.sleep(3)
		
	def login(self):
		#로그인 페이지 이동 
		self.driver.find_element_by_id('group1543').click()

		time.sleep(5)

		for handle in self.driver.window_handles:
			self.driver.switch_to_window(self.main)

		#공인인증서 로그인 선택 
		iframe =self.driver.find_element_by_id('txppIframe')
		self.driver.switch_to.frame(iframe)
		self.driver.find_element_by_id('trigger38').click()

		iframe = self.driver.find_element_by_id('dscert')

		time.sleep(10)

		self.driver.switch_to.frame(iframe)

		#공인인증서 선택
		self.driver.find_element_by_xpath('//*[@title="인증서 이름"]')

		#패스워드 입력, 로그인 후 메인화면 진입 
		self.driver.find_element_by_id('input_cert_pw').send_keys(self.pwd)
		self.driver.find_element_by_id('btn_confirm_iframe').click()
		time.sleep(3)

		#전자세금계산서 발행 화면 
		self.driver.find_element_by_id('myMenuImg1').click()		
		time.sleep(5)

		dt = datetime.datetime.now()
		return dt.strftime("%Y.%m.%d.%H:%M:%S") + " -  complete login"

	def customer_info(self, regnumber,bizcondition,bizitem,day):
		for handle in self.driver.window_handles:
			self.driver.switch_to_window(self.main)
		
		#거래처 조회 클릭
		iframe = self.driver.find_element_by_id('txppIframe')
		self.driver.switch_to.frame(iframe)
		self.driver.find_element_by_id('grpBtnDmnrClplcInqrTop').click()

		time.sleep(3)

		#거래처 조회 상세화면 
		iframe =self.driver.find_element_by_id('clplcInqrPopup_iframe')
		self.driver.switch_to.frame(iframe)

		time.sleep(3)
		self.driver.find_element_by_id('group1381').click()
		self.driver.find_element_by_id('edtTxprDscmNoEncCntn').send_keys(regnumber)
		self.driver.find_element_by_id('btnSearch').click()

		time.sleep(3)
		self.driver.find_element_by_id('grdResult_cell_0_0').click()
		self.driver.find_element_by_id('grdResult_cell_0_0').click()

		self.driver.find_element_by_id('btnProcess').click()
			
		time.sleep(2)
		Alert(self.driver).accept()
		time.sleep(3)
		###거래처 선택 완료 

		iframe = self.driver.find_element_by_id('txppIframe')
		self.driver.switch_to.frame(iframe)

		#업태변경
		self.driver.find_element_by_id('edtDmnrBcNmTop').clear()
		self.driver.find_element_by_id('edtDmnrBcNmTop').send_keys(unicode(bizcondition,'utf-8'))
		self.driver.find_element_by_id('edtDmnrItmNmTop').clear()
		self.driver.find_element_by_id('edtDmnrItmNmTop').send_keys(unicode(bizitem,'utf-8'))

		#작성일자
		writingdate = self.year+self.month+day
		self.driver.find_element_by_id('calWrtDtTop_input').clear()
		time.sleep(1)
		self.driver.find_element_by_id('calWrtDtTop_input').send_keys(unicode(writingdate,'utf-8'))
		time.sleep(1)

		dt = datetime.datetime.now()
		return dt.strftime("%Y.%m.%d.%H:%M:%S") + " - complete writing customer information"

	def service_info(self, order, day,item, cost):

		################--여러개일 수 있음, 0부터 
		#품목일
		box = "genEtxivLsatTop_"+order+"_edtLsatSplDdTop"
		self.driver.find_element_by_id(box).click()
		self.driver.find_element_by_id(box).send_keys(day)

		#품목명
		box = "genEtxivLsatTop_"+order+"_edtLsatNmTop"
		self.driver.find_element_by_id(box).send_keys(unicode(item,'utf-8'))

		#규격,수량
		box = "genEtxivLsatTop_"+order+"_edtLsatRszeNmTop"
		self.driver.find_element_by_id(box).send_keys("1")

		box = "genEtxivLsatTop_"+order+"_edtLsatQtyTop"
		self.driver.find_element_by_id(box).send_keys("1")

		#단가
		box = "genEtxivLsatTop_"+order+"_edtLsatUtprcTop"
		self.driver.find_element_by_id(box).send_keys(cost)

		#공급가액, 세액은 클릭만 하면 자동계산
		box = "genEtxivLsatTop_"+order+"_edtLsatSplCftTop"
		self.driver.find_element_by_id(box).click()

		print "item : " + unicode(item, 'utf-8')
		dt = datetime.datetime.now()
		return dt.strftime("%Y.%m.%d.%H:%M:%S") + " - complete writing information"

	def issue(self):

		#발급
		self.driver.find_element_by_id('btnIsn').click()

		#iframe 전환, 전자세금계산서 발급 확인 팝업
		time.sleep(3)
		self.iframe = self.driver.find_element_by_id('UTEETZZA89_iframe')
		self.driver.switch_to.frame(self.iframe)

		#발급취소
		#self.driver.find_element_by_id('btnClose').click()

		#발급하기
		self.driver.find_element_by_id('trigger20').click()

		time.sleep(3)

		#서명취소
		##################################################################
		#ControlFocus("인증서 선택창", " ", "Edit2")
		#ControlSetText("인증서 선택창"," ", "Edit2", "인증서 비밀번호")
		#ControlClick("인증서 선택창", " ", "Button12")
		##################################################################		
		#autoit.run("C:\\work\\invoice\\test_sign.exe")
		
		#인증서 서명
		##################################################################
		#ControlFocus("인증서 선택창", " ", "Edit2")
		#ControlSetText("인증서 선택창"," ", "Edit2", "인증서 비밀번호")
		#ControlClick("인증서 선택창", " ", "Button11")
		##################################################################
		autoit.run("C:\\work\\invoice\\invoice_sign.exe")

		dt = datetime.datetime.now()
		return dt.strftime("%Y.%m.%d.%H:%M:%S") + " - complete issuing invoice"		

	def exit(self):
		self.driver.quit()

		dt = datetime.datetime.now()
		return dt.strftime("%Y.%m.%d.%H:%M:%S") + " - close all window"
