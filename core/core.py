"""
 @author: bishisimo
 @time: 2020-12-22 14:42
 """
import json
import time
from pprint import pp

from lxml import etree

import pendulum
import requests
from loguru import logger

from entity.jd_config import JdConfig
from utils.time_sync import TimeSync


class JdGo:

    def __init__(self, thor, goods_id="100016672370", appoint_time=None):
        self.thor = thor
        self.goods_id = goods_id
        self.appoint_time = appoint_time
        self.jdConfig = JdConfig()
        self.time_sync = TimeSync()
        self.session = requests.session()  # 会话
        self.user_url = self.jdConfig.user_url_format.format(int(time.time() * 1000))
        self.order_url = self.jdConfig.order_url_format.format(self.goods_id)
        self.goods_url = self.jdConfig.item_url_format.format(self.goods_id)
        self.time_diff = 0.1
        self.appoint_url = ''
        self.user_info = None
        self.retry_count = 0
        self.reg_url = "https://search.jd.com/search?keyword=3080&qrst=1&wq=3080&shop=1&ev=exbrand_%E5%BE%AE%E6%98%9F%EF%BC%88MSI%EF%BC%89%5Eexprice_7499-7499%5E&cid3=679"
        # self._login()

    def jd_action(self, url, action=None):
        if action == "post":
            return self.session.post(url, headers=self.jdConfig.headers)
        else:
            return self.session.get(url, headers=self.jdConfig.headers)

    def _login(self):
        self.session.cookies.set("thor", self.thor)
        response = self.jd_action(self.user_url).text.strip('jsonpUserinfo()\n')
        self.user_info = json.loads(response)
        logger.info(self.user_info)
        if not self.user_info.get('nickName'):
            raise Exception("账号验证错误请检查thor")

    def search(self):
        r = self.session.get(url=self.reg_url, headers=self.jdConfig.headers)

    def buy(self):
        if self.appoint_time is not None:
            appoint_time = pendulum.parse(self.appoint_time, tz="local")
            sleep_time = appoint_time.timestamp() - self.time_sync.get_sync_time()
            time.sleep(sleep_time)
        while True:

            if self.make_order():
                return
            else:
                self.retry_count += 1
                if self.retry_count >= self.jdConfig.retry_limit:
                    logger.error("抢购次数达到限制")
                    return
                time.sleep(self.jdConfig.gap)

    def make_order(self):
        self.jdConfig.headers["referer"] = self.goods_url
        self.jd_action(self.order_url)
        if self.retry_count > 0:
            logger.info(f"第{self.retry_count}此重试,重置购物车中...")
            change_num_url = self.jdConfig.change_num_format.format(self.goods_id)
            self.jd_action(change_num_url)
        self.jd_action(self.jdConfig.pay_url)
        response = self.jd_action(self.jdConfig.pay_success, "post")
        order_id = json.loads(response.text).get('orderId')
        if order_id:
            logger.info('抢购成功订单号:{order_id}')
            return True
        return False

    def listen_goods_state(self):
        headers = self.jdConfig.headers.copy()
        logger.info(self.goods_url)
        r = requests.get(self.goods_url, headers=headers)
        root = etree.HTML(r.content)
        print(root.xpath("//a[@id='InitCartUrl']"))
        print(root.xpath("//a[@id='btn-reservation']"))


if __name__ == '__main__':
    jd_thor = ""
    jd = JdGo(jd_thor)
    jd.listen_goods_state()
