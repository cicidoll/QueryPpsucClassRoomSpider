from asyncio.tasks import sleep
import asyncio
import functools
from .process_text import ProcessText


# requests会阻塞asyncio循环
class GetHtmlBus:
    """ 异步爬取网页文本总线控制器 """

    def __init__(self, headers, session):
        # 将传入的Headers和Session进行保存
        self.requestsUA = headers
        self.session = session
        # self.responseObjectList = []

    def bus(self, urlPools, week):
        """ 总线控制器 """
        # 创建并执行协程任务
        loopBus = asyncio.get_event_loop()
        # 实例化文本处理类
        self.processText = ProcessText(week)
        # 协程任务列表
        tasks = []
        for item in urlPools:
            tasks.append(loopBus.create_task(self.send(item)))
        loopBus.run_until_complete(asyncio.wait(tasks))
        loopBus.close()
        self.processText.processTextSave()

    async def send(self,
                   requestsObject={
                       "uid": "-1",
                       "classRoomName": "None",
                       "classRoomNum": "-1",
                       "url": "None"}):
        """ 发送网络请求，并返回抓取到的响应内容 """
        # 自定义响应对象：responseObject
        # responseObject = {"uid":链接Id, "classRoomName":教学楼名, "classRoomNum":教室, "content":抓取文本}
        responseObject = {
            "uid": requestsObject["uid"],
            "classRoomName": requestsObject["classRoomName"],
            "classRoomNum": requestsObject["classRoomNum"],
            "content": '',
            "url": requestsObject['url']
        }
        try:
            # 利用BaseEventLoop.run_in_executor()可以在coroutine中执行第三方的命令，例如requests.get()
            # 第三方命令的参数与关键字利用functools.partial传入
            loop = asyncio.get_event_loop()

            future = loop.run_in_executor(None,
                                          functools.partial(
                                              self.session.get,
                                              url=requestsObject["url"],
                                              headers=self.requestsUA
                                          )
                                          )
            response = await future
            # 要设置响应包的编码格式为gbk，不然会乱码！！！
            response.encoding = "gbk"
            # HTML内容
            content = response.text
            responseObject["content"] = content
            self.processText.processTextContent(responseObject)
        except Exception as e:
            print(e)
            raise e
