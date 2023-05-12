"""CLI Group implementation."""
import pathlib
from typing import Optional

import click
import yaml

from wai_data_tools import actions
from wai_data_tools.defaults import default_config
from wai_data_tools.utils import setup_logging


@click.group()
@click.option("--logging-dir", type=click.Path(path_type=pathlib.Path, exists=True), default=None, show_default=True)
@click.option("--logging-config", type=click.Path(path_type=pathlib.Path, exists=True), default=None, show_default=True)
def cli(logging_dir: Optional[pathlib.Path], logging_config: Optional[pathlib.Path]) -> None:
    """CLI Tool for creating and transforming datasets."""
    setup_logging.setup_logging(logging_dir=logging_dir, logging_config_file=logging_config)


@cli.command()
@click.option("--src", default=".", type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("--dest", default="empty_videos", type=click.Path(path_type=pathlib.Path))
@click.option("--dry-run", is_flag=True)
def filter_empty(src: pathlib.Path, dest: pathlib.Path, dry_run: bool) -> None:
    """Copy all non-empty videos to a folder specified by the user.

    Args:
        src: Path that must already exist with the videos to process
        dest: Path, where to dump the files
        dry_run: boolean
    """
    click.echo("Filtering empty videos...")
    actions.filter_empty_videos(src=src, dest=dest, dry_run=dry_run)
    click.echo("Empty videos removed!")


@cli.command()
@click.option("--dataset-name", type=str)
@click.option("--data-dir", type=click.Path(path_type=pathlib.Path))
@click.option("--label-info-path", type=click.Path(path_type=pathlib.Path))
def create_dataset(dataset_name: str, data_dir: pathlib.Path, label_info_path: pathlib.Path) -> None:
    """Create and store dataset."""
    click.echo(f"Creating dataset with name {dataset_name}")
    actions.create_dataset(dataset_name, data_dir, label_info_path)
    click.echo("Dataset created!")


@cli.command()
@click.option("--dataset-name", type=str)
def show_dataset(dataset_name: str) -> None:
    """Show dataset in FiftyOne web app."""
    click.echo("Launching app...")
    actions.show_dataset(dataset_name)
    click.echo("App closed.")


@cli.command()
@click.option("--dataset-name", type=str)
@click.option("--dst", type=click.Path(path_type=pathlib.Path))
@click.option("--export-format", type=str, default=actions.EI_EXPORT_FORMAT, show_default=True)
@click.option("--config-filepath", type=click.Path(path_type=pathlib.Path), default=None)
def export_dataset(
    dataset_name: str, dst: pathlib.Path, export_format: str, config_filepath: Optional[pathlib.Path]
) -> None:
    """Package and export dataset to destination."""
    click.echo(f"Exporting dataset {dataset_name}...")
    actions.export_dataset(dataset_name, dst, export_format=export_format, config_filepath=config_filepath)
    click.echo("Dataset exported!")


@cli.command()
@click.option("--dataset-name", type=str)
def delete_dataset(dataset_name: str) -> None:
    """Delete dataset from database."""
    click.echo(f"Deleting dataset {dataset_name}...")
    actions.delete_dataset(dataset_name)
    click.echo("Dataset deleted!")


@cli.command()
@click.option("--dataset-name", type=str)
@click.option("--anno-key", type=str)
@click.option("--take", default=-1, type=int)
def create_annotation_job(dataset_name: str, anno_key: str, take: int) -> None:
    """Create annotation job in CVAT."""
    click.echo(f"Creating annotation job for dataset {dataset_name}...")
    subset = take if take > 0 else None
    actions.create_annotation_job(dataset_name, anno_key, subset)
    click.echo("Annotation job created!")


@cli.command()
@click.option("--dataset-name", type=str)
@click.option("--anno-key", type=str)
@click.option("--cleanup", default=False, type=str)
def read_annotations(dataset_name: str, anno_key: str, cleanup: bool) -> None:
    """Read annotations from CVAT."""
    click.echo(f"Creating annotation job for dataset {dataset_name}...")
    actions.read_annotations(dataset_name, anno_key, cleanup)
    click.echo("Annotation job created!")


@cli.command()
@click.option("--dst", type=click.Path(path_type=pathlib.Path))
def create_config_file(dst: pathlib.Path) -> None:
    """Generate a default configuration file at destination."""
    click.echo(f"Creating default config file at {dst}...")
    with dst.open(mode="w") as file_stream:
        yaml.dump(default_config.config, file_stream)
    click.echo("Default config file created!")


@cli.command()
def list_datasets() -> None:
    """List datasets in fiftyone database."""
    actions.list_datasets()


@cli.command()
@click.option("--dataset", type=str)
@click.option("--config-filepath", type=click.Path(path_type=pathlib.Path, exists=True))
def preprocess_dataset(dataset_name: str, config_filepath: pathlib.Path) -> None:
    """Preprocess videos according to config."""
    actions.preprocess_dataset(dataset_name=dataset_name, config_filepath=config_filepath)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
