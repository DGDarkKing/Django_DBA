from dataclasses import dataclass


@dataclass
class ColumnDataDto:
    name: str
    type: str
    limit: int | None = None
    num_scale: int | None = None
    not_null: bool = False
    default_value: str | None = None


@dataclass
class PkDto:
    name: str
    columns: list[str]

@dataclass
class IndexDto:
    name: str
    columns: list[str]
    is_unique: bool