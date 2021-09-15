import requests
from selenium import webdriver

""" 教学周所在的Xpath路径
    /html/body/div/div[2]/div[1]/div[1]/div/div/span
    //*[@id="calendar_contain"]/div/span """

class GetWeek:
    def __init__(self, session, jwcUrlText):
        self.seleniumUrl = 'https://webvpn.ppsuc.edu.cn%s' % (jwcUrlText)
        self.session = session
        
    def webdriverRun(self):
        """ 启动Selenium浏览器线程，返回当前教学周 """
        webapi = webdriver.Chrome()
        # 全局等待10min
        webapi.implicitly_wait(10)
        webapi.get(self.seleniumUrl)
        # 更新cookies
        webapi.delete_all_cookies()
        webapi = self.cookiesConver(webapi)
        # 获取节点数据
        webapi.get(self.seleniumUrl)
        weekElement = webapi.find_element_by_xpath('//*[@id="calendar_contain"]/div/span')
        result = weekElement.text
        webapi.quit()
        return int(result)

    def cookiesConver(self, webapi):
        """ cookies转换
            将Requests中的会话同步到Selenium
        """
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        # 获取requests侧的cookies
        for key in cookies.keys(): 
            # 向selenium侧传入以requests侧cookies的name为键value为值的字典
            webapi.add_cookie( {  'name': key,
                                  'value': cookies.get(key)})
        return webapi