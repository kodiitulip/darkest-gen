from __future__ import annotations
from dataclasses import dataclass as component
from tomlkit import TOMLDocument, load
import os

from tomlkit.items import AoT
from typer import echo


@component(order=True, frozen=True)
class CorridorObject:
    name: str
    description: str
    roll: int

    @staticmethod
    def from_toml(path: str) -> list[CorridorObject]:
        if not os.path.exists(path):
            echo(f"Config file {path} not found", err=True)
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
