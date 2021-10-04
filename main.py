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

startCpu = time.perf_counter()
start = time.time()

# 全局变量，保存着登录后的cookie信息
session = requests.Session()
session.cookies = http.cookiejar.LWPCookieJar('cookie')

""" 设置登录用方法所需Headers参数 """
headers = loadJson('config/requestConfig.json')["headers"]
session.headers = headers
# 实例化登录器，触发登录操作
# 更新session，保存更新后响应值
login = Login(session)
session = login.session
loginResponse = login.response

# 获取四位一体课表链接
swytUrlText = GetUrlData(headers, session).getSwytUrl()
# 获取教务处链接
jwcUrlText = GetUrlData(headers, session).getJwcUrl()
# 获取教学周
computedWeek = GetWeek(session, headers, jwcUrlText)
week = computedWeek.getFirstDay()

# # 批量创建链接池
createUrlPool = CreateUrlPool(swytUrlText)
createUrlPool.createUrlObject()
urlPools = createUrlPool.urlPoolResult
# # 启动多线程并发控制
getHtmlBus = GetHtmlBus(headers, session)
getHtmlBus.bus(urlPools, week)

end = time.time()
endCpu = time.perf_counter()
print('程序执行时间: ',end - start)
print('CPU执行时间: ',endCpu - startCpu)