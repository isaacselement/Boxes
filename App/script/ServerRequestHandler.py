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

        status = '200 OK'
        response_body = ''

        if request_method.lower() == 'get':
            if request_path == '/service/developer':
                response_body = fileHandler.getIndexTemplate()

        if request_method.lower() == 'post':
            if request_path == '/service/uploadDeveloper':
                # threadPool.add_task(self.handleData, environ)

                status = self.handleData(environ)
                response_body = fileHandler.getIndexTemplate()
                #response_body = response_body % reponse_data

            if request_path == '/service/upload':
                # threadPool.add_task(self.handleData, environ)
                response_body = '{\"result\": 1}'
                statuscode = self.handleData(environ)
                #if statuscode.startswith('200'):
                    #response_body = '{\"result\": 1}'

        response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
        start_response(status, response_headers)
        return [response_body]


    def handleData(self, environ):
        print '#### --> handleData thread id is : ' + str(threading.current_thread().ident)
        formDatasList = formHandler.getFormDataAsList(environ)
        fileData, parameters = formHandler.parseFormDataList(formDatasList)
        file_name = formHandler.getFileName(formDatasList[1])
        print '#### --> has  parsed form data successfully'


        fileHandler.saveFileFromFormData(fileData, file_name, file_absolute_path)
        print '######## a file upload absolute path : ' + file_absolute_path + '  file name : ' + file_name

        return '200 OK'
