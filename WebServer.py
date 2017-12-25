from socket import *
import re
import os

SERVER_PORT = 4001
SERVER_ADDRESS = 'localhost'

def start_server():
    serverSocket = socket(AF_INET, SOCK_STREAM) # create instance of Socket Object
    serverSocket.bind((SERVER_ADDRESS, SERVER_PORT))# bind address and port
    serverSocket.listen(1)
    print("Server started at port {}".format(SERVER_PORT))
    return serverSocket

def listen_requests(serverSocket):

    while 1:
        connectionSocket, addr = serverSocket.accept() # get client
        sentence = connectionSocket.recv(1024).decode() # receive http message
        file_path = parse_sentence(sentence) # parse message
        responsed = response(file_path, connectionSocket) # generate response


        connectionSocket.close()

def response(file_path, connectionSocket):
    has_file = True
    if file_path == './': # set default filepath to index.html
        file_path = './index.html'

    with open('./headers', 'rb') as f: #get header
        header = f.read()
    print(file_path)
    if not os.path.isfile(file_path): #check whether the file exists
        header = define_header(header, b'.txt')
        return_content = header + b'\n File not found!'
    else:
        with open(file_path, 'rb') as f: #if exists, read it
            content = f.read()
        header = define_header(header, detect_content_type(file_path)) #modify header
        return_content = header + content #generate return conten

    connectionSocket.send(return_content) #send


def detect_content_type(file_path): #use regular expression to detect file type
    txt_pattern = re.compile('.txt')
    html_pattern = re.compile('.html')
    css_pattern = re.compile('.css')
    js_pattern = re.compile('.js')
    video_pattern = re.compile(".mp4")
    pic_pattern = r'.jpg'
    if re.search(txt_pattern, file_path) != None:
        return b'text/plain'
    elif re.search(html_pattern, file_path) or re.search(css_pattern, file_path) or re.search(js_pattern, file_path) :
        return b'text/html'
    elif re.search(js_pattern, file_path):
        return b'VIDEO'
    elif re.search(pic_pattern, file_path):
        return b'image/webb'
    else:
        return b'application/source'

def define_header(header, content_type):
    if content_type == b'VIDEO':
        with open('./video_header', 'rb') as f:
            header = f.read()
    else:
        header = header.replace(b"CONTENT_TYPE", content_type)
    return header


def parse_sentence(sentence):
    if sentence == "":
        return
    file_path_pattern = re.compile('GET (/.*?) HTTP/1.1') # get file path
    file_path = '.' + re.findall(file_path_pattern, sentence)[0]

    return file_path



if __name__ == "__main__":

    serverSocket = start_server() # start server
    listen_requests(serverSocket) # listen to requests


