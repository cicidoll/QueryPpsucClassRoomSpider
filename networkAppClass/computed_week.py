import re
import datetime
import math

class GetWeek:
    def __init__(self, session, headers, jwcUrlText):
        self.jwcUrl = 'https://webvpn.ppsuc.edu.cn%s' % (jwcUrlText)
        # 将传入的Headers和Session进行保存
        self.headers = headers
        self.session = session
        self.firstDate = ''
        
    def getFirstDay(self):
        ''' 获取教务处网页源代码 '''
        response = self.session.get(self.jwcUrl, headers = self.headers)
        # HTML内容
        html = response.text
        self.firstDate = self.regHtmlFirstDay(html)
        return self.computedWeek()

    def regHtmlFirstDay(self, inputString):
        ''' 匹配到当前学期的初始第一天 '''
        # JCalendar.tempFirstDay = "2021-9-6";
        pattern = re.compile(r'JCalendar.tempFirstDay = "(\d+-\d+-\d+)"')
        result = re.search(pattern, inputString).group(1)
        return result

    def computedWeek(self):
        ''' 计算当前教学周，参考时间2021-8-23周一 '''
        # 初始化变量类型为datetime
        initDate = datetime.datetime.strptime('2021-8-23', "%Y-%m-%d")
        firstDate = datetime.datetime.strptime(self.firstDate, "%Y-%m-%d")
        nowDate = datetime.datetime.today()
        # 开始计算
        initFirstDifference = (firstDate - initDate).days % 7
        initFirstDifference = 0 if initFirstDifference==0 else 7 - initFirstDifference
        firstNowDifference = (nowDate - firstDate).days - initFirstDifference
        if firstNowDifference<0: return 0
        week = math.ceil(firstNowDifference / 7) + 1
        return week