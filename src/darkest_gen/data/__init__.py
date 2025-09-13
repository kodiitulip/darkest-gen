from __future__ import annotations
from dataclasses import dataclass as component, field

from darkest_gen.data.objects import CorridorObject


@component()
class State:
    """Classe contendo informações sobre o estado da aplicação"""

    corridor_objects: list[CorridorObject] = field(default_factory=list)
