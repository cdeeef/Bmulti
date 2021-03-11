import base64
import json
import requests
import time
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains


def base64_api(img, uname='你的用户名', pwd='你的密码'):
    """
    打码平台：http://www.kuaishibie.cn/user/index.html
    验证码识别接口
    :param uname: 快识别用户名
    :param pwd: 快识别密码
    :param img: 图片路径
    :return: 返回识别结果
    """

    base64_data = base64.b64encode(img)
    b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "image": b64, "typeid": 21}
    result = json.loads(requests.post("http://api.ttshitu.com/imageXYPlus", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


b_user = 'b站用户名'
b_passwd = 'b站密码'

driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://passport.bilibili.com/login')
u_input = driver.find_element_by_xpath('//*[@id="login-username"]')
p_input = driver.find_element_by_xpath('//*[@id="login-passwd"]')
u_input.send_keys(b_user)
time.sleep(1)
p_input.send_keys(b_passwd)
time.sleep(1)
l_btn = driver.find_element_by_xpath('//*[@class="btn btn-login"]')
l_btn.click()
time.sleep(2)
capcha_img = driver.find_element_by_xpath('//img[@class="geetest_item_img"]')
content = requests.get(capcha_img.get_attribute('src')).content
f = BytesIO()
f.write(content)
up_img = Image.open(f)
scale = [capcha_img.size['width'] / up_img.size[0],
         capcha_img.size['height'] / up_img.size[1]]
result = base64_api(content)
position = result.split('|')
position = [[int(j) for j in i.split(',')] for i in position]
for items in position:
    ActionChains(driver).move_to_element_with_offset(capcha_img, items[0] * scale[0], items[1] * scale[1]).click().perform()
    time.sleep(0.5)
btn = driver.find_element_by_xpath('//*[@class="geetest_commit_tip"]')
btn.click()
print(driver.get_cookies())

