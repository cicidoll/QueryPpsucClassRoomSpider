from sanic import Sanic
from sanic.response import json
from utils import loadJson
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


@app.get("/detail/<Input>")
async def getDetailedMessage(request,Input):
    try:
        buildingName, Time, date = str(Input).split("_")[0], str(Input).split("_")[1], str(Input).split("_")[2]
        return json(ClassRoomData[urlMap0[buildingName]][Time][date])
    except Exception as e:
        return json({e})
