import json


def loadJson(fileNamePath):
    """ 注意，这里传入的fileNamePath相对路径，以本方法所在文件为基准 """
    try:
        with open(fileNamePath, 'r', encoding='utf8') as (jsonFile):
            json_data = json.load(jsonFile)
            return json_data
    except Exception as e:
        pass


def encodeGBK(verse: str):
    """
    Output Eg: %27%CD%C5%BD%D7%D2%BB%27
    """
    byte = verse.encode('GBK')
    res = str(byte)[2:-1].replace("\\x", "%").upper()
    return res


if __name__ == '__main__':
    encodeGBK("团阶一")  # output: %CD%C5%BD%D7%D2%BB
    encodeGBK("'团报告厅'")
