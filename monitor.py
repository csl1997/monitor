import requests, json, time
import smtplib, ssl
from email.mime.text import MIMEText
from email.utils import formataddr

item_id_5600x = '183432'
item_id_3080_1 = '182755'
item_id_3080_2 = '181354'
item_id_3080_3 = '181354'
item_id_3080_4 = '125953'
url = 'https://www.canadacomputers.com/product_info.php?ajaxstock=true&itemid='
url_5600x = 'https://www.canadacomputers.com/product_info.php?cPath=4_64_1969&item_id=183432'
url_3080_1 = 'https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=182755'
url_3080_2 = 'https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=181354'
url_3080_3 = 'https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=181353'
url_3080_4 = 'https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=181348'
headers = {"Cookie": "preferloc=MISS;"}

user = 'chensilun1997@gmail.com'

def get_html_info(url):
    response = requests.get(url, headers = headers)
    j = json.loads(response.text)
    return j

def judge(content):
    if type(content["avail"]) == str:
        amount = int(content["avail"].strip('+-'))
    else:
        amount = int(content["avail"])

    if amount == 0:
        try:
            amount = int(content["avail2"])
        except:
            pass
    
    return amount > 0

def email(item_name, content):
    sender = 'test@test.com'
    port = 465

    m = item_name + '有货啦。\n位置：' + content["loc"]
    m += '\n 链接：'
    if item_name == '5600x':
        m += url_5600x
    elif item_name == '3080_1':
        m += url_3080_1
    elif item_name == '3080_2':
        m += url_3080_2
    elif item_name == '3080_3':
        m += url_3080_3
    elif item_name == '3080_4':
        m += url_3080_4
    msg = MIMEText(m,'plain','utf-8')
    msg['From'] = formataddr(["Bot",sender])
    msg['To'] = formataddr(["补货提醒",user])
    msg['Subject'] = item_name + "补货提醒"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
        server.login('email@gmail.com', 'passord')
        server.sendmail(sender, user, msg.as_string())
        print('Email sent for ' + item_name)


def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec

if __name__ == '__main__':
	s = sleep_time(0, 3, 0)

	get_3080 = False
	get_5600x = True
	while True:
		res_5600x = get_html_info(url+item_id_5600x)
		res_3080_1 = get_html_info(url+item_id_3080_1)
		res_3080_2 = get_html_info(url+item_id_3080_2)
		res_3080_3 = get_html_info(url+item_id_3080_3)
		res_3080_4 = get_html_info(url+item_id_3080_4)

		if not get_5600x and judge(res_5600x):
			email('5600x', res_5600x)
			get_5600x = True
        
		if not get_3080 and judge(res_3080_1):
			email('3080_1', res_3080_1)
			get_3080 = True

		if not get_3080 and judge(res_3080_2):
			email('3080_2', res_3080_2)
			get_3080 = True

		if not get_3080 and judge(res_3080_3):
			email('3080_3', res_3080_3)
			get_3080 = True

		if not get_3080 and judge(res_3080_4):
			email('3080_4', res_3080_4)
			get_3080 = True
        
		time.sleep(s)