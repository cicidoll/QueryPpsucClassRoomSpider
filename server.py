from sanic import Sanic, request
from sanic.response import json, text
from utils import loadJson
import refreshClassroomData
app = Sanic("MyHelloWorldApp")
ClassRoomData = loadJson("data/classRoomData.json")
BuildingConfig = loadJson("config/classRoomNumConfig.json")["classRoomNum"]
BuildingRoom = ["zhuJian", "zhongLou", "XiPei"]

urlMap0 = {"zj": "zhuJian", "zl": "zhongLou", "xp": "XiPei", "tj": "TuanJie"}
urlMap1 = {"zhuJian": "zj", "zhongLou": "zl", "XiPei": "xp", "TuanJie": "tj"}
#  url缩写和楼名称映射一下


@app.get("/")
async def getAllMessage(request):
    return json(ClassRoomData)


@app.get("/updateData")
async def getAllMessage(request):
    try:
        refreshClassroomData.Work()
        return text("NO ERROR OCCURRED")
    except Exception as e:
        return json(e)


@app.get("/detail/Class")
async def getDetailedMessage(request: request.Request):
    args = request.args
    print(args)
    try:
        buildingName, Time, date = args['building'][0], args['time'][0], args['date'][0]
        return json(ClassRoomData[urlMap0[buildingName]][Time][date])
    except Exception as e:
        return json({e})


@app.get("/detail/mobilize")
async def getDetailedMessageForMobilize(request: request.Request):
    args = request.args
    print(args)
    try:
        buildingName, room = args['building'][0], args['room'][0]
        return json(loadJson("data/mobilizeBorrow.json")["mobilize"][urlMap0[buildingName]][room])
    except Exception as e:
        return json({e})


@app.get("/detail/borrow")
async def getDetailedMessageForBorrow(request: request.Request):
    args = request.args
    print(args)
    try:
        buildingName, room = args['building'][0], args['room'][0]
        return json(loadJson("data/mobilizeBorrow.json")["borrow"][urlMap0[buildingName]][room])
    except Exception as e:
        return json({e})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)