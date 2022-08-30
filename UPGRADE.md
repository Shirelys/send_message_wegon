# 更新说明

## 2022.08.30

1. 支持多个生日（倒计时）了，理论上无限个。。但没必要，BIRTHDAY 字段用换行可以分隔不同的日期（兼容原有格式），模板中为了保持兼容没有改名字，所以第一行是 `birthday_left`，第二行开始依次是 `birthday_left_1`、`birthday_left_2` ......
2. 太多日期格式不匹配了。。兼容了 05-20、2022-05-20 两种格式。
3. 控制台输出加入输出的模板，发送成功，数据错误却不知道为什么的情况得到了解决。

示例模板：

今天是 {{ date.DATA }} {{ week_day.DATA }}

今天天气：{{ weather.DATA }}

湿度：{{ humidity.DATA }}

风向风力：{{ wind.DATA }}

空气指数：{{ air_data.DATA }}

空气质量：{{ air_quality.DATA }}

当前温度：{{ temperature.DATA }}

最低气温：{{ lowest.DATA }}

最高气温：{{ highest.DATA }}

我们已经相恋 {{ love_days.DATA }} 天啦

距离你的生日还有：{{ birthday_left.DATA }} 天

距离老子的生日还有：{{ birthday_left_1.DATA }} 天

距离墨子的生日还有：{{ birthday_left_2.DATA }} 天

距离韩非子的生日还有：{{ birthday_left_3.DATA }} 天

{{ words.DATA }}

## 2022.08.28

1. 增加星期几字段
2. 增加湿度、风向级、空气指数、空气质量字段

示例模板：

今天是 {{ date.DATA }} {{ week_day.DATA }}

今天天气：{{ weather.DATA }}

湿度：{{ humidity.DATA }}

风向风力：{{ wind.DATA }}

空气指数：{{ air_data.DATA }}

空气质量：{{ air_quality.DATA }}

当前温度：{{ temperature.DATA }}

最低气温：{{ lowest.DATA }}

最高气温：{{ highest.DATA }}

我们已经相恋 {{ love_days.DATA }} 天啦

距离你的生日还有：{{ birthday_left.DATA }} 天

{{ words.DATA }}

## 2022.08.24

1. 增加了城市字段（真的快变成天气预报了）

示例模板：

今天是 {{ date.DATA }}

城市：{{ city.DATA }}

今天天气：{{weather.DATA }}

当前温度：{{ temperature.DATA }}

最低温：{{ lowest.DATA }}

最高温：{{ highest.DATA }}

我们已经相恋 {{ love_days.DATA }} 天啦

距离你的生日还有：{{ birthday_left.DATA }} 天

{{ words.DATA }}

## 2022.08.22

1. 增加天气范围（最高温、最低温）
2. 支持多个接收人
3. 所有字段都是彩色的

示例模板：

今天是 {{ date.DATA }}

今天天气：{{weather.DATA }}

当前温度：{{ temperature.DATA }}

低温：{{ lowest.DATA }}

最高温：{{ highest.DATA }}

我们已经相恋 {{ love_days.DATA }} 天啦

距离你的生日还有：{{ birthday_left.DATA }} 天

{{ words.DATA }}
