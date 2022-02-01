"""
Module with preprocessing functionality.
"""

from typing import Dict, Tuple

import numpy as np
import torchvision.transforms as torch_trans

transform_translation_table = {
    "img_size": torch_trans.Resize
}


def compose_transforms(transforms_config: Dict[str, Tuple[int, int]]) -> torch_trans.Compose:
    """
    Composes a sequence of transforms based on order in transforms configuration.
    :param transforms_config: Configuration for transforms
    :return: Composed transforms
    """
    transform_list = [torch_trans.ToPILImage()]
    for transform_name, transform_args in transforms_config.items():
        configured_transform = transform_translation_table[transform_name](transform_args)
        transform_list.append(configured_transform)
    transform_list.append(np.asarray)
    sequential_transforms = torch_trans.Compose(transform_list)

    return sequential_transforms
