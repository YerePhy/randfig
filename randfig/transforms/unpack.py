from typing import Sequence, Mapping, Any
from randfig.transforms.config_transform import ConfigTransform
from randfig.utils import unpack


__all__ = ["Unpack"]


class Unpack(ConfigTransform):
    """
    Wrapper of :py:func:`randifg.utils.unpack`.
    It unpacks the values assocaited to a sequence of
    keys.

    .. exec_code::

        # --- hide: start ---
        from randfig import Unpack
        # --- hide: stop ---

        init_config = {"key": [0, 1]}
        unpack = Unpack(keys=["key"], new_keys=[["key_0", "key_1"]], remove=True)
        unpacked = unpack(init_config)

        # --- hide: start ---
        print(f"unpacked: {unpacked}")
        # --- hide: stop ---
    """

    def __init__(self, keys: Sequence[str], new_keys: Sequence[Sequence[Any]], remove: bool = False) -> None:
        """
        Args:
            keys: keys whose values will be unpakced
            new_keys: a sequence of sequence with the names for the new keys.
            remove: whether to remove each key in ``keys`` afeter unpacking or not.
        """
        super().__init__(keys)
        self.new_keys = new_keys
        self.remove = remove

    def __call__(self, cfg: Mapping) -> Mapping:
        self._check_mapping(cfg)

        for k, nk in zip(self.keys, self.new_keys):
            cfg = unpack(cfg, k, nk, self.remove)

        return cfg
