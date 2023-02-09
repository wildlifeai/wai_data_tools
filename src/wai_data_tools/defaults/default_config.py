"""Default configuration for datasets."""
config = {
    "labels": [
        {"name": "rat", "is_target": True, "sampling_frequency": 1},
        {"name": "weta", "is_target": True, "sampling_frequency": 1},
        {"name": "millipede", "is_target": True, "sampling_frequency": 2},
    ],
    "preprocessing": {
        "transformations": {
            "img_size": [
                48,
                48,
            ]
        }
    },
    "data_split": {"test_size": 0.25},
    "logging": {"logging_dir": "default", "logging_config_file": "default"},
}
