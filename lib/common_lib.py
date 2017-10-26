class CommonResponse(object):
    def __init__(self, data=None, name=None):
        self.data = data
        self.name = name

    def success(self, data, name):
        return {'code': '1', 'msg': '%s data is success' % name, 'result': data}

    def error(self, data, name):
        return {'code': '0', 'msg': '%s data is error' % name, 'result': data}