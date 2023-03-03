"""Default configuration for datasets."""
config = {
    "labels": [
        {"name": "rat", "is_target": True},
        {"name": "weta", "is_target": True},
        {"name": "millipede", "is_target": True},
    ],
    "transformations": {
        "fps": 8,
        "size": [
            48,
            48,
        ],
    },
    "data_split": {"test_size": 0.25},
    "logging": {"logging_dir": "default", "logging_config_file": "default"},
}
