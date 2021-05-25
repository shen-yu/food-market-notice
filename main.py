import requests
import json
import pandas as pd
from config import markets
from sendmsg import *

base_url = 'http://nmpt.zjamr.zj.gov.cn'

headers = {
    'User-Agent':
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Cookie': 'SESSION=Nzc0OGViN2YtNmNhZi00NmQ2LTlmNjUtMTUwNWE5MjBhN2Zh'
}
df = pd.DataFrame()


def get_response(html_url):
    response = requests.get(url=html_url, headers=headers)
    response.encoding = response.apparent_encoding
    return response


def get_market_price(keyword):
    r = get_response(f'{base_url}/scmarket/allNoQueryParams?name={keyword}')
    res = json.loads(r.text)
    name = res['markets'][0]['name']
    id = res['markets'][0]['id']

    r2 = get_response(f'{base_url}/spgoods/getGoodsPrice?marketid={id}')
    res2 = json.loads(r2.text)['newPrice']
    data = pd.DataFrame(res2).set_index('index')
    data['market'] = name
    return data


for i in markets:
    df = pd.concat([df, get_market_price(i)], ignore_index=True)

data = df.sort_values(by=['good_name'])
data.drop(columns=['gather_time'], inplace=True)
data.columns = ['最高价格', '最低价格', '平均价格', '商品', '市场']

if __name__ == '__main__':
    send_msg('今日菜价', data)
