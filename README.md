# Emotion-Analysis-Project

## 软件工程作业博客链接如下：
* [团队作业1——团队展示&选题](https://www.cnblogs.com/doublettian75/p/18486470)
* [团队作业2——《需求规格说明书》](https://www.cnblogs.com/doublettian75/p/18508828)
* [团队作业3——需求改进&系统设计](https://www.cnblogs.com/doublettian75/p/18525034)
* [团队作业4——项目冲刺集合贴](https://www.cnblogs.com/doublettian75/p/18535611)
* [团队作业5——测试与发布（Alpha版本）](https://www.cnblogs.com/doublettian75/p/18555487)

### 队名：p人大联盟

|队员|学号|
| :----: | :----: |
|张颢严|3222004426|
|王睿娴|3222003968|
|潘思言|3222004423|
|梁恬（组长）|3222004467|

<br>

### 团队项目描述
##### 随着社交媒体和在线评论平台的迅猛发展，用户在社交网络、电子商务网站、论坛等平台上发布了大量的文本评论和反馈。

##### 微博情感分析系统致力于帮助用户更全面更方便地了解微博舆论的情感倾向。在此系统中，用户输入想要查询的微博关键词，然后据此关键词，系统取相关微博评论，并对评论进行情感极性分析，最后给出舆论对于该话题关键词的总词云图、正面情感词云图、负面情感词云图和情感分布饼状图。在分析完成后，用户可点击按钮选择跳转到AI建议模块，询问A对此舆情分析结果的建议，建议文本已预先填好在输入框中。

<br>

## <font color="#008B8B"><font size="4"><font face="微软雅黑">**安装开始使用方法**</font></font></font>
#### 配置硬软件环境(目前只有以下环境能够在一定程度上确保正常使用开发的软件)
* 在Windows 11操作系统中，安装配置适合Windows 11操作系统的[Python 3.11](https://www.python.org/downloads/),[PyCharm 2023.3.3（Community Edition）](https://www.jetbrains.com/pycharm/download/?section=windows)
* 安装配置教程可参考：[Python 3.11 安装教程](https://blog.csdn.net/weixin_41989626/article/details/140155419)，[PyCharm 2023.3.3 Community Edition 安装教程](https://blog.csdn.net/killer_queen2Y/article/details/134893821)
#### （2）下载解压软件
* 下载并解压[软件压缩包](https://github.com/TheteamofP/Emotion-Analysis-Project/blob/main/Emotion-Analysis.zip)
#### （3）设置编码与运行配置
* 用PyCharm打开解压的软件文件夹中的Emotion-Analysis pycharm项目文件夹，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127205308084-1800070027.png)
* 在PyCharm中键盘输入快捷键“ctrl+alt+s”打开设置，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241128131924486-1378022731.png)
* 在设置的搜索中输入“控制台”，将“默认编码”设置为“UTF-8”，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241128174454263-831096276.png)
* 打开运行/调试配置，添加新配置，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127205448740-1103701956.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127205546193-313892342.png)
* 在新配置的运行中选择下载的Python 3.11文件夹中的python.exe，并选择Emotion-Analysis pycharm项目文件夹中的app.py文件作为脚本，并替换原本的环境变量为：`OPENAI_API_KEY=sk-02HUIWUOSRHjsGaKTSHFgjAWPZPNKBla7SrrlwPt05hqhOnK;OPENAI_API_BASE=https://api.chatanywhere.tech`，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210002025-1652102826.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210028722-787264789.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210114432-704720719.png)，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210139728-706422809.png)
#### （4）开始使用，启动项目
* 点击“应用”和“运行”，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210302713-1421464545.png)
* 点击运行界面中的网址，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210405325-1976859148.png)
* 默认浏览器将出现“情感分析系统”网页，即可开始使用软件，如图：![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127210507689-552850144.png)
* 如果想要停止使用，则关闭“情感分析系统”网页，如下图软件终止程序，关闭Pycharm应用即可，![](https://img2024.cnblogs.com/blog/3509240/202411/3509240-20241127211117906-8573518.png)
