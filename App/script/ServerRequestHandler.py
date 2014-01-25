import threading

import os
import json
import re
import ThreadPool
import FormHandler
import FileHandler
import urllib

formHandler = FormHandler.FormHandler()
fileHandler = FileHandler.FileHandler()

threadPool = ThreadPool.ThreadPool(5)

absolutePath = os.path.expanduser("~")
file_absolute_path = absolutePath + "/Workspaces/Resources/Boxes/"





class m_get_handler:
    def __init__(self):
        self.func_table = {}

    def register_method(self,funcDict):
        self.func_table.update(funcDict)

    def handle_download(self,environ):
        response_body = ''
        query_string = environ['QUERY_STRING']
        files_directory = file_absolute_path + query_string
        try:
            dirlist = os.listdir(files_directory)
        except os.error:
             response_body = "No permission to list directory"

        response_body = json.dumps(list)
        return response_body,None


    def handle(self,path,environ):
        print 'get====='





class m_post_handler:

    def handle_upload(self,environ):
        path = fileHandler.handleData(formHandler,file_absolute_path,environ)
        return '{\"status\": \"1\",\"action\":\"'+ path + '\"}',None

    def handle_download(self,environ):
        response_length=''
        response_body = ''
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
                print list
            except os.error:
                response_body = '{\"status\": \"0\",\"action\":\"/service/download\",\"description\":' + 'No permission to list directory' + '}'

            filesList = json.dumps(list)
            response_body = '{\"status\": \"1\",\"action\":\"/service/download\",\"results\":' + filesList + '}'
        else:
            fileNamePath = file_absolute_path + path
            print fileNamePath
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
                    file_list = os.listdir(folder_thumb_path)                        #print file_list
                    for single_file in file_list:
                        #print single_file
                        if single_file[-4:] == '.jpg':
                            #found a thumbnail already
                            the_thumb = folder_thumb_path+'/'+single_file
                            #make the link
                            command = 'ln -s '+self.qoute_space(the_thumb)+ ' ' +self.qoute_space(fileNamePath)
                            print command
                            os.system(command)
                            break
                else:
                    print "may be we encounter a chinese char url"
                    #try to resolve a url with chinese character inside
                    #Iterate through the path, try to decode everything
                    path_apart = path.split('/')
                    new_apart = []
                    for part in path_apart:
                        try:
                            part = urllib.unquote(part)
                        finally:
                            new_apart.append(part)
                    fix_url = '/'.join(new_apart)
                    fix_path = file_absolute_path+fix_url
                    response_length = str(os.path.getsize(fix_path))
                    filelike = file(fix_path, 'r')
                    response_body = environ['wsgi.file_wrapper'](filelike)



        return response_body,response_length

    def qoute_space(self,s):
        return s.replace(' ',r'\ ')

    def handle_move(self,environ):
        formDatas = formHandler.getFormDatas(environ)
        formDatasList = formDatas.split('&')
        print formDatas
        for element in formDatasList:
            values = element.split('=')
            os.system('ln -s ' + file_absolute_path+self.qoute_space(values[0]) + ' ' + file_absolute_path+self.qoute_space(values[1]))
            print "EXE: ln "+ file_absolute_path+values[0] + ' ' + file_absolute_path+values[1]
        lastObject = formDatasList[-1]
        lastValues = lastObject.split('=')
        return '{\"status\": \"1\",\"action\":\"/service/move\"}',None

    def fetch_config(self,environ):
        response_body = ''
        response_length = ''
        formDatas = formHandler.getFormDatas(environ)
        formDatasList = formDatas.split('&')
        listLen = len(formDatasList)
        path = ''
        for index in range(0,listLen):
            element = formDatasList[index]
            values = element.split('=')
            if values[0] == 'PATH':
                path = values[1]
                break
        head,tail = os.path.split(path)
        isFile = bool(tail.strip())
        if isFile:
            filepath = file_absolute_path + head+ '/config/' + tail
            print filepath
            if os.path.isfile(filepath):
                print filepath + ' is a file'
                file_size = os.path.getsize(filepath)
            else:
                print 'use default file'
                filepath = file_absolute_path + head + '/config/' + 'config.txt'

            file_size = os.path.getsize(filepath)
            response_length = str(os.path.getsize(filepath))
            filedata = file(filepath,'r')
            response_body = environ['wsgi.file_wrapper'](filedata)

        return response_body,response_length

    def get_track_file(self, environ):
        response_body = ''
        response_length = ''
        formDatas = formHandler.getFormDatas(environ)
        formDatasList = formDatas.split('&')
        listLen = len(formDatasList)
        path = ''

        for index in range(0,listLen):
            element = formDatasList[index]
            values = element.split('=')
            if values[0] == 'PATH':
                path = values[1]
                break

        head,tail = os.path.split(path)
        isFile = bool(tail.strip())

        if isFile:
            filePath = file_absolute_path + head + '/'+tail
            print filePath
            if os.path.isfile(filePath):
                file_size = os.path.getsize(filePath)
                response_length = str(file_size)
                filedata = file(filePath,'r')
                response_body = environ['wsgi.file_wrapper'](filedata)
            else:
                print "file not exists"
        return response_body,response_length


    def __init__(self):
        self.func_table = {"/service/upload":self.handle_upload,
                           "/service/download":self.handle_download,
                           "/service/move":self.handle_move,
                           "/service/fetchconfig":self.fetch_config,
                           "/service/getTrackFile":self.get_track_file}

    def register_method(self,funcDict):
        self.func_table.update(funcDict)

    def handle(self,path,environ):
        return (self.func_table[path])(environ)





class ServerRequestHandler:
    #create object at the first place, call when needed is better then this.
    #needs improve
    def get_handler_by_type(self, type):
        if type == 'get':
            return m_get_handler()
        elif type == 'post':
            return m_post_handler()

    def handleRequest(self, environ, start_response):

        request_path = environ['PATH_INFO']
        request_type = environ['REQUEST_METHOD']
        request_type = request_type.lower()
        #print '#### Path: ' + request_path + ' | Method: ' + request_method

        response_body = '{\"status\": 0}'
        response_length = ''


        handle_method = self.get_handler_by_type(request_type)
        response_body,response_length = handle_method.handle(request_path,environ)

        if not response_length:
            response_length = str(len(response_body))
        response_headers = [('Content-Type', 'text/html'), ('Content-Length',response_length)]
        start_response('200 OK', response_headers)

        return response_body

