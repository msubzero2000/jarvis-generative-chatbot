import json


class JsonFile(object):

    @staticmethod
    def jsonFromFile(filePath):
        file = open(filePath, "r")
        return json.loads(file.read())

    @staticmethod
    def jsonToFile(filePath, jsonObj):
        file = open(filePath, "w")
        file.write(json.dumps(jsonObj, sort_keys=True, indent=4, separators=(',', ': ')))
        file.close()
