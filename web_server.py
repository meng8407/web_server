"""
web server 程序
完成一个类，提供给使用者，让使用者可以快速搭建web服务，展示
自己的网页
用tcp协议传输，io多路进程，正则表达式查找
先搭建主函数，搭建传输准备类，搭建接受，收发，网址
"""
from socket import *
from select import select
import re
#搭建并发io模型，实现http协议
class WebSever:
    def __init__(self,host='0.0.0.0',port=80,
                   html=None):
        self.host=host
        self.port=port
        self.html=html
        self.rlist=[]
        self.wlist=[]
        self.slist=[]
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sock=socket()
        self.sock.setblocking(False)

    def bind(self):
        self.adreess=(self.host,self.port)
        self.sock.bind(self.adreess)
        #启动服务开始监听套接字
    def start(self,connfd):
        self.sock.listen(5)
        while True:
            rs,ws,xs=select(self.rlist,self.wlist,self.slist)
            #链接客户端
            for i in self.sock:
                connfd,addr=i.accept()
                print("连接到：",addr)
                connfd.setblocking(False)
                self.rlist.append(connfd)

            else:
                #收到客户端请求
                self.handel(i)

    def handel(self,connfd):
        #接受浏览器请求
        request=connfd.recv(1024*10).decode()
        #解析请求
        patten="[a-z]+\s+(?P<info>/\S*)"
        result=re.match(patten,request)
        if result:
            info=result.group("info")
            print("请求内容：",info)
            self.send_html(connfd,info)
        else:
            #没有匹配到内容断开连接
            connfd.close
            self.rlist.remove(connfd)
    def send_html(self,connfd,info):
        if info=="/":
            filename=self.html+"/index.html"
        else:
            filename=self.html+info
        try:
            #请求里面有图片
            f=open(filename,"rb")
        except:
            #文件不存在
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry...<\h1>"
            response = response.encode()
        else:
            data = f.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n" % len(data)
            response += "\r\n"
            response = response.encode() + data
        finally:
            # 发送响应给客户端
            connfd.send(response)

if __name__ == '__main__':

    #实例化一个对象，需要客户传入信息 http地址
    httpd=WebSever(host='0.0.0.0',port=8888,
                   html="./static")#文件地址)
    httpd.start()