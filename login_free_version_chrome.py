import os
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
MAIN_URL = 'https://www.douyu.com/'
DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"drivers\chromedriver.exe")
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
			time.sleep(2) # 重载刷掉超级粉丝团动态页面
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
	profile_directory = r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
	chrome_options.add_argument(profile_directory)
	chrome_options.add_argument(r'--lang=zh-CN')
	browser = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
	browser.implicitly_wait(13)
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