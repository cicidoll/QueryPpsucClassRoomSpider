import requests
import http.cookiejar
import time
from requests.api import get

from networkAppClass.login import Login
from networkAppClass.get_urldata import GetUrlData
from networkAppClass.computed_week import GetWeek
from networkAppClass.create_url_pool import CreateUrlPool
from networkAppClass.get_html import GetHtmlBus
from utils import loadJson

""" vpn_timestamp的单位是纳秒 有效时间应该是1h
    也有可能是时间戳,13位时间戳
    wrdrecordvisit要比vpn_timestamp早一些
    没有wrdrecordvisit参数，也能请求到数据 """

startCpu = time.perf_counter()  # perf_counter()返回当前的计算机系统时间
start = time.time()  # time time() 返回当前时间的时间戳（1970纪元后经过的浮点秒数）。

# 全局变量，保存着登录后的cookie信息
session = requests.Session()  # requests.session():维持会话,可以让我们在跨请求时保存某些参数
session.cookies = http.cookiejar.LWPCookieJar('cookie')  # cookie相关

""" 设置登录用方法所需Headers参数 """
headers = loadJson('config/requestConfig.json')["headers"]
session.headers = headers
# 实例化登录器，触发登录操作
# 更新session，保存更新后响应值
login = Login(session)  # 登陆
session = login.session
loginResponse = login.response

# 获取四位一体课表链接
# swytUrlText = GetUrlData(headers, session).getSwytUrl()
swytUrlText = "/http/77726476706e69737468656265737421a1a510d276693c1e2c59dae2c90476/swyt/index.php"
# 获取教务处链接
# jwcUrlText = GetUrlData(headers, session).getJwcUrl()
# 获取教学周
computedWeek = GetWeek(session, headers)
week = computedWeek.manual_getweek('2022-9-5')  # 这里需要手动输入一下这学期的第一天，然后就可以算出当前的周数了

# # 批量创建链接池
createUrlPool = CreateUrlPool(swytUrlText)
createUrlPool.createUrlObject()
urlPools = createUrlPool.urlPoolResult
# # 启动多线程并发控制
getHtmlBus = GetHtmlBus(headers, session)
getHtmlBus.bus(urlPools, week)

end = time.time()
endCpu = time.perf_counter()
print('程序执行时间: ', end - start)
print('CPU执行时间: ', endCpu - startCpu)
