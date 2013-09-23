import threading

import os
import ThreadPool
import FormHandler
import FileHandler

formHandler = FormHandler.FormHandler()
fileHandler = FileHandler.FileHandler()

threadPool = ThreadPool.ThreadPool(5)

absolutePath = os.path.expanduser("~")
file_absolute_path = absolutePath + "/Workspace/resources/boxes/"

class ServerRequestHandler:
    def handleRequest(self, environ, start_response):

        request_path = environ['PATH_INFO']
        request_method = environ['REQUEST_METHOD']
        #print '#### Path: ' + request_path + ' | Method: ' + request_method

        response_body = '{\"status\": 0}'

        if request_method.lower() == 'get':
            if request_path == '/service/developer':
                response_body = fileHandler.getIndexTemplate()

        if request_method.lower() == 'post':
            if request_path == '/service/uploadDeveloper':
                # threadPool.add_task(self.handleData, environ)
                self.handleData(environ)

            if request_path == '/service/upload':
                # threadPool.add_task(self.handleData, environ)
                self.handleData(environ)
                response_body = '{\"status\": \"1\",\"action\":\"/service/upload\"}'

        response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
        start_response('200 OK', response_headers)

        return [response_body]


    def handleData(self, environ):
        print '#### --> handleData thread id is : ' + str(threading.current_thread().ident)
        formDatasList = formHandler.getFormDataAsList(environ)
        fileData, parameters = formHandler.parseFormDataList(formDatasList)
        file_name = formHandler.getFileName(formDatasList[1])
        print '#### --> has  parsed form data successfully'


        fileHandler.saveFileFromFormData(fileData, file_name, file_absolute_path)
        print '######## a file upload absolute path : ' + file_absolute_path + '  file name : ' + file_name
