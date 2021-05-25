import requests
from config import *

def send_msg(title, content):
    data_pushplus = {
        "token": pushplus_token,
        "title": title,
        "content": content.to_html(index=False, justify='center'),
        "template": "markdown"
    }
    data_qmsg = {"msg": content.to_markdown(index=False)}
    data_sc = {"text": title, "desp": content.to_markdown(index=False)}
    if pushplus_token != '':
        requests.post('http://www.pushplus.plus/send', data=data_pushplus)
    if qmsg_key != '':
        requests.post(f'https://qmsg.zendee.cn/send/{qmsg_key}',
                      data=data_qmsg)
    if sc_key != '':
        requests.post(f'https://sc.ftqq.com/{sc_key}.send', data=data_sc)