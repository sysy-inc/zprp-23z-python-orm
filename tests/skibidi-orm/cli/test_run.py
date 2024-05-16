from typer.testing import CliRunner
import typer
import pytest
from skibidi_orm.cli.run import app

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
