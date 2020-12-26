from transitions.extensions import GraphMachine
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
from utils import send_text_message, send_message
import requests
canmessage = TemplateSendMessage(
                                alt_text ='Buttons template',
                                template = ButtonsTemplate(
                                    thumbnail_image_url='https://ppt.cc/f6aUmx@.png',
                                    title = '請問需要什麼服務?',
                                    text = '如需更多功能請按其他鍵或輸入"其他"',
                                    actions=[
                                        MessageTemplateAction(
                                            label = '火車訂票',
                                            text = '火車訂票'
                                        ),
                                        MessageTemplateAction(
                                            label = '高鐵訂票',
                                            text = '高鐵訂票'
                                        ),
                                        MessageTemplateAction(
                                            label = '今日運勢',
                                            text = '今日運勢'
                                        ),
                                        MessageTemplateAction(
                                            label = '其他',
                                            text = '其他'
                                        )
                                        
                                    ]
                                )
                            )
canmessage1 = TemplateSendMessage(
                                alt_text ='Buttons template',
                                template = ButtonsTemplate(
                                    thumbnail_image_url='https://ppt.cc/f6aUmx@.png',
                                    title = '請問需要什麼服務?',
                                    text = '如需返回請按返回鍵或輸入"返回"',
                                    actions=[
                                        MessageTemplateAction(
                                            label = '還沒做',
                                            text = '還沒做'
                                        ),
                                        MessageTemplateAction(
                                            label = '還沒做',
                                            text = '還沒做'
                                        ),
                                        MessageTemplateAction(
                                            label = '還沒做',
                                            text = '還沒做'
                                        ),
                                        MessageTemplateAction(
                                            label = '返回',
                                            text = '返回'
                                        )
                                        
                                    ]
                                )
                            )
keyword = ["牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座", "水瓶座", "雙魚座", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
keyword1 = ["還沒做", "返回"]
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "火車訂票"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        reply_arr = []
        reply_arr.append(TextSendMessage("https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"))
        reply_arr.append(canmessage)
        send_message(reply_token, reply_arr)
        self.go_back()

    # def on_exit_state1(self):
    #     print("Leaving state1")

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "高鐵訂票"

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        reply_arr = []
        reply_arr.append(TextSendMessage("https://www.thsrc.com.tw/"))
        reply_arr.append(canmessage)
        send_message(reply_token, reply_arr)
        self.go_back()

    # def on_exit_state2(self):
    #     print("Leaving state2")

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "今日運勢"

    def on_enter_state3(self, event):
        print("I'm entering state3")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入你的星座:\n牡羊座 請輸入0\n金牛座 請輸入1\n雙子座 請輸入2\n巨蟹座 請輸入3\n獅子座 請輸入4\n處女座 請輸入5\n天秤座 請輸入6\n天蠍座 請輸入7\n射手座 請輸入8\n摩羯座 請輸入9\n水瓶座 請輸入10\n雙魚座 請輸入11\n輸入12返回上一頁")


    # def on_exit_state3(self):
    #     print("Leaving state3")

    def is_going_to_state4(self, event):
        print("INFUNCTION")
        text = event.message.text
        
        return text.lower() in keyword

    def on_enter_state4(self, event):
        print(event.message.text)
        i=0
        if(len(event.message.text)==3):
            i=0
            for key in keyword:
                if(key == event.message.text):
                    break
                i=i+1
        else :
            i=int(event.message.text)
        

        reply_token = event.reply_token
        if (i==12):
            send_message(reply_token, canmessage)
            self.go_back()
            return
        reply_arr = []

        str_arr = keyword[i]+"\n\n"

        res = requests.get("https://astro.click108.com.tw/daily_"+str(i)+".php?iAstro="+str(i))
        
        pos = res.text[res.text.find('love.png'):res.text.find('love.png')+200]
        pos = pos[pos.find('LIGHT">'):pos.find('LIGHT">')+100]
        # reply_arr.append(TextSendMessage("愛情運勢: "+pos[pos.find('icon')+5:pos.find('.png')]+"/5"))
        # ☆★
        star =""
        for i in range (0, int(pos[pos.find('icon')+5:pos.find('.png')])):
            star =star+"★"
        for i in range (0, 5-int(pos[pos.find('icon')+5:pos.find('.png')])):
            star =star+"☆"
        str_arr = str_arr + "愛情運勢: "+star+"\n\n"

        pos = res.text[res.text.find('work.png'):res.text.find('work.png')+200]
        pos = pos[pos.find('LIGHT">'):pos.find('LIGHT">')+100]
        # reply_arr.append(TextSendMessage("工作運勢: "+pos[pos.find('icon')+5:pos.find('.png')]+"/5"))
        star =""
        for i in range (0, int(pos[pos.find('icon')+5:pos.find('.png')])):
            star =star+"★"
        for i in range (0, 5-int(pos[pos.find('icon')+5:pos.find('.png')])):
            star =star+"☆"
        str_arr = str_arr +"工作運勢: "+star+"\n\n"

        pos = res.text[res.text.find('all.png'):res.text.find('all.png')+200]
        pos = pos[pos.find('LIGHT">'):pos.find('LIGHT">')+100]
        # reply_arr.append(TextSendMessage("總運勢: "+pos[pos.find('icon')+5:pos.find('.png')]+"/5"))
        star =""
        for i in range (0, int(pos[pos.find('icon')+5:pos.find('.png')])):
            star =star+"★"
        for i in range (0, 5-int(pos[pos.find('icon')+5:pos.find('.png')])):
            star =star+"☆"
        str_arr = str_arr + "整體運勢: "+star+"\n\n"

        str_arr = str_arr + "幸運數字: "+res.text[res.text.find('"NUMERAL">')+10:res.text.find('"NUMERAL">')+11]+"\n\n"
        # reply_arr.append(TextSendMessage("幸運數字: "+res.text[res.text.find('"NUMERAL">')+10:res.text.find('"NUMERAL">')+11]))
        pos = res.text[res.text.find('title02.png')+52:res.text.find('title02.png')+90]
        # reply_arr.append(TextSendMessage("幸運顏色: "+pos[pos.find("<h4>")+4:pos.find("<h4>")+7]))
        str_arr = str_arr + "幸運顏色: "+pos[pos.find("<h4>")+4:pos.find("<h4>")+7] 

        reply_arr.append(TextSendMessage(str_arr))
        reply_arr.append(canmessage)
        send_message(reply_token, reply_arr)
        self.go_back()

    def is_going_to_state5(self, event):
        text = event.message.text
        return text.lower() == "其他"

    def on_enter_state5(self, event):
        print("I'm entering state5")

        reply_token = event.reply_token
        # reply_arr = []
        # reply_arr.append(TextSendMessage("https://www.thsrc.com.tw/"))
        # reply_arr.append(canmessage)
        send_message(reply_token, canmessage1)
        # self.go_back()

    def is_going_to_state6(self, event):
        text = event.message.text
        return text.lower() in keyword1

    def on_enter_state6(self, event):
        print("I'm entering state6")
        reply_token = event.reply_token

        if(event.message.text == "返回"):
            print("BACKKK")
            send_message(reply_token, canmessage)
            self.go_back()
            return

        reply_arr = []
        reply_arr.append(TextSendMessage("此功能開發中，敬請期待"))
        reply_arr.append(canmessage1)
        send_message(reply_token, reply_arr)
        # self.go_back()