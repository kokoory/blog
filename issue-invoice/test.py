# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
import time
from time import gmtime, strftime
import datetime
import autoit
import invoice

invo = invoice.IssueInvoice()
print invo.dt.strftime("%Y.%m.%d.%H:%M:%S") + " - issue invoice"

print invo.login()
print invo.customer_info("1234567890", "서비스", "서비스", "17")

item = "품목명을 넣어주세요"
print invo.service_info("0", "17", item, "50000000")

print invo.issue()
print invo.exit()
