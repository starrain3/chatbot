import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
from fsm import TocMachine
from utils import send_text_message

load_dotenv()

machine = TocMachine(
    states=["user", "state1", "state2", "state3", "state4", "state5", "state6", "state7", "state8"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state3",
            "conditions": "is_going_to_state3",
        },
         {
            "trigger": "advance",
            "source": "state3",
            "dest": "state4",
            "conditions": "is_going_to_state4",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state5",
            "conditions": "is_going_to_state5",
        },
        {
            "trigger": "advance",
            "source": "state5",
            "dest": "state6",
            "conditions": "is_going_to_state6",
        },
        {
            "trigger": "advance",
            "source": "state5",
            "dest": "state7",
            "conditions": "is_going_to_state7",
        },
        {
            "trigger": "advance",
            "source": "state7",
            "dest": "state8",
            "conditions": "is_going_to_state8",
        },
        {"trigger": "go_back", "source": ["state1", "state2", "state3", "state4", "state6"], "dest": "user" },
        {"trigger": "go_back5", "source": ["state6", "state7", "state8"], "dest": "state5" }
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
canmessage = TemplateSendMessage(
                                alt_text ='Buttons template',
                                template = ButtonsTemplate(
                                    thumbnail_image_url='https://ppt.cc/f6aUmx@.png',
                                    title = '請問需要什麼服務?',
                                    text = '如需更多功能請按其他鍵或輸入"其他"',
                                    actions=[
                                        MessageTemplateAction(
                                            label = '今日運勢',
                                            text = '今日運勢'
                                        ),
                                        MessageTemplateAction(
                                            label = '火車訂票',
                                            text = '火車訂票'
                                        ),
                                        MessageTemplateAction(
                                            label = '高鐵訂票',
                                            text = '高鐵訂票'
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
                                    text = '如需返回上一頁請按返回鍵或輸入"返回"',
                                    actions=[
                                        MessageTemplateAction(
                                            label = '今日各地天氣預報',
                                            text = '今日各地天氣預報'
                                        ),
                                        MessageTemplateAction(
                                            label = '不要按我',
                                            text = '不要按我'
                                        ),
                                        MessageTemplateAction(
                                            label = '返回',
                                            text = '返回'
                                        )
                                        
                                    ]
                                )
                            )

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    keyword = ['火車訂票' , '高鐵訂票', '今日運勢', "其他", "今日各地天氣預報", "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座", "水瓶座", "雙魚座", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16","返回", "不要按我"]
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            if(str(machine.state) == "user"): 
                line_bot_api.reply_message(event.reply_token, canmessage)
            elif(str(machine.state) == "state5"):
                line_bot_api.reply_message(event.reply_token, canmessage1)

            continue
        
        for key in keyword:

            if(key == event.message.text): 
                response = machine.advance(event)
                if response == False:
                    if(str(machine.state) == "state3"): 
                        send_text_message(event.reply_token, "輸入錯誤，請再確認一次\n請輸入你的星座:\n牡羊座 請輸入0\n金牛座 請輸入1\n雙子座 請輸入2\n巨蟹座 請輸入3\n獅子座 請輸入4\n處女座 請輸入5\n天秤座 請輸入6\n天蠍座 請輸入7\n射手座 請輸入8\n摩羯座 請輸入9\n水瓶座 請輸入10\n雙魚座 請輸入11\n輸入12返回上一頁")
                    else:
                        send_text_message(event.reply_token, "系統忙碌中")
                print(f"\nFSM STATE: {machine.state}")
                return "OK"
        if(str(machine.state) == "user"): 
            line_bot_api.reply_message(event.reply_token, canmessage)
        elif(str(machine.state) == "state3"): 
            send_text_message(event.reply_token, "輸入錯誤，請再確認一次\n請輸入你的星座:\n牡羊座 請輸入0\n金牛座 請輸入1\n雙子座 請輸入2\n巨蟹座 請輸入3\n獅子座 請輸入4\n處女座 請輸入5\n天秤座 請輸入6\n天蠍座 請輸入7\n射手座 請輸入8\n摩羯座 請輸入9\n水瓶座 請輸入10\n雙魚座 請輸入11\n輸入12返回上一頁")
        elif(str(machine.state) == "state5"):
             line_bot_api.reply_message(event.reply_token, canmessage1)
        else : 
            send_text_message(event.reply_token, "輸入錯誤，請再確認一次")

    print(f"\nFSM STATE: {machine.state}")
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
