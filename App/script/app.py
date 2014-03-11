#!/usr/bin/env python

import threading
from App.script import ServerRequestHandler


serverRequestHandler = ServerRequestHandler.ServerRequestHandler()


def application(environ, start_response):
    print 'Main thread id is : ' + str(threading.current_thread().ident)
    return serverRequestHandler.handleRequest(environ, start_response)

#from wsgiref.simple_server import make_server
#httpd = make_server(
#    '',  # The host name.
#    8051,       # A port number where to wait for the request.
#    application  # Our application object name, in this case a function.
#)
#httpd.serve_forever()
