from datetime import date, datetime, timedelta
import math
from webbrowser import get
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage
import requests
import os
import random
import re

nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d") #今天的日期

# 开始日正数
start_date = os.getenv('START_DATE')
city = os.getenv('CITY')
# 生日，最终日倒数
# birthday = os.getenv('BIRTHDAY')
end_date = os.getenv('END_DATE')

app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')

user_ids = os.getenv('USER_ID', '').split("\n")
template_id = os.getenv('TEMPLATE_ID')

if app_id is None or app_secret is None:
  print('请设置 APP_ID 和 APP_SECRET')
  exit(422)

if not user_ids:
  print('请设置 USER_ID，若存在多个 ID 用回车分开')
  exit(422)

if template_id is None:
  print('请设置 TEMPLATE_ID')
  exit(422)

# weather 直接返回对象，在使用的地方用字段进行调用。
def get_weather():
  if city is None:
    print('请设置城市')
    return None
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  if res is None:
    return None
  weather = res['data']['list'][0]
  return weather

# 获取当前日期为星期几
def get_week_day():
  week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
  week_day = week_list[datetime.date(today).weekday()]
  return week_day

# 各种正数日
def get_memorial_days_count(aim_date):
  if aim_date is None:
    print('没有设置 开始日')
    return 0
  delta = today - datetime.strptime(aim_date, "%Y-%m-%d")
  return delta.days

# 各种倒计时
def get_counter_left(aim_date):
  if aim_date is None:
    return 0

  # 为了经常填错日期的同学们
  if re.match(r'^\d{1,2}\-\d{1,2}$', aim_date):
    next = datetime.strptime(str(date.today().year) + "-" + aim_date, "%Y-%m-%d")
  elif re.match(r'^\d{2,4}\-\d{1,2}\-\d{1,2}$', aim_date):
    next = datetime.strptime(aim_date, "%Y-%m-%d")
    next = next.replace(nowtime.year)
  else:
    print('日期格式不符合要求')
    
  if next < nowtime:
    next = next.replace(year=next.year + 1)
  return (next - today).days

# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def format_temperature(temperature):
  return math.floor(temperature)

# 随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

# 返回一个数组，循环产生变量
# def split_birthday():
#   if birthday is None:
#     return None
#   return birthday.split('\n')

# 对传入的多个日期进行分割
def split_dates(aim_dates):
  if aim_dates is None:
    return None
  return aim_dates.split('\n')

weather = get_weather()
if weather is None:
  print('获取天气失败')
  exit(422)
data = {
  # 城市
  "city": {
    "value": city,
    "color": get_random_color()
  },
  # 今天日期
  "date": {
    "value": today.strftime('%Y年%m月%d日'),
    "color": get_random_color()
  },
  # 今天周几
  "week_day": {
    "value": get_week_day(),
    "color": get_random_color()
  },
  # 天气状况
  "weather": {
    "value": weather['weather'],
    "color": get_random_color()
  },
  # 湿度
  "humidity": {
    "value": weather['humidity'],
    "color": get_random_color()
  },
  # 风力
  "wind": {
    "value": weather['wind'],
    "color": get_random_color()
  },

  "air_data": {
    "value": weather['airData'],
    "color": get_random_color()
  },
  # 空气质量
  "air_quality": {
    "value": weather['airQuality'],
    "color": get_random_color()
  },
  # 温度
  "temperature": {
    "value": math.floor(weather['temp']),
    "color": get_random_color()
  },
  # 最高温
  "highest": {
    "value": math.floor(weather['high']),
    "color": get_random_color()
  },
  # 最低温度
  "lowest": {
    "value": math.floor(weather['low']),
    "color": get_random_color()
  },
  # 正计时
  # "having_day": {
  #   "value": get_memorial_days_count(),
  #   "color": get_random_color()
  # },
  # 每日一言
  "words": {
    "value": get_words(),
    "color": get_random_color()
  },
  # 倒计时
  # "endday_left": get_counter_left,
  # "color": get_random_color()
}

# 倒计时添加到数据
for index, aim_date in enumerate(split_dates(end_date)):
  key_name = "endday_left"
  if index != 0:
    key_name = key_name + "_%d" % index
  data[key_name] = {
    "value": get_counter_left(aim_date),
    "color": get_random_color()
  }

# 各种正计时
for index, aim_date in enumerate(split_dates(start_date)):
  key_name = "having_day"
  if index != 0:
    key_name = key_name + "_%d" % index
  data[key_name] = {
    "value": get_memorial_days_count(aim_date),
    "color": get_random_color()
  }

if __name__ == '__main__':
  try:
    client = WeChatClient(app_id, app_secret)
  except WeChatClientException as e:
    print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
    exit(502)

  wm = WeChatMessage(client)
  count = 0
  try:
    for user_id in user_ids:
      print('正在发送给 %s, 数据如下：%s' % (user_id, data))
      res = wm.send_template(user_id, template_id, data)
      count+=1
  except WeChatClientException as e:
    print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
    exit(502)

  print("发送了" + str(count) + "条消息")
