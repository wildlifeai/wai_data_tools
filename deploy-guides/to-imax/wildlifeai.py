"""Wildlife.ai dataloader functions."""
import pathlib
from typing import Callable

import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
from sklearn.preprocessing import LabelEncoder

import ai8x


DATASET_DIR = "/PATH/TO/DATASET"


class WildlifeDataset(Dataset):
    """Dataset object for wildlife.ai images."""

    def __init__(self, dataset_dir: pathlib.Path, train: bool, transform: Callable) -> None:
        """Initialise object."""
        # load csv with labels
        dataframe = pd.read_csv(dataset_dir / "frame_information.csv")
        dataframe["label_encoded"] = LabelEncoder().fit_transform(dataframe["label"])
        split_key = "Train" if train else "Test"
        self.dataframe = dataframe[dataframe["split"] == split_key].reset_index()
        self.dataset_dir = dataset_dir
        self.transform = transform

    def __getitem__(self, item):
        """Get item."""
        image_path = (
            self.dataset_dir
            / "dataset"
            / self.dataframe.loc[item, "video_name"]
            / self.dataframe.loc[item, "file_name"]
        )
        with Image.open(image_path) as image:
            input_image = self.transform(image)
        label = self.dataframe.loc[item, "label_encoded"]
        return input_image, label

    def __len__(self):
        """Get size of dataset."""
        return len(self.dataframe)


def get_wildlifeai_dataset(data, load_train=True, load_test=True):
    """Get dataset."""
    (data_dir, args) = data

    data_dir = pathlib.Path(DATASET_DIR)

    if load_train:
        train_transform = transforms.Compose(
            [
                transforms.Resize((28, 28)),
                transforms.RandomAffine(degrees=20, translate=(0.1, 0.1), shear=5),
                transforms.ToTensor(),
                ai8x.normalize(args=args),  # pylint: disable=undefined-variable
            ]
        )

        train_dataset = WildlifeDataset(dataset_dir=data_dir, train=True, transform=train_transform)
    else:
        train_dataset = None

    if load_test:
        test_transform = transforms.Compose(
            [
                transforms.Resize((28, 28)),
                transforms.ToTensor(),
                ai8x.normalize(args=args)
            ]  # pylint: disable=undefined-variable
        )

        test_dataset = WildlifeDataset(dataset_dir=data_dir, train=False, transform=test_transform)

        if args.truncate_testset:
            test_dataset.data = test_dataset.data[:1]  # pylint: disable=attribute-defined-outside-init
    else:
        test_dataset = None

    return train_dataset, test_dataset


datasets = [
    {
        'name': 'WILDLIFE',
        'input': (3, 28, 28),
        'output': list(map(str, range(3))),
        'loader': get_wildlifeai_dataset,
    },
]
