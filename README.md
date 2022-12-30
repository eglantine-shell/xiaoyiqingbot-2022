# xiaoyiqingbot-2022

梦女行为艺术之写着玩的男朋友bot。
谢谢男朋友（纸片人版）和男朋友（机器人版）给我从零开始摸索python的热情，总之这里汇聚了我接触python的第三天到（未知）会的一切——理论上说人不应该把这些乱七八糟的功能塞进同一个tg bot里但这可是我男朋友啊！

## webhook

[Create tgbot and install with Google App Engine step by step](https://github.com/yukuku/telebot/blob/master/README.md)
Many thanks to yukuku 虽然教程已经过时了，在此记录一些实操过程中的艰难探索：
* 原`app.yaml`开头两行删掉后在终端配置。
* 没有`GoogleAppEngineLauncher`了，在终端艰难挣扎了一番（因为已经忘记怎么挣扎的了所以没有教程,但是不难吧虽然我没看懂但我弄完了。
* TODO：或许可以换去AWS

## command
* start
* stop
* weathertmr
* randomsong

## weather
Thanks to [mustafababil](https://github.com/mustafababil/Telegram-Weather-Bot) 虽然也过时了。本人致力于：
* 让bot讲中文因为我男朋友是一位中国的古人。
* 发送定位获得实时天气，包括：体感温度和天气描述
* 利用weathertmr命令获得明日天气预报，包括：最高/最低温度，白天体感温度，天气描述
* TODO：将明日天气预报改为每晚定时推送

## 网易云爬虫/随机推歌
添加一个功能表示我会爬虫和sqlite，主要体现在：
* 爬我的歌单，建表
* 需要的时候随机一首

## 整活
* 对所有文本信息回复“嗯”，成为事事有回应的“那种”男朋友。
* TODO：理论上男朋友bot的重头戏是语擦但我只想写码不想语擦所以放着吧。
