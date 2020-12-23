"""
 @author: bishisimo
 @time: 2020-12-22 14:42
 """
import json

import requests

from entity.jd_config import JdConfig


class JdGo:

    def __init__(self, item_id="100016672370"):
        self.jdConfig = JdConfig()
        self.goods_id = ""  # 商品id
        self.session = requests.session()  # 会话
        self.item_id = item_id
        self.item_url = None
        self._build_item_url()

    def _build_item_url(self):
        self.item_url = f"{self.jdConfig.item_url_prefix}/{self.item_id}.html"

    def _init_time(self):
        ret = requests.get(self.jdConfig.clock_url).text
        js = json.loads(ret)
        self.time_diff = js.get('serverTime') / 1000 - time.time() + 0.001