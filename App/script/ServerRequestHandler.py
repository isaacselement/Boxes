import threading

import os
import json
import re
import ThreadPool
import FormHandler
import FileHandler

formHandler = FormHandler.FormHandler()
fileHandler = FileHandler.FileHandler()

threadPool = ThreadPool.ThreadPool(5)

absolutePath = os.path.expanduser("~")
file_absolute_path = absolutePath + "/Workspaces/resources/boxes/"

class ServerRequestHandler:
    def handleRequest(self, environ, start_response):

        request_path = environ['PATH_INFO']
        request_method = environ['REQUEST_METHOD']
        #print '#### Path: ' + request_path + ' | Method: ' + request_method

        response_body = '{\"status\": 0}'
        response_length = ''



        if request_method.lower() == 'get':
            if request_path == '/service/download':
                query_string = environ['QUERY_STRING']
                files_directory = file_absolute_path + query_string
                try:
                    list = os.listdir(files_directory)
                except os.error:
                    response_body = "No permission to list directory"

                response_body = json.dumps(list)





        if request_method.lower() == 'post':

            if request_path == '/service/upload':
                # threadPool.add_task(self.handleData, environ)
                self.handleData(environ)
                response_body = '{\"status\": \"1\",\"action\":\"/service/upload\"}'

            elif request_path == '/service/move':
                formDatas = formHandler.getFormDatas(environ)
                formDatasList = formDatas.split('&')
                for element in formDatasList:
                    values = element.split('=')
                    os.system('ln -s ' + file_absolute_path+values[0] + ' ' + file_absolute_path+values[1])
                    #print "EXE: ln "+ file_absolute_path+values[0] + ' ' + file_absolute_path+values[1]
                lastObject = formDatasList[-1]
                lastValues = lastObject.split('=')

            elif request_path == '/service/download':
                formDatas = formHandler.getFormDatas(environ)
                formDatasList = formDatas.split('&')
                listLen = len(formDatasList)
                path = ''
                for index in range(0, listLen):
                    element = formDatasList[index]
                    values = element.split('=')
                    if values[0] == "PATH":
                        path = values[1]
                        break
                head, tail = os.path.split(path)
                isFile = bool(tail.strip())
                if not isFile:
                    files_directory = file_absolute_path + path
                    try:
                        list = os.listdir(files_directory)
                    except os.error:
                        response_body = '{\"status\": \"0\",\"action\":\"/service/download\",\"description\":' + 'No permission to list directory' + '}'

                    filesList = json.dumps(list)
                    response_body = '{\"status\": \"1\",\"action\":\"/service/download\",\"objects\":' + filesList + '}'
                else:
                    fileNamePath = file_absolute_path + path
                    try:
                        file_size = os.path.getsize(fileNamePath)
                        response_length = str(os.path.getsize(fileNamePath))
                        filelike = file(fileNamePath, 'r')
                        response_body = environ['wsgi.file_wrapper'](filelike)
                    except os.error:
                        #file do not exists
                        #try to access a folder by path name
                        foldername = ''
                        print 'there is a missing thumb :' + path
                        pattern = r'(.*)/*thumbnails/(.+)\.jpg'
                        folder_name_match = re.search(pattern,path)
                        if folder_name_match:
                            foldername = folder_name_match.group(2)
                            prefolder = folder_name_match.group(1)
                            #try to grab a thumbnail from this folder
                            folder_thumb_path = file_absolute_path+ prefolder+'/'+foldername+'/thumbnails'
                            file_list = os.listdir(folder_thumb_path)
                            #print file_list
                            for single_file in file_list:
                                #print single_file
                                if single_file[-4:] == '.jpg':
                                    #found a thumbnail already
                                    the_thumb = folder_thumb_path+'/'+single_file
                                    #make the link
                                    command = 'ln -s '+the_thumb+ ' ' +fileNamePath
                                    print command
                                    os.system(command)
                                    break
                        else:
                            print "not matching"


        if not response_length:
            response_length = str(len(response_body))
        response_headers = [('Content-Type', 'text/html'), ('Content-Length',response_length)]
        start_response('200 OK', response_headers)

        return response_body


    def handleData(self, environ):
        print '#### --> handleData thread id is : ' + str(threading.current_thread().ident)
        formDatasList = formHandler.getFormDataAsList(environ)
        fileData, parameters = formHandler.parseFormDataList(formDatasList)
        file_name = formHandler.getFileName(formDatasList[1])
        print '#### --> has  parsed form data successfully'


        fileHandler.saveFileFromFormData(fileData, file_name, file_absolute_path)
        print '######## a file upload absolute path : ' + file_absolute_path + '  file name : ' + file_name
