from dataclasses import dataclass

from migration_engine.migrator import MigratorSingleton


@dataclass
class Column[TAdapter]:
    name: str
    data_type: TAdapter
    constraints: TAdapter

    def __init__(self, name: str, migrator: MigratorSingleton, data_type: TAdapter, constraints: TAdapter):
        self.name = name
        self.data_type = data_type
        self.constraints = constraints

    def __str__(self):
        return f'{self.name} {self.data_type} {self.constraints}'
