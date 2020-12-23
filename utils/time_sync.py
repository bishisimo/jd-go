"""
 @author: bishisimo
 @time: 2020-12-23 9:01
 """
import json
from loguru import logger
import requests
import pendulum
from sys import platform

from entity.jd_config import JdConfig


class TimeSync:
    def __init__(self):
        self.jdConfig = JdConfig
        self.offset = self.get_offset()

    def show_time(self):
        local_time = pendulum.now()
        remote_time = self.get_jd_time()
        fmt = "YYYY-MM-DD hh:mm:ss"
        logger.info(
            f"jd_time:{remote_time.format(fmt)},self_time:{local_time.format(fmt)},diff:{local_time.diff(remote_time).microseconds}us")

    def get_jd_time(self):
        url = self.jdConfig.clock_url
        ret = requests.get(url).text
        js = json.loads(ret)
        return pendulum.from_timestamp(js.get('serverTime') / 1000, tz="local")

    def get_offset(self):
        local_time = pendulum.now().timestamp()
        remote_time = self.get_jd_time().timestamp()
        return local_time - remote_time

    def get_sync_time(self):
        return pendulum.now().timestamp() - self.offset


if __name__ == '__main__':
    ts = TimeSync()
    print(ts.get_sync_time())
