![qimai](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/qimai_logo.png)
# qimai_spider
七麦网站爬虫 (解决自动化登陆请求、破解请求签名算法、识别登陆验证码)

七麦是一个提供`AppStore`和全国各大安卓市场的数据的网站，感兴趣的朋友可以[官网](https://www.qimai.cn/)走一波

------
### ps: 2018-12-05 初始ReadMe，上传可用脚本

###     2018-12-06 完善ReadMe 除了识别验证码部分。
-------

1 . [反爬手段](#1-反爬手段)
- 1.1 [前端调试Debug](##1.1-前端调试Debug)
- 1.2 [自动登录流程分析](##1.2-自动登录流程分析)
- 1.3 [登录验证码识别](##1.3-登录验证码识别)
- 1.4 [请求签名](##1.4-请求签名)

2 . [反“反爬”手段](#2-反“反爬”手段)
- 2.1 [反前端调试Debug](##2.1-反前端调试Debug)
- 2.2 [自动登录流程分析](##2.2-自动登录流程分析)
- 2.3 [CNN登录验证码识别](##2.3-CNN登录验证码识别)
- 2.4 [JS请求签名逆向破解](##2.4-JS请求签名逆向破解)

3 . [参考资料](#3-参考资料)

4 . [使用](#4-使用)

# 1 反爬手段

## 1.1 前端调试Debug

首先，我们进入[七麦的首页](https://www.qimai.cn/)，使用`Chrome`打开`DevTool`，就会发现弹出`Debug`的页面。

![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/debug.png)

而且会跳到`source`这个`Tab`，

![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/qimai_source.png)

这就是典型的前端反调试，它是会根据某些条件判断你是否处于调试的状态，来不断的产生`Debug`，来阻断你调试的过程，最后由于`debug`对象不断堆积，导致浏览器崩溃。

## 1.2 自动登录流程分析

首先，我们进入七麦的[登录页面](https://www.qimai.cn/account/signin/r/%2)，我们再次打开`DevTools`，把选项卡切到`Network`tab，我们可以发现其实会产生3个`XHR`请求，这三个请求的时间都是有差别的，而且每个请求的响应都是如图所示，

![响应](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/%E5%93%8D%E5%BA%94.png)

会有成功的应答，因此我们可以分析，该登录流程是有先后请求的关系，经过后面的验证，确实是有请求的先后，不能直接一步登录。

![登录流程分析](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/%E7%99%BB%E5%BD%95%E6%B5%81%E7%A8%8B%E5%88%86%E6%9E%90.png)

## 1.3 登录验证码识别

到了很烦人的验证码，我们可以仔细看一下这个验证码，它的内容其实不是很复杂，特征还是比较明显的，关于它的具体破解我们之后再进行详细的分析，我们可以看看如何得到验证码的图片。

![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/%E9%AA%8C%E8%AF%81%E7%A0%81.png)

## 1.4 请求签名

![请求参数](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0.png)

如图所示，我们看之前登录流程中的某些请求在请求参数中会有这个字段的参数，我们具体找个`URL`来看一下，

以
`https://api.qimai.cn/rank/indexPlus/brand_id/1?analysis=IRIdEVEIChkIDF1USWkOFkofB0YADVNoWVQYCHZCBwdVAgFSBFFWB1ciGgA%3D`
这个地址为例，我们看到的是

![QQ截图20181206010532](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ截图20181206010532.png)

也就是请求签名的参数是`analysis`

# 2 反“反爬”手段

## 2.1 反前端调试Debug

![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/callstack.png)

我们根据之前的`Debug`,我们顺着右侧的`Call Stack`,找到产生这个代码的源文件，如图所示，就可以发现源代码如图所示，

![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/js.png)

![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/qimai_source.png)

这时我们可以把`js`文件下载下来，修改上图的代码为
```js
function t() {
  try {
    var a = "";
    !function e(n) {
      (1 !== ("" + n / n).length || 0 === n) && function() {}
      .constructor(a)(),
      e(++n)
    }(0)
  } catch (a) {
    setTimeout(t, 500)
  }
}
```
即可屏蔽掉debugger，或者我们可以暴力一点，直接
![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/t.png)
```js
t=function(){}
```

PS: 由于在分析七麦的网站时，它莫名的取消了前端反调试这个限制，所以大家在爬的时候可以放心的调试，有对于前端反调试感兴趣的同学可以私信我一些具体案例。

大家可以参考一下的文章：

https://segmentfault.com/a/1190000012359015

https://0x0d.im/archives/javascript-anti-debug-and-obfuscator.html

之后会具体出一些跟前端有关的反爬手段的解决。


## 2.2 自动登录流程分析

流程分析我们就是按之前的图顺序来发请求，具体可参考源码

## 2.3 CNN登录验证码识别



## 2.4 JS请求签名逆向破解

现在我们来一步步试着破解，以`analysis`为加密参数，我们下一个xhr断点，
也就是我们到该请求的`js`文件当中
![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206010836.png)，在右侧的`XHR Breakpoints`中添加一个适配项，拦截一个XHR请求，![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206010938.png)我们刷新页面进入断点的`js`文件，我们看到如图所示，![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206011020.png)接着我们顺着`Call Stack`寻找什么时候`analysis`参数被添加，我们发现这里还没有被添加![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206011144.png)，接着找，我们发现在这里的时候还没添加参数，![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206011313.png)下一步就有了参数，于是我们在这一步的`js`代码中寻找，我们发现了`interceptors`，也就是请求拦截器![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206012514.png)，我们打个断点，![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206012537.png)进入`interceptors`流中查看一下，![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206014306.png)即可发现主加密代码，如何寻找加密代码就是以上的流程，接下来，我们来分析一下具体的加密算法，我们可以发现，![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206014405.png)主要的使用的函数是`l.h`,`l.d`，我们直接在这两个函数上打断点，即可进入响应的算法，下面就是不断地下一跳了。![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206014647.png)![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206014750.png)![](https://github.com/AntiCrawlerSolution/qimai_spider/blob/master/static/QQ%E6%88%AA%E5%9B%BE20181206015000.png)


# 3 参考资料

1.参考了冷月大神的[《七麦加密破解》](https://lengyue.me/index.php/2018/10/15/qimai/)，做了些补充.

2.也参考了[不知名的大神](https://blowingdust.com/category/tech.html)的另一种分析方法.

3.感谢[nickliqian老哥的cnn识别](https://github.com/nickliqian/cnn_captcha)，推荐一波，有待大家的优化。

# 4 使用

具体使用：

（1）auto_login

```python
from auto_login.login_async import qimai_login_async
session = await qimai_login_async()
```
即可获取一个aiohttp.ClientSession对象

 (2) captcha_reconize

 使用方法可参考上面的`nickliqian`大神，另外加了一点自己的获取验证码图片的方法以及训练样本。
 
