from typing import Callable
from typer.testing import CliRunner
import typer
import pytest
from skibidi_orm.cli.run import app
import importlib
import py  # type: ignore

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


def test_studio_no_options_too_many_schemas(tmpdir: py.path.local):  # type: ignore
    file_path = tmpdir.join("schema.py")  # type: ignore
    file_path2 = tmpdir.mkdir("other").join("schema.py")  # type: ignore
    file_path.write("")  # type: ignore
    file_path2.write("")  # type: ignore
    result = runner.invoke(app, ["studio"])
    assert result.exit_code == 1
    assert (
        "Multiple schema files found. Please specify the schema file to use: --schema-file <PATH>"
        in result.stdout
    )
    tmpdir.remove()


def test_studio_one_schema_option(monkeypatch: pytest.MonkeyPatch, tmpdir: py.path.local):  # type: ignore
    import skibidi_orm.migration_engine.studio.server  # type: ignore

    def mock_func(schema_file: str):
        print("Success test", end="")

    monkeypatch.setattr(
        "skibidi_orm.migration_engine.studio.server.run_server", mock_func
    )
    importlib.reload(skibidi_orm.cli.run)  # type: ignore

    file_path = tmpdir.join("schema.py")  # type: ignore
    file_path.write("")  # type: ignore

    result = runner.invoke(
        app, ["studio", "--schema-file", file_path.strpath]  # type: ignore
    )

    assert "Success test" in result.stdout
    tmpdir.remove()
