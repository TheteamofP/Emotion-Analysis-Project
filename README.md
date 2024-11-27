# Emotion-Analysis-Project

# [测试与发布（Alpha版本）](https://www.cnblogs.com/doublettian75/p/18555487)

### 队名：p人大联盟

|队员|学号|
| :----: | :----: |
|张颢严|3222004426|
|王睿娴|3222003968|
|潘思言|3222004423|
|梁恬（组长）|3222004467|

<br>

### 团队项目描述
##### 随着社交媒体和在线评论平台的迅猛发展，用户在社交网络、电子商务网站、论坛等平台上发布了大量的文本评论和反馈。微博情感分析系统致力于帮助用户更全面更方便地了解微博舆论的情感倾向。在此系统中，用户输入想要查询的微博关键词，然后据此关键词，系统取相关微博评论，并对评论进行情感极性分析，最后给出舆论对于该话题关键词的总词云图、正面情感词云图、负面情感词云图和情感分布饼状图。在分析完成后，用户可点击按钮选择跳转到AI建议模块，询问A对此舆情分析结果的建议，建议文本已预先填好在输入框中。

<br>

## <font color="#008B8B"><font size="4"><font face="微软雅黑">**安装开始使用方法**</font></font></font>
#### 配置硬软件环境(目前只有以下环境能够在一定程度上确保正常使用开发的软件)
* 在Windows 11操作系统中，安装配置适合Windows 11操作系统的[Python 3.11](https://www.python.org/downloads/),[PyCharm 2023.3.3（Community Edition）](https://www.jetbrains.com/pycharm/download/?section=windows)
* 安装配置教程可参考：[Python 3.11 安装教程](https://blog.csdn.net/weixin_41989626/article/details/140155419)，[PyCharm 2023.3.3 Community Edition 安装教程](https://blog.csdn.net/killer_queen2Y/article/details/134893821)
#### 下载解压软件
* 下载并解压[软件压缩包](https://github.com/TheteamofP/Emotion-Analysis-Project/blob/main/Emotion-Analysis.zip)
#### 配置运行配置
* 用PyCharm打开解压的软件文件夹中的Emotion-Analysis pycharm项目文件夹，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127205308084-1800070027.png)
* 打开运行/调试配置，添加新配置，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127205448740-1103701956.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127205546193-313892342.png)
* 在新配置的运行中选择下载的Python 3.11文件夹中的python.exe，并选择Emotion-Analysis pycharm项目文件夹中的app.py文件作为脚本，并替换原本的环境变量为：`OPENAI_API_KEY=sk-02HUIWUOSRHjsGaKTSHFgjAWPZPNKBla7SrrlwPt05hqhOnK;OPENAI_API_BASE=https://api.chatanywhere.tech`，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210002025-1652102826.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210028722-787264789.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210114432-704720719.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210139728-706422809.png)
#### 开始使用，启动项目
* 点击“应用”和“运行”，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210302713-1421464545.png)
* 点击运行界面中的网址，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210405325-1976859148.png)
* 默认浏览器将出现“情感分析系统”网页，即可开始使用软件，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210507689-552850144.png)
* 如果想要停止使用，则关闭“情感分析系统”网页，如下图软件终止程序，关闭Pycharm应用即可，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127211117906-8573518.png)
#### 提示
* “话题分析”得出结果的时间难以预测，关键词越普遍，时间长度越长，收集时间越长，请耐心等待
* “话题分析”得出分析结果后点击最下方的“点击查看AI助手建议”可跳转至AI建议，发送“输入信息”框已有的内容，即可得到AI对分析结果的结论与建议
* “AI建议”的AI能接收并正确处理恢复的信息最多只能输入1600个中文字符
* 在“情感分析系统”网页中分析得到的词云图和分布扇形图将保存在Emotion-Analysis pycharm项目文件夹的result文件夹中，可按需取用
* 点击网页背景部分会返回首页，此时正在进行的“话题分析”或“AI建议”不会因此停止或消失
#### *“话题分析”中需要输入的Cookie的获取方法
  * 打开[微博网址](https://weibo.cn/)
  * 点击“登录”，登录微博，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127120405248-1317957418.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127120433691-16150431.png)
  * 登录微博后，在[微博网址](https://weibo.cn/)打开浏览器的开发者工具，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241126133431144-2078678274.png)
  * 保持开发者工具打开，点击“下页”，见图红框：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241126133531453-814568252.png)
  * 选择开发者工具的网络Network，选择Name列表中的第一项，在左侧的请求头Request Headers中找到Cookie对应右侧的值即为需要输入分析系统的Cookie，见下图红框：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241126134135765-1991210342.png)
