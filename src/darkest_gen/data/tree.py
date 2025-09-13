from __future__ import annotations
from dataclasses import dataclass as component, field

from darkest_gen.data.objects import CorridorObject


@component(order=True, frozen=True)
class RoomNode:
    parent: CorridorNode | None = None
    child_1: CorridorNode | None = None
    child_2: CorridorNode | None = None
    child_3: CorridorNode | None = None
    id: str = "1"


@component(order=True, frozen=True)
class CorridorNode:
    parent: RoomNode
    child: RoomNode
    id: str = "A"
    objects: list[CorridorObject] = field(default_factory=list)
