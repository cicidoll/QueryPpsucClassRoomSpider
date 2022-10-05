from sanic import Sanic, request
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


@app.get("/detail")
async def getDetailedMessage(request: request.Request):
    args = request.args
    print(args)
    try:
        buildingName, Time, date = args['building'][0], args['time'][0], args['date'][0]
        return json(ClassRoomData[urlMap0[buildingName]][Time][date])
    except Exception as e:
        return json({e})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)