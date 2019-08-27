# ManhuaguiPyCrawler
用Python爬取漫画柜的漫画
## 开发环境
- 操作系统: Win10
- 编辑器: VS Code
- 编程语言: Python3
- Python第三方库: requests, selenium, bs4, lxml
- 安装[Chrome](https://www.google.cn/intl/zh-CN/chrome/)和对应的[Chrome Driver](http://npm.taobao.org/mirrors/chromedriver/), 并把Chrome Driver的路径放在环境变量Path里, 后者具体可参考[如何快速下载、安装和配置chromedriver?](https://jingyan.baidu.com/article/f7ff0bfcdd89ed2e27bb1379.html)
## 实现原理
用Python+Selenium操作Chrome浏览器, 进行漫画网站的浏览, 按钮点击等, 从而将目标漫画一页一页地下载到本地. 
## 优点
能有效地下载那些异步加载的图片(大多数漫画网站都是采取这种方式加载图片).
## 缺点
程序运行的时候会自动打开一个Chrome窗口, 因此会占用比较多的系统资源. 
## 注意
漫画柜有时候会因为迷之因素而上不去, 记得挂上VPN.
## TODO
下一步想分析生成图片资源url的JavaScript代码, 从而直接找到图片资源的真实地址, 这样不用开浏览器, 少占用资源, 也能加快下载速度. 
