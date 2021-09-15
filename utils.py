import json


def loadJson(fileNamePath):
    """ 注意，这里传入的fileNamePath相对路径，以本方法所在文件为基准 """
    try:
        with open(fileNamePath,'r',encoding='utf8')as(jsonFile):
            json_data = json.load(jsonFile)
            return json_data
    except Exception as e:
        pass