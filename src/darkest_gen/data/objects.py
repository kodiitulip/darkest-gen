from __future__ import annotations
from dataclasses import dataclass as component
from tomlkit import TOMLDocument, load, table
import os

from tomlkit.items import AoT, Table
from typer import echo


@component(order=True, frozen=True)
class CorridorObject:
    """Classe contendo dados e funções com relação a objetos que corredores podem possuir"""

    name: str
    description: str
    roll: int

    @staticmethod
    def from_toml(path: str) -> list[CorridorObject]:
        """Função que retorna uma lista de objetos de corredor a partir de um documento .toml"""
        if not os.path.exists(path):
            echo(f"Config file {path} not found", err=True, color=True)
            return []

        with open(path, "r", encoding="utf-8") as file:
            data: TOMLDocument = load(file)

        rolls_data: AoT = data.get("rolls", AoT([]))
        rolls = rolls_data.unwrap()

        def mapping_fn(a: dict[str, str | int]) -> CorridorObject:
            return CorridorObject(
                name=str(a.get("nome", "Unknown")),
                description=str(a.get("descricao", "")),
                roll=int(a.get("roll", 1)),
            )

        rolls = list(map(mapping_fn, rolls))

        return rolls

    def to_markdown(self) -> str:
        return ""

    def to_toml_table(self) -> Table:
        corridor_object = (
            table()
            .add("nome", self.name)
            .add("descricao", self.description)
            .add("roll", self.roll)
        )
        return corridor_object
