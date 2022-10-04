import time

class GetUrlData:
    # 四位一体课表链接所在path
    # swytUrlPath = '//*[@id="group-2"]/div[9]/div/div[3]/@data-redirect'
    def __init__(self, headers, session):
        # 将传入的Headers和Session进行保存
        self.headers = headers
        self.session = session
        # 获取当前13位时间戳
        self.millis = int(round(time.time() * 1000))

    
    def getSwytUrl(self):
        """ 获取四位一体课表链接 """
        # 设置请求头参数并请求网页
        url = 'https://webvpn.ppsuc.edu.cn/user/portal_groups?_=%s' % (self.millis)
        response = self.session.get(url, headers = self.headers)
        response_json = response.json()
        swytUrlText = response_json['data'][0]['resource'][7]['redirect']
        return swytUrlText

    
    def getJwcUrl(self):
        """ 获取教务处链接 """
        # 设置请求头参数并请求网页
        url = 'https://webvpn.ppsuc.edu.cn/user/portal_groups?_=%s' % (self.millis)
        response = self.session.get(url, headers = self.headers)
        response_json = response.json()
        jwcUrlText = response_json['data'][0]['resource'][5]['redirect']
        return jwcUrlText
