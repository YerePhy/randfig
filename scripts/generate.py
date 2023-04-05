import hydra
import yaml
import logging
from random import randint
from pathlib import Path
from omegaconf import DictConfig, OmegaConf
from pyprojroot import here
from randfig import Save


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
    cfg = hydra.utils.instantiate(cfg, _recursive_=True)

    for n in range(cfg["n_random_configs"]):
        init_randfig = {"scanner_name": f"Scanner {n}"}
        out = cfg["compose"](init_randfig)
        Save(
            save_dir=here().joinpath("scanner_randfigs"),
            filename=f"scanner_{n}.yaml",
        )(out)


if __name__ == '__main__':
    main()
