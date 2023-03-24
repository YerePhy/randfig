import hydra
import yaml
import logging
from random import randint
from pathlib import Path
from omegaconf import DictConfig, OmegaConf
from pyprojroot import here


config_path = here().joinpath("configs/config.yaml")
params_stats_path = here().joinpath("scanner_params/params_stats.csv")

log = logging.getLogger(__name__)

with open(params_stats_path, "r") as sf:
    param_stats = yaml.safe_load(sf)

try:
    OmegaConf.register_new_resolver("stats", lambda s: param_stats[s])
except ValueError:
    pass


@hydra.main(
    config_path=str(config_path.parent),
    config_name=str(config_path.name),
    version_base=None
)
def main(cfg: DictConfig):
    """
    Generate random configs.
    """
    OmegaConf.resolve(cfg)
    tfs = hydra.utils.instantiate(cfg, _recursive_=True)
    out_cfg = tfs({})
    log.info(out_cfg)


if __name__ == '__main__':
    main()
