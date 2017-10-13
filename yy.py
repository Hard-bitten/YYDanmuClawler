#-*- encoding:utf-8 -*-
 
import sys
from socket import *
import json, time, threading,xml
from websocket import create_connection
import re

class Client():
    roomid = 0
    loginInfo = {
        "uri": 0, 
        "type": 0, 
        "svc_link": "66b2c67d-f7ab-4355-a6f0-b52ffccc857e"
        }
    sureinfo = {
        "uri": 1,
        "top_sid": 0,
        "sub_sid": 0,
        "svc_link": "66b2c67d-f7ab-4355-a6f0-b52ffccc857e"
    }
    cookie = ''
    def __init__(self,roomid):
        self.roomid = roomid
        self.sureinfo["top_sid"] = self.roomid
        self.sureinfo["sub_sid"] = self.roomid
        ts=time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time()))
        self.chatfile = open('./result/chatmsg_%s_%s.txt'%(self.roomid,ts),"w+")
        self.giftfile = open('./result/gift_%s_%s.txt'%(self.roomid,ts),"w+")
        
        self.ws = create_connection("ws://tvgw.yy.com:26101/websocket")
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()
        self.beats = threading.Thread(target=self.beat)
        self.beats.start()


    def send(self,data):
        try:
            if self.ws.connected:
                self.ws.send(json.dumps(data))
        except error as e:
            print(e)
        
    def beat(self):
        while 1:
            time.sleep(5)
            data = {"uri": "6", "ts": int(time.time()), "svc_link": ""};
            self.send(data)
            # print(data)
            
    def recv(self):
        while self.ws.connected:
            try:
                result = json.loads(self.ws.recv())
                # print ("received msg:"+str(result))
                if result['response'] == 'login':
                    print('login')
                    self.send(self.loginInfo)
                    time.sleep(1)
                elif result['response'] == 'init':
                    print('init')
                    self.sureinfo['svc_link'] = self.cookie
                    self.send(self.sureinfo)
                    time.sleep(1)
                elif result['response'] == 'join':
                    print('join')
                    pass
                elif result['response'] == 'gift_broadcast':
                    gifts = result['gifts']
                    for gift in gifts:
                        s = (gift['from_uid']+'\t'+gift['from_name']+'\t'+gift['gift_type']+'\t'+gift['gift_num']+'\n')
                        self.giftfile.write(s)
                        self.giftfile.flush()
                elif result['response'] == 'chat':
                    msg = result['chat_msg']
                    pat = re.compile('<txt.+?data=\"(.+?)\".*(.+)/>')
                    mess = pat.split(msg)
                    nick = result['nick']
                    yyid = result['yyid']

                    if mess:
                        s = yyid+'\t'+nick+'\t'+mess[1]+'\n'
                        print(s,end='')
                        self.chatfile.write(s)
                        self.chatfile.flush()
                else:
                    pass

            except Exception as e:
                print(e)
  
 
 
if __name__ == '__main__':
    c = Client(89703802)
