import socket
import _thread
import json

'''
https://gitee.com/huoyo/microhttp
'''


class HttpCode(object):
    OK = (200, 'OK')
    Bad_Request = (400, 'Bad Request')
    Unauthorized = (401, 'Unauthorized')
    Forbidden = (403, 'Forbidden')
    Not_Found = (404, 'Not Found')
    Method_Not_Allowed = (405, 'Method Not Allowed')
    Request_Timeout = (408, 'Request Timeout')
    Internal_Server_Error = (500, 'Internal Server Error')


class Request(object):
    '''
    an object to receive a http request
    '''

    def __init__(self):
        self.method = "GET"
        self.uri = ""
        self.headers = dict()
        self.route_param = dict()
        self.body_param = dict()
        self.version = ''

    def __str__(self):
        return 'Request=>[method:{},uri:{},version:{},route_param:{},body_param:{}]'.format(self.method, self.uri,
                                                                                            self.version,
                                                                                            str(self.route_param),
                                                                                            str(self.body_param))


class Response(object):
    '''
    an object to send a http response
    '''

    def __init__(self, http_code=HttpCode.OK[0], content_type='application/json', connection='close',
                 message=HttpCode.OK[1], version=''):
        self.http_code = http_code
        self.content_type = content_type
        self.connection = connection
        self.version = version
        self.message = message
        self.body = ''


class WebServer(object):
    '''
    a simple web server
    Note:
        1.no session for this server
        2.no keep-alive for this server
        3.supported methods: [GET,POST,PUT,DELETE]
        4.can not upload files for this server
    '''

    def __init__(self, context_path='', max_connections=100, read_size=4096):
        self.route_map = dict()
        self.read_size = read_size
        self.max_connections = max_connections
        self.context_path = context_path

    def route(self, url, method='GET'):
        def decorate(fun):
            self.route_map[self.context_path + url] = (method, fun)
            return fun

        return decorate

    def get(self, url):
        return self.route(url, 'GET')

    def post(self, url):
        return self.route(url, 'POST')

    def delete(self, url):
        return self.route(url, 'DELETE')

    def put(self, url):
        return self.route(url, 'PUT')

    def run(self, host='0.0.0.0', port=80, blocked=True):
        '''
        start a simple server to receive requests
        :param host: unnecessary to explain
        :param port:unnecessary to explain
        :param blocked: unnecessary to explain
        :return:
        '''
        if not blocked:
            _thread.start_new_thread(self.__run, (host, port))
        else:
            self.__run(host, port)

    def __run(self, host='0.0.0.0', port=80):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('web started on http://{}:{}'.format(host, port))
        s.bind((host, port))
        s.listen(self.max_connections)
        while True:
            conn, addr = s.accept()
            try:
                self.handle_client(conn, addr)
            except Exception as e:
                print(e)
                if conn is not None:
                    conn.close()

    def handle_client(self, conn, addr):
        rec_data = conn.recv(self.read_size)
        rec_str = str(rec_data, 'utf-8')
        request = self.parse_received(rec_str)
        if request.uri not in self.route_map.keys():
            self.response(conn, Response(http_code=HttpCode.Not_Found[0], message=HttpCode.Not_Found[1],
                                         version=request.version))
            return
        method, function = self.route_map[request.uri]
        if method != request.method:
            self.response(conn,
                          Response(http_code=HttpCode.Method_Not_Allowed[0], message=HttpCode.Method_Not_Allowed[1],
                                   version=request.version))
            return
        response = Response(http_code=HttpCode.OK[0], message=HttpCode.OK[1], version=request.version)
        response_body = function(request, response)
        if response_body is not None:
            response.body = response_body
        self.response(conn, response)

    def parse_received(self, text: str):
        text_split = text.split("\r\n")
        header_end = 0
        method = None
        route_param_str = ''
        http_version = ''
        body_param = ''
        headers = dict()
        for i, line in enumerate(text_split):
            if i == 0:
                line_split = line.split(" ")
                if len(line_split) < 3:
                    continue
                method, route_param_str, http_version = line_split[0], line_split[1], line_split[2]

            if line == '' and header_end == 0:
                header_end = i
            if i > header_end and header_end != 0:
                body_param += line

            if i > 0 and header_end == 0:
                s_index = line.index(":")
                k = line[0:s_index]
                v = line[s_index + 1:]
                headers[k.lower()] = v.strip()

        uri, uri_param = self.parse_route_param(route_param_str)
        request = Request()
        request.method = method
        request.uri = uri
        request.version = http_version
        request.route_param = uri_param
        request.headers = headers
        body_param = body_param.strip()
        if 'content-type' in request.headers.keys():
            if 'application/json' in request.headers['content-type']:
                if len(body_param) > 0 and body_param.startswith("{") and body_param.endswith("}"):
                    request.body_param = json.loads(body_param)
            elif 'application/x-www-form-urlencoded' in request.headers['content-type']:
                fparams = body_param.split('&')
                request.body_param = {param.split('=')[0]: param.split('=')[1] for param in fparams}

        return request

    def parse_route_param(self, route_param_str: str):
        if "?" not in route_param_str:
            return route_param_str, dict()
        route, param_str = route_param_str.split("?")
        params = param_str.split('&')
        param_dict = {param.split('=')[0]: param.split('=')[1] for param in params}
        return route, param_dict

    def response(self, conn: socket, response: Response):
        try:
            conn.send(
                bytes('{} {} {}\r\n'.format(response.version, response.http_code, response.message),'utf-8'))
            conn.send(bytes('Content-Type: {}\r\n'.format(response.content_type),'utf-8'))
            conn.send(bytes('Connection: {}\r\n\r\n'.format(response.connection),'utf-8'))
            if 'application/json' in response.content_type:
                conn.sendall(bytes(response.body,'utf-8'))
            elif 'text/html' in response.content_type:
                conn.sendall(bytes(response.body,'utf-8'))
            else:
                conn.sendall(bytes(response.body,'utf-8'))
            conn.close()
        except Exception as e:
            print(e)
