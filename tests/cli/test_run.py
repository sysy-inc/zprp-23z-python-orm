from typer.testing import CliRunner

from skibidi_orm.cli.run import app

runner = CliRunner()


def test_migration():
    result = runner.invoke(app, ["migrate", "-m", "test message"])
    assert result.exit_code == 0
    assert "Running migration with message: test message" in result.stdout


def test_list_migrations():
    result = runner.invoke(app, ["list-migrations"])
    assert result.exit_code == 0
    assert "Listing all migrations" in result.stdout


def test_go():
    result = runner.invoke(app, ["go", "1"])
    assert result.exit_code == 0
    assert "Going to migration with ID: 1" in result.stdout


def test_migrate_no_message():
    result = runner.invoke(app, ["migrate"])
    assert result.exit_code == 0
    assert "Please enter a message for the migration:" in result.stdout


def test_go_no_migration_id():
    result = runner.invoke(app, ["go"])
    assert result.exit_code == 0
    assert "Please enter the migration ID:" in result.stdout
