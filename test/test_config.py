"""
 @author: bishisimo
 @time: 2020-12-22 15:12
 """
import hydra

from entity.jd_config import JdConfig
from utils.config import Config


def test_config():
    @hydra.main(config_path="../", config_name="config")
    def my_app(cfg: JdConfig) -> None:
        print(cfg)
