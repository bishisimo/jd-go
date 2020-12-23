"""
 @author: bishisimo
 @time: 2020-12-22 16:49
 """
from dataclasses import dataclass
from pprint import pp
from time import time

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class JdConfig:
    headers = {
        'referer': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    root_url = "https://www.jd.com/"
    clock_url = "https://a.jd.com//ajax/queryServerData.html"
    user_url_prefix = f"https://passport.jd.com/user/petName/getUserInfoForMiniJd.action?&callback=jsonpUserinfo&_="  # 用户信息获取地址
    buy_url = 'https://cart.jd.com/gate.action?pid={}&pcount=1&ptype=1'  # 加购物车
    change_num = 'https://cart.jd.com/changeNum.action?pid={}&pcount=1&ptype=1'  # 修改购物车商品数量为1
    pay_url = 'https://cart.jd.com/gotoOrder.action'  # 下单
    pay_success = 'https://trade.jd.com/shopping/order/submitOrder.action'  # 订单提交
    retry_limit = 100  # 重试次数限制
    gap = 0.1  # 重试间隔
    item_url_prefix = "https://item.jd.com/.html"
