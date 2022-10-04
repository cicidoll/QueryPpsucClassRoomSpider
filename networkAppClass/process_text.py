from dataclasses import dataclass
from lxml import etree
from interval import Interval
import datetime  # 导入datetime模块
import re
import json
import sys

sys.path.append(".")
from utils import loadJson


class ProcessText:
    def __init__(self, week):
        self.week = week
        # 写入json的文本变量，初始化模板
        self.classRoomDataJsonText = loadJson('config/dataTemplate.json')
        self.mobilizeBorrowJsonText = loadJson('config/mobilizeBorrowTemplate.json')
        self.pathPool = loadJson('config/classRoomNumConfig.json')["pathPool"]

    def processTextSave(self):
        jsonName = "./data/classRoomData.json"
        jsondata = json.dumps(self.classRoomDataJsonText, indent=4, separators=(',', ': '))  # json格式美化写入
        writeFile = open(jsonName, 'w', encoding='utf-8')
        writeFile.write(jsondata)
        writeFile.close()

        jsonName = "./data/mobilizeBorrow.json"
        # 加入 ensure_ascii=False 选项。导出json文件不乱码
        jsondata = json.dumps(self.mobilizeBorrowJsonText, indent=4, ensure_ascii=False, separators=(',', ':'))
        writeFile = open(jsonName, 'w', encoding='utf-8')
        writeFile.write(jsondata)
        writeFile.close()

    def processTextContent(self, responseObject):
        htmlContent = etree.HTML(responseObject["content"])
        pathCount = 0
        dayCount = 1
        print("URL:{}".format(responseObject["url"]))
        print("爬取课表：")
        for path in self.pathPool:
            pathTemp = htmlContent.xpath(path)
            pathFlag = 1  # 默认置1，代表有课
            # 检测文本
            print("教室：{0}{1} pathCount={2} dayCount={3} 周{3}".format(responseObject["classRoomName"],
                                                                        responseObject["classRoomNum"], pathCount,
                                                                        dayCount), end="")
            if len(pathTemp) == 0:  # 如果该节点中长度为0，则说明没有课。
                pathFlag = 0
            else:  # 长度不为0，说明有课。结合具体的教学周，查询本教室当前教学周是否有课
                pathTemp = max(pathTemp, key=len, default='')
                pathFlag = self.RegStr(pathTemp)

            # append(0)为占位符,表示有课
            if 0 <= pathCount < 5:
                if pathFlag == 0:  # pathFlag为0，代表无课
                    self.classRoomDataJsonText[responseObject["classRoomName"]]["am12"][str(dayCount)].append(
                        int(responseObject["classRoomNum"]))
                    print("上午12节无课")
                else:
                    print("上午12节有课")
            elif 5 <= pathCount < 10:
                if pathFlag == 0:
                    self.classRoomDataJsonText[responseObject["classRoomName"]]["am34"][str(dayCount)].append(
                        int(responseObject["classRoomNum"]))
                    print("上午34节无课")
                else:
                    print("上午34节有课")
            elif 10 <= pathCount < 15:
                if pathFlag == 0:
                    self.classRoomDataJsonText[responseObject["classRoomName"]]["pm12"][str(dayCount)].append(
                        int(responseObject["classRoomNum"]))
                    print("下午12节无课")
                else:
                    print("下午12节有课")
            elif 15 <= pathCount < 20:
                if pathFlag == 0:
                    self.classRoomDataJsonText[responseObject["classRoomName"]]["pm34"][str(dayCount)].append(
                        int(responseObject["classRoomNum"]))
                    print("下午34节无课")
                else:
                    print("下午34节有课")

            pathCount += 1
            dayCount += 1
            dayCount = dayCount if dayCount <= 5 else 1
        # 调停课信息处理，当小于当前教学周时，不将其记录。
        pathMobilize = ".//div[@class='row-fluid sortable'][2] \
                        /div[@class='box span12']/div[@class='box-content'] \
                        /table/tbody/tr"
        pathBorrow = ".//div[@class='row-fluid sortable'][3] \
                        /div[@class='box span12']/div[@class='box-content'] \
                        /table/tbody/tr"
        # 该数据列表的具体长度
        mobilizeTimes = len(htmlContent.xpath(pathMobilize))
        borrowTimes = len(htmlContent.xpath(pathBorrow))

        # 开始处理调停课信息
        # 1、需要记录数据如下：
        for index in range(mobilizeTimes):
            pathContent = htmlContent.xpath(pathMobilize)[index]
            className = pathContent[4][0].xpath('string(.)')  # 课程名字
            classes = pathContent[7].xpath('string(.)')  # 调课类别
            oldDate = pathContent[8].xpath('string(.)')  # 原上课日期
            oldTimes = pathContent[11].xpath('string(.)')  # 原节次
            oldRoom = pathContent[12][0].xpath('string(.)')  # 原教室
            newDate = ''  # 置空
            newTimes = ''  # 置空
            newRoom = ''  # 置空
            if classes == "停课" and datetime.datetime.today() > datetime.datetime.strptime(str(oldDate), "%Y-%m-%d"):
                continue
            # 如果当前停课的课程日期比当前日期早，那就不记录了
            if classes != '停课':
                # 原教学周索引为9，现教学周索引为15
                oldWeek = int(pathContent[9].xpath('string(.)'))
                newWeek = int(pathContent[15].xpath('string(.)'))
                # 检测原教学周与现教学周若早于当前教学周，直接跳过该组数据。
                if (self.week >= max(oldWeek, newWeek)): continue
                newDate = pathContent[14].xpath('string(.)')  # 现上课日期
                newTimes = pathContent[17].xpath('string(.)')  # 现节次
                newRoom = pathContent[18][0].xpath('string(.)')  # 现教室
                if datetime.datetime.today() > datetime.datetime.strptime(str(newDate), "%Y-%m-%d"):
                    continue
                # 如果当前换课的课程日期比当前日期早，那就不记录了
            self.mobilizeBorrowJsonText["mobilize"][responseObject["classRoomName"]][responseObject["classRoomNum"]] \
                .append({
                'className': className, \
                'classes': classes, \
                'oldDate': oldDate, \
                'oldTimes': oldTimes, \
                'oldRoom': oldRoom, \
                'newDate': newDate, \
                'newTimes': newTimes, \
                'newRoom': newRoom}
            )
        dateMode = re.compile("\d+-\d+-\d+")
        dateMode1 = re.compile("\d{4,}\d{2,}\d{2,}")
        for index in range(borrowTimes):
            pathContent = htmlContent.xpath(pathBorrow)[index]
            if pathContent[11].xpath('string(.)') == '否': continue  # 若借用申请未通过审核，则跳过。
            borrowDate = pathContent[4].xpath('string(.)')  # 借用日期
            borrowTime = pathContent[5].xpath('string(.)')  # 借用时间
            borrowReason = pathContent[6].xpath('string(.)')  # 借用事由
            if '/' in borrowDate:
                borrowDate = str(borrowDate).replace("/", '-')
            standardDate = dateMode.findall(borrowDate)
            if len(standardDate) > 0:
                standardDate = standardDate[0]
            else:
                standardDate = str(dateMode1.findall(borrowDate)[0])
                standardDate = standardDate[0:4] + '-' + standardDate[4:6] + '-' + standardDate[6:8]
            if ((datetime.datetime.strptime(standardDate, '%Y-%m-%d') - datetime.datetime.today()).days < 0):
                continue  # 当借用日期已过期，则将其跳过。
            self.mobilizeBorrowJsonText["borrow"][responseObject["classRoomName"]][responseObject["classRoomNum"]] \
                .append({
                'borrowDate': borrowDate, \
                'borrowTime': borrowTime, \
                'borrowReason': borrowReason}
            )

    def RegStr(self, string):
        ''' 判断当前教学周 '''
        Reg1 = r'\d-\d\d'
        Reg2 = r'\d-\d'
        if re.search(Reg1, string) is None:
            it = re.search(Reg2, string)
        else:
            it = re.search(Reg1, string)
        numberList = str(it.group()).split('-')
        for i in range(len(numberList)):
            numberList[i] = int(numberList[i])

        # 若有课，返回1；无课，返回0
        return 1 if self.week in Interval(numberList[0], numberList[1]) else 0
