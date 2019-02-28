from requests import session,Request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import csv,time,re,os

username = "yl1133"
password = ""

assert username, "username is empty!"
assert password, "password is empty!"
# ++++++++++++++使用说明+++++++++++++++++++++++++
# 1.pip install bs4'
# 2.按照下列字段，在jira筛选并保存筛选器
# 3.必填-filter/jira账号/jira密码/excel文件名'
# +++++++++++++++使用说明++++++++++++++++++++++++

root_url = "http://jira.yealink.com:8080"
excel_name = "TestCases.csv"#excel文件名
csv_file = open(excel_name,"w",newline='')
writer = csv.writer(csv_file)
writer.writerow(['项目','主题','用例链接','模块','状态'])
#writer.writerow(['项目','主题','bug链接','模块','经办人','创建时间','状态','严重程度','解决人','概率性故障','优先级','创建者','解决结果','关注人','bug打回次数','Developer','更新日期'])
# writer.writerow(['项目','主题','bug链接','模块','经办人','创建时间','状态','严重程度','解决人','概率性故障','优先级','创建者'])
# writer.writerow([project,summary,bug_url,components,assignee,created_time,status,bug_level,who_solve,gailv,priority,creator,resolution,watches,bugDahui,Developer,updated_time])
# writer.writerow(['主题','模块','经办人','用例级别','状态','PC自测结果','报告人','描述','测试用例类型'])
# writer.writerow([summary,bug_url,components,assignee,created_time,status,bug_level])
filter = '12849'#筛选器对应的序号

login_url="http://jira.yealink.com:8080/login.jsp"
# 创建session请求对象，保存登录会话请求u
session_req=session()
# 使用 Chrome Headless 替代PhantomJS
# 需要安装chromedriver，win可以使用choco install chromedriver 进行安装
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)
#PhantomJS是一个无界面的,可脚本编程的WebKit浏览器引擎。
# 它原生支持多种web 标准：DOM 操作，CSS选择器，JSON，Canvas 以及SVG
#driver = webdriver.PhantomJS()
driver.get(login_url)
#登录jira
driver.find_element_by_id('login-form-username').send_keys(username)#账号
driver.find_element_by_id("login-form-password").send_keys(password)#密码
driver.find_element_by_id("login-form-submit").click()
print("Login Success!")
#打开指定的筛选器界面
url = 'http://jira.yealink.com:8080/issues/?filter='+filter
driver.get(url)
time.sleep(2)
elem = driver.find_element_by_class_name("pagination")
table_source = elem.get_attribute('innerHTML')
#获取bug总数--从而计算出bug页数
bug_count = driver.find_element_by_css_selector('span.results-count-total.results-count-link').text
page_count = int(int(bug_count)/50)
link_list = []
for j in range(page_count+1):
    #根据bug页数，生成页面链接，bug数量一页50条
    link_list.append('/issues/?filter='+filter+'&startIndex='+str(j*50))
for link in link_list:
    page_link = root_url + link
    # 取得链接内容的源代码
    driver.get(page_link)
    time.sleep(5)
    current_url = driver.current_url
    print(current_url)
    # 获取链接界面的bug表格所有行元素
    data = driver.find_element_by_id("issuetable").\
        find_elements_by_tag_name("tr")
    data = data[1:]
    for i in range(len(data)):#issuerow52811 > td.summary#issuerow52811 > td.summary > p > a
        #遍历所有行元素，获得bug：主题，模块，经办人，创建时间，状态，严重程度，bug链接，'解决人','概率性故障','优先级'
        # +++++++++++++++++++++++++测试用例抓取+++++++++++++++++++++++++++++++
        # summary = data[i].find_element_by_css_selector("td.summary > p > a").text
        # components = data[i].find_element_by_css_selector("td.components").text
        # assignee = data[i].find_element_by_css_selector("td.assignee > span").text
        # level = data[i].find_element_by_css_selector("td.customfield_11310").text
        # status = data[i].find_element_by_css_selector("td.status > span").text
        # PC_zice = data[i].find_element_by_css_selector("td.customfield_11800").text
        # reporter = data[i].find_element_by_css_selector("td.reporter > span").text
        # description = data[i].find_element_by_css_selector("td.description").text
        # casetype = data[i].find_element_by_css_selector("td.customfield_11503").text
        # +++++++++++++++++++++++++测试用例抓取+++++++++++++++++++++++++++++++
        #遍历所有行元素，获得bug：主题，模块，经办人，创建时间，状态，严重程度，bug链接，'解决人','概率性故障','优先级'
        summary = data[i].find_element_by_css_selector("td.summary > p > a").text
        components = data[i].find_element_by_css_selector("td.components").text
        #assignee = data[i].find_element_by_css_selector("td.assignee > span").text
        # level = data[i].find_element_by_css_selector("td.customfield_11310").text
        # status = data[i].find_element_by_css_selector("td.status > span").text
        # level = data[i].find_element_by_css_selector("#reporter_yl1198").text
        # assignee = data[i].find_element_by_css_selector("td.assignee").text
        #created_time = data[i].find_element_by_css_selector("td.created").text
        status = data[i].find_element_by_css_selector("td.status").text
        #bug_level = data[i].find_element_by_css_selector("td.customfield_11201").text
        # # bug_level = data[i].find_element_by_css_selector("td.customfield_11201").text
        bug_url = data[i].find_element_by_css_selector("td.summary > p > a").get_attribute('href')
        #who_solve = data[i].find_element_by_css_selector("#user_cf_admin").text
        #who_solve = data[i].find_element_by_css_selector("td.customfield_11903").text#解决人
        #gailv = data[i].find_element_by_css_selector("td.customfield_11308").text#概率性故障
        #priority = data[i].find_element_by_css_selector("td.priority > img").text#优先级
        #creator = data[i].find_element_by_css_selector("td.creator").text#创建者
        #resolution = data[i].find_element_by_css_selector("td.resolution").text#解决结果
        #watches = data[i].find_element_by_css_selector("td.watches").text#关注人
        #bugDahui = data[i].find_element_by_css_selector("td.customfield_11316").text#bug打回
        #Developer = data[i].find_element_by_css_selector("td.customfield_10600").text#Developer
        #updated_time = data[i].find_element_by_css_selector("td.updated > span > time").text#Developer
        project = data[i].find_element_by_css_selector("td.project").text#项目
        # # who_solve = data[i].find_element_by_css_selector("#user_cf_admin").text
        # # who_solve = data[i].find_element_by_css_selector("#user_cf_admin").text
        # writer.writerow([project,summary,components,assignee,level,status,PC_zice,reporter,description,casetype])
        #writer.writerow([project,summary,bug_url,components,assignee,created_time,status,bug_level,who_solve,gailv,priority,creator,resolution,watches,bugDahui,Developer,updated_time])
        writer.writerow([project,summary,bug_url,components,status])
    print('success')
csv_file.close()
