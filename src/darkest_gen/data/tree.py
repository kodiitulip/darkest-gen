from __future__ import annotations
from dataclasses import dataclass as component, field

from darkest_gen.data.objects import CorridorObject


@component(order=True, kw_only=True)
class RoomNode:
    parent: CorridorNode | None = None
    children: list[CorridorNode | None] = field(default_factory=list)
    id: str = "1"


@component(order=True, kw_only=True)
class CorridorNode:
    parent: RoomNode
    child: RoomNode | None = None
    id: str = "A"
    objects: list[CorridorObject] = field(default_factory=list)
