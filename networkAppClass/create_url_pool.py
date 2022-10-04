from urllib import parse
import sys

sys.path.append(".")
from utils import loadJson

# 拼接字符串模板
ZHUJIAN = "{}?{}&jxcdmc=%27%CD%C5%D6%FD%BD%A3%C2%A5{}%27"
ZHONG = "{}?{}&jxcdmc=%27%CD%C5%D3%FD%BE%AF%D6%D0%C2%A5{}%27"
XIPEI = "{}?{}&jxcdmc=%27%CD%C5%D3%FD%BE%AF%CE%F7%C2%A5{}%27"

# 拼接字符串具体填充对象
PARSEURLENCODE = {
    "zhuJian": ZHUJIAN,
    "zhongLou": ZHONG,
    "XiPei": XIPEI
}

# 2021-9-12更新
# 发现四位一体课表查询链接中，原index.php更换为jxcdkbcx.php
OLDPHP = "index.php"
NEWPHP = "jxcdkbcx.php"


# 批量创建链接池
class CreateUrlPool:
    def __init__(self, swytUrlText: str = ''):
        # 初始化参数
        self.swytUrlText = swytUrlText
        self.urlPoolResult = []
        self.requestsUA: dict = loadJson('config/requestConfig.json')
        self.createUrlDic: dict = loadJson('config/createUrlDic.json')["urlDic"]
        self.classRoomNumConfig: dict = loadJson('config/classRoomNumConfig.json')
        self.classRoomsNumLists: dict = self.classRoomNumConfig["classRoomNum"]
        self.classRoomNameList: list = list(list(self.classRoomNumConfig.items())[0][1].keys())

    def createUrlObject(self):
        uid: int = 1
        for classRoomName in self.classRoomNameList:
            classRoomNumList = self.classRoomsNumLists[classRoomName]
            for classRoomNum in classRoomNumList:
                url: str = (
                    PARSEURLENCODE[classRoomName].format(
                        self.swytUrlText.replace(OLDPHP, NEWPHP),  # 待修改
                        parse.urlencode(self.createUrlDic),
                        classRoomNum
                    )
                )
                # 拼接为完整的Url链接
                urlReferer = self.requestsUA["headers"]["Referer"][0:-1]
                url = urlReferer + url
                urlObject = {
                    "uid": uid,
                    "classRoomName": classRoomName,
                    "classRoomNum": classRoomNum,
                    "url": url
                }
                self.urlPoolResult.append(urlObject)
                # uid自增1
                uid = uid + 1

# https://webvpn.ppsuc.edu.cn/http/77726476706e69737468656265737421a1a510d276693c1e2c59dae2c90476/swyt/jxcdkbcx.php?xnxq=%222021-20221%22&jxcdmc=%27%CD%C5%D6%FD%BD%A3%C2%A5101%27
# https://webvpn.ppsuc.edu.cn/http/77726476706e69737468656265737421a1a510d276693c1e2c59dae2c90476/swyt/jxcdkbcx.php?xnxq= %222021-20221%22 &jxcdmc= %27%CD%C5%D3%FD%BE%AF%CE%F7%C2%A5509%27
