from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import TypedDict
from random import randint, choice, random
from tomllib import load

ALPHAIDS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class TreasureRank(Enum):
    NONE = 0
    GRAUI = 1
    GRAUII = 2
    GRAUIII = 3


class DangerType(Enum):
    NONE = "Nenhum"
    BLEEDING = "Sangrar"
    DISEASE = "Doença"
    POISON = "Veneno"
    DISTURB = "Perturbar"
    TIRE = "Cansar"


class DungeonObject(TypedDict):
    name: str
    description: str
    treasure: TreasureRank
    danger: DangerType


class CorridorAttributes(TypedDict):
    fights: int
    objects: int
    traps: int
    treasure: bool
    collector: bool


def read_room_objects() -> list[DungeonObject]:
    with open("dungeon_objects.toml", "rb") as file:
        toml = load(file)
    if toml["room_objects"] is None:
        raise ValueError(
            'dungeon_objects.toml is invalid as it does not contain a "room_objects" Array!'
        )
    objs = [DungeonObject(obj) for obj in toml["room_objects"]]
    return objs


def read_corridor_objects() -> list[DungeonObject]:
    with open("dungeon_objects.toml", "rb") as file:
        toml = load(file)
    if toml["corridor_objects"] is None:
        raise ValueError(
            'dungeon_objects.toml is invalid as it does not contain a "corridor_objects" Array!'
        )
    objs = [DungeonObject(obj) for obj in toml["corridor_objects"]]
    return objs


CORRIDOR_ATTRIBUTE_TABLE = {
    1: CorridorAttributes(
        fights=1, objects=0, traps=0, treasure=False, collector=False
    ),
    2: CorridorAttributes(
        fights=1, objects=1, traps=0, treasure=False, collector=False
    ),
    3: CorridorAttributes(
        fights=1, objects=2, traps=0, treasure=False, collector=False
    ),
    4: CorridorAttributes(
        fights=1, objects=3, traps=0, treasure=False, collector=False
    ),
    5: CorridorAttributes(
        fights=1, objects=0, traps=0, treasure=False, collector=False
    ),
    6: CorridorAttributes(
        fights=2, objects=0, traps=0, treasure=False, collector=False
    ),
    7: CorridorAttributes(
        fights=3, objects=0, traps=0, treasure=False, collector=False
    ),
    8: CorridorAttributes(
        fights=0, objects=2, traps=0, treasure=False, collector=False
    ),
    9: CorridorAttributes(
        fights=0, objects=3, traps=0, treasure=False, collector=False
    ),
    10: CorridorAttributes(
        fights=0, objects=0, traps=0, treasure=False, collector=False
    ),
    11: CorridorAttributes(
        fights=1, objects=0, traps=1, treasure=False, collector=False
    ),
    12: CorridorAttributes(
        fights=2, objects=1, traps=0, treasure=False, collector=False
    ),
    13: CorridorAttributes(
        fights=2, objects=2, traps=0, treasure=False, collector=False
    ),
    14: CorridorAttributes(
        fights=1, objects=1, traps=1, treasure=False, collector=False
    ),
    15: CorridorAttributes(
        fights=1, objects=2, traps=1, treasure=False, collector=False
    ),
    16: CorridorAttributes(
        fights=1, objects=1, traps=2, treasure=False, collector=False
    ),
    17: CorridorAttributes(
        fights=1, objects=2, traps=2, treasure=False, collector=False
    ),
    18: CorridorAttributes(
        fights=0, objects=0, traps=0, treasure=True, collector=False
    ),
    19: CorridorAttributes(
        fights=3, objects=0, traps=2, treasure=False, collector=False
    ),
    20: CorridorAttributes(
        fights=0, objects=0, traps=0, treasure=False, collector=True
    ),
}
CORRIDOR_OBJECTS_TABLE: list[DungeonObject] = read_corridor_objects()
ROOM_OBJECTS_TABLE: list[DungeonObject] = read_room_objects()


@dataclass(order=True, kw_only=True)
class Room:
    id: int = field(kw_only=False)
    objects: DungeonObject | None = None
    treasure: bool = False
    combat: bool = False

    @staticmethod
    def generate_random(*, id: int = 0) -> Room:
        """Gera uma sala aleatória com seus devidos atributos"""
        content_dice = randint(1, 10)
        room: Room
        if 1 <= content_dice <= 5:
            room = Room(id)
        elif 6 <= content_dice <= 7:
            room = Room(id, treasure=True, combat=True)
        elif 8 <= content_dice <= 9:
            room = Room(id, combat=True, objects=choice(ROOM_OBJECTS_TABLE))
        else:
            room = Room(id, combat=True)
        return room

    def get_markdown(self) -> str:
        md = (
            [f"### Sala {self.id}"]
            + (
                [
                    f"{" " * 4}- Combate",
                    *[f"{" " * 8}{i+1}. Inimigo Teste" for i in range(4)],
                ]
                if self.combat
                else []
            )
            + (
                [
                    f"{" " * 4}- {self.objects["name"]}\n{" " * 6}{self.objects["description"]}",
                ]
                if self.objects
                else []
            )
            + (
                [
                    f"{" " * 4}- Tesouro III",
                    *[f"{" " * 8}- Item Teste" for _ in range(3)],
                ]
                if self.treasure
                else []
            )
        )
        return "\n\n".join(md)


@dataclass(order=True, kw_only=True)
class Corridor:
    id: str = field(kw_only=False)
    origin: Room
    destination: Room
    attributes: CorridorAttributes
    objects: list[DungeonObject] = field(default_factory=list)
    fights: list = field(default_factory=list)

    def endpoints(self) -> tuple[Room, Room]:
        """Retorna as salas conectadas na ordem (origem, destino)"""
        return self.origin, self.destination

    @staticmethod
    def generate_random(*, origin: Room, destination: Room, id: str = "A") -> Corridor:
        """Gera um corredor aleatório com seus devidos atributos"""
        content_dice: int = randint(1, 20)
        attr: CorridorAttributes = CORRIDOR_ATTRIBUTE_TABLE[content_dice]
        corr: Corridor = Corridor(
            id, origin=origin, destination=destination, attributes=attr
        )
        for _ in range(attr["objects"]):
            corr.objects.append(choice(CORRIDOR_OBJECTS_TABLE))

        return corr

    def get_markdown(self) -> str:
        md = (
            [f"### Corredor {self.id}"]
            + [
                "\n\n".join(
                    [f"{" "*4}- Combate"]
                    + [f"{" "*6}{i + 1}. Inimigo Teste" for i in range(3)]
                )
                for _ in range(self.attributes["fights"])
            ]
            + [
                "\n".join(
                    [f"{" "*4}- {obj["name"]}"]
                    + ([f"{" "*6}{obj["description"]}"] if obj["description"] else [])
                )
                for obj in self.objects
            ]
        )

        return "\n\n".join(md)


@dataclass(kw_only=True, order=True)
class Dungeon:
    corridors: list[Corridor] = field(default_factory=list)
    rooms: list[Room] = field(default_factory=list)

    def rooms_count(self) -> int:
        """Retorna a quantidade de salas na masmorra"""
        return len(self.rooms)

    def insert_room(self, room: Room) -> None:
        """Adiciona uma sala à masmorra"""
        self.rooms.append(room)

    def insert_corridor(self, corridor: Corridor) -> None:
        """Insere um corredor à masmorra"""
        self.corridors.append(corridor)

    def generate_corridor(self, origin: Room, destination: Room, *, id: str) -> None:
        """gera um corredor conectado as salas oferecidas com o id fornecido"""
        corr = Corridor.generate_random(origin=origin, destination=destination, id=id)
        self.insert_corridor(corr)
        if origin not in self.rooms:
            self.insert_room(origin)
        if destination not in self.rooms:
            self.insert_room(destination)

    def to_markdown(self) -> str:
        """Gera um texto em formato MARKDOWN, com as informações da masmorra formatado"""
        doc = """# Masmorra

## Salas

---

"""
        doc += "\n\n".join([room.get_markdown() for room in self.rooms])
        doc += """

## Corredores

---

"""
        doc += "\n\n".join([corr.get_markdown() for corr in self.corridors])
        doc += "\n"
        return doc

    @staticmethod
    def generate_random_dungeon(*, boss: bool = False) -> Dungeon:
        """Gera uma masmorra aleatória"""
        dungeon = Dungeon()
        size = choice([6, 8, 10]) + (1 if boss else 0)

        for r in range(size):
            pastroom = None if dungeon.rooms_count() == 0 else dungeon.rooms[r - 1]
            if dungeon.rooms_count() >= 2 and random() < 0.3:
                pastroom = dungeon.rooms[r - 2]
            if pastroom is None:
                # aqui eh a sala raiz
                dungeon.insert_room(room=Room.generate_random(id=r + 1))
                continue

            # aqui eh uma sala conectada por um corredor
            currroom = Room.generate_random(id=r + 1)
            dungeon.generate_corridor(pastroom, currroom, id=ALPHAIDS[r])

        return dungeon


def main():
    dun = Dungeon.generate_random_dungeon()
    doc = dun.to_markdown()
    with open("TEST.md", "w+", encoding="utf-8") as output_file:
        output_file.write(doc)


if __name__ == "__main__":
    main()
