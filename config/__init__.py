import os.path as osp
import yaml

# 현재 파일의 디렉터리 위치
here = osp.dirname(osp.abspath(__file__))

def get_config():
    config_file = osp.join(here, "config.yaml")
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Global configuration
CONFIG = get_config()