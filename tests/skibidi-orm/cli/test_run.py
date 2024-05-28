from os import path
import os
from typing import Callable
from typer.testing import CliRunner
import typer
import pytest
from skibidi_orm.cli.run import app
import importlib

runner = CliRunner()


@pytest.fixture
def mock_input_id(monkeypatch: pytest.MonkeyPatch):
    def mock_input(prompt: pytest.MonkeyPatch):
        return "1"

    monkeypatch.setattr(typer, "prompt", mock_input)


def test_list_migrations():
    result = runner.invoke(app, ["list-migrations"])
    assert result.exit_code == 0
    assert "Listing all migrations" in result.stdout


def test_go():
    result = runner.invoke(app, ["go", "1"])
    assert result.exit_code == 0
    assert "Going to migration with ID: 1" in result.stdout


def test_go_no_migration_id(mock_input_id: pytest.MonkeyPatch):
    result = runner.invoke(app, ["go"])
    assert result.exit_code == 0
    assert "Going to migration with ID: 1" in result.stdout


def test_studio_no_options_too_many_schemas(clear_local_tmp_dir):  # type: ignore
    file_path = "./tmp/test/studio/schema.py"
    file_path2 = "./tmp/test/studio/other/schema.py"
    os.makedirs(path.dirname(file_path))
    os.makedirs(path.dirname(file_path2))
    with open(file_path, "w") as f:
        f.write("")
    with open(file_path2, "w") as f:
        f.write("")
    result = runner.invoke(app, ["studio"])
    assert result.exit_code == 1
    assert (
        "Multiple schema files found. Please specify the schema file to use: --schema-file <PATH>"
        in result.stdout
    )


def test_studio_one_schema_option(monkeypatch: pytest.MonkeyPatch, clear_local_tmp_dir):  # type: ignore
    import skibidi_orm.migration_engine.studio.server  # type: ignore

    mock_func: Callable[[str], None] = lambda schema_file: print("Success test", end="")
    monkeypatch.setattr(
        "skibidi_orm.migration_engine.studio.server.run_server", mock_func
    )
    importlib.reload(skibidi_orm.cli.run)  # type: ignore

    file_path = "./tmp/schema.py"
    with open(file_path, "w") as f:
        f.write("")

    result = runner.invoke(app, ["studio", "--schema-file", file_path])

    assert "Success test" == result.stdout
