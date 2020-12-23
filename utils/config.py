"""
 @author: bishisimo
 @time: 2020-12-22 14:46
 """
import hydra
from omegaconf import DictConfig, OmegaConf

from utils.tool import singleton


@singleton
class Config:
    def __init__(self, config_path="", config_name="config"):
        self.config_path = config_path
        self.config_name = config_name
        self.config = None
        self._init_config()

    def _init_config(self):
        @hydra.main(config_path=self.config_path, config_name=self.config_name)
        def _config(cfg: DictConfig):
            self.config = cfg

        _config()

    def select(self, key):
        return OmegaConf.select(self.config, key)


@hydra.main(config_path='../', config_name="config")
def get_config(cfg: DictConfig):
    print(OmegaConf.select(cfg, "db"))


if __name__ == '__main__':
    c = Config("../")
    assert c.config is not None
    print(c.select("jd"))
