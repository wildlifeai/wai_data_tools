import pathlib
import pandas as pd

from typing import Callable
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset
import ai8x


class WildlifeDataset(Dataset):
    def __init__(self, dataset_dir: pathlib.Path, train: bool,  transforms: Callable) -> None:
        """Initialise object. """
        # load csv with labels
        dataframe = pd.read_csv(dataset_dir)
        split_key = "Train" if train else "Test"
        self.dataframe = dataframe[dataframe["split"] == split_key]
        self.dataset_dir = dataset_dir
        self.transforms = transforms

    def __getitem__(self, item):
        image_path = self.dataset_dir / self.dataframe.loc[item, "filename"]
        with Image.open(image_path) as im:
            input_image = im.load()
            input_image = self.transforms(input_image)
        label = self.dataframe.loc[item, "label"]
        return input_image, label

    def __len__(self):
        return len(self.dataframe)


def get_wildlifeai_dataset(data, load_train=True, load_test=True):
    (data_dir, args) = data

    if load_train:
        train_transform = transforms.Compose([
            transforms.RandomCrop(48, padding=4),
            transforms.RandomAffine(degrees=20, translate=(0.1, 0.1), shear=5),
            transforms.ToTensor(),
            ai8x.normalize(args=args)
        ])

        train_dataset = WildlifeDataset(dataset_dir=data_dir, train=True, transforms=train_transform)
    else:
        train_dataset = None

    if load_test:
        test_transform = transforms.Compose([
            transforms.ToTensor(),
            ai8x.normalize(args=args)
        ])

        test_dataset = WildlifeDataset(dataset_dir=data_dir, train=False, transforms=test_transform)

        if args.truncate_testset:
            test_dataset.data = test_dataset.data[:1]
    else:
        test_dataset = None

    return train_dataset, test_dataset
