from lxml import etree
from requests.sessions import session
import sys
sys.path.append(".")
from utils import loadJson

class Login:
    # 验证码图片ID所在path
    captchaPath = '//*[@id="captcha-wrap"]/div/div/input[1]/@value'
    # 验证码请求头参数
    headers = loadJson('config/requestConfig.json')["headers"]
    headers["Referer"] = 'https://webvpn.ppsuc.edu.cn/login'
    # 注册用数据
    loginData = loadJson('user.json')

    def __init__(self, session):
        # 保存session
        self.session = session
        self.response = ''
        # self.doLogin()
    
    """ 登录注册时，
      需要发送的验证码随机参数
      解析Html节点内容，返回str类型的参数 """
    def getSetCaptcha(self):
        # 设置请求头参数并请求网页
        url = 'https://webvpn.ppsuc.edu.cn/login'
        response = self.session.get(url, headers = self.headers)
        # HTML内容
        html = response.text
        htmlContent = etree.HTML(html)
        captchaText = htmlContent.xpath(self.captchaPath)[0]
        # 更新响应值
        self.loginData['captcha_id'] = captchaText

    """ 使用账号密码进行登录 """
    def doLogin(self):
        # 更新随机码参数
        self.getSetCaptcha()
        url = 'https://webvpn.ppsuc.edu.cn/do-login'
        response = self.session.post(url, data = self.loginData, headers = self.headers)
        self.response = response

login = Login('test')
print(login.headers)