import os
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
MAIN_URL = 'https://www.douyu.com/'
LOGIN_URL = 'https://www.douyu.com/member/oauth/signin/weibo?biz_type=1&ref_url=https%3A%2F%2Fwww.douyu.com%2F&room_id=0&cate_id=0&tag_id=0&child_id=0&vid=0&fac=&type=login'
APP_PATH = r"C:\Users\Administrator\AppData\Roaming\360se6\Application\360se.exe"
DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"drivers\chromedriver_for_360.exe")
collect_dict = dict()
firstpage_symbol = True


def query_data(url):
	req = requests.get(url, headers=HEADERS)
	req_dict = req.json()
	detail_dict = {i['roomId']: (i['nickname'], i['roomName']) 
		for i in req_dict['data'] 
		if ("cdk" not in i['roomName'].lower() and 
			"激活码" not in i['roomName'] and 
			"禁言" not in i['roomName'] and 
			"曲" not in i['roomName'] and 
			"歌" not in i['roomName'] and 
			"照片" not in i['roomName'] and 
			"写真" not in i['roomName'] and 
			"0.5" not in i['roomName'] and 
			"一元" not in i['roomName'] and 
			amount_ana(i['roomName']))
		}
	collect_dict.update(detail_dict)


def start_par(browser):
	global firstpage_symbol
	print(collect_dict)
	for key, value in collect_dict.items():
		if firstpage_symbol:
			browser.get(MAIN_URL+str(key))
			browser.get(MAIN_URL)
			browser.get(MAIN_URL+str(key))
			firstpage_symbol = False
		else:
			browser.get(MAIN_URL+str(key))
		try:
			browser.find_element_by_css_selector('[class="UPlayerLotteryEnter is-active "]').click()
			browser.find_element_by_css_selector('[class="ULotteryStart-joinBtn  "]').click()
			print("参与成功！ 房间号: %s 抽奖内容: %s" % (key, value[1]))
		except:
			try:
				tag_value = browser.find_element_by_class_name('ULotteryStart-joinBtnText')
				if "已成功参与" in tag_value.text:
					print("已成功参与！ 房间号: %s" % (key))
			except:
				print("此房间抽奖已结束！ 房间号: %s" % (key))
		time.sleep(2)


def amount_ana(stn):
	res = r"\d{1}.*?\d{0,3}"
	result = re.findall(res, stn)
	if result:
		if float(result[0]) > 8: # 匹配到数字，判断其是否大于 8
			return True # 大于 8 则参与
		else:
			return False 
	else:
		return True # 如果未匹配到数字一律参与


def main():
	global collect_dict
	url = "https://www.douyu.com/japi/weblist/apinc/rec/lottery?num=4&page=%s"
	for i in range(1, 7):
		query_data(url % i)
	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = APP_PATH
	chrome_options.add_argument(r'--lang=zh-CN')
	browser = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
	browser.implicitly_wait(13)
	try:
		while True:
			browser.get(LOGIN_URL)
			browser.find_element_by_id("userId").send_keys("your_userid")  # 账号
			browser.find_element_by_id("passwd").send_keys("your_password") # 密码
			time.sleep(2)  # 账号输入延迟
			browser.find_element_by_css_selector('[class="WB_btn_login formbtn_01"]').click()
			time.sleep(5)  # 登录检测延迟
			if "斗鱼" in browser.title:
				print("登录成功！")
				break
	except:
		print("登录点击已生效！")
	while True:
		start_par(browser)
		print("暂停抽奖 1 分钟")
		collect_dict = dict()
		time.sleep(55)
		for i in range(1, 7):
			query_data(url % i)
	# browser.quit()


if __name__ == '__main__':
	main()