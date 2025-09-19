from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import TypedDict
from random import randint, choice


class TreasureRank(Enum):
    NONE = 0
    GRAUI = 1
    GRAUII = 2
    GRAUIII = 3


class DangerType(Enum):
    NONE = ""
    BLEEDING = "Sangrar"
    DISEASE = "Doença"
    POISON = "Veneno"
    DISTURB = "Perturbar"
    TIRE = "Cansar"


# WARNING: Lista de objetos temporaria
TEMPOBJECTS: list[DungeonObject] = [
    {
        "name": "Temp",
        "description": "Temp",
        "danger": DangerType.POISON,
        "treasure": TreasureRank.NONE,
    }
]


class DungeonObject(TypedDict):
    name: str
    description: str
    treasure: TreasureRank
    danger: DangerType


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
            # TODO: addicionar os objetos das salas e
            # adicionar uma função para que os objetos
            # sejam selecionados por dados
            room = Room(id, combat=True, objects=choice(TEMPOBJECTS))
        else:
            room = Room(id, combat=True)
        return room


@dataclass(order=True, kw_only=True)
class Corridor:
    id: str = field(kw_only=False)
    origin: Room
    destination: Room
    objects: list[DungeonObject] = field(default_factory=list)
    fight: int = 0
    trap: int = 0
    treasure: bool = False
    collector: bool = False

    def endpoints(self) -> tuple[Room, Room]:
        """Retorna as salas conectadas na ordem (origem, destino)"""
        return self.origin, self.destination

    # TODO: gerar um corredor aleatório com objetos
    @staticmethod
    def generate_random() -> Corridor:
        """Gera um corredor aleatório com seus devidos atributos"""
        ...


@dataclass(kw_only=True, order=True)
class Dungeon:
    corridors: list[Corridor] = field(default_factory=list)
    rooms: list[Room] = field(default_factory=list)

    def rooms_count(self) -> int:
        """Retorna a quantidade de salas na masmorra"""
        return len(self.rooms)

    # NOTE: remover caso não seja usado
    def corridors_count(self) -> int:
        """Retorna a quantidade de corredores na masmorra"""
        return len(self.corridors)

    # NOTE: remover caso não seja usado
    def get_corridor(self, room1: Room, room2: Room) -> Corridor | None:
        for corr in self.corridors:
            if room1 in corr.endpoints() and room2 in corr.endpoints():
                return corr
        return None

    def insert_room(self, room: Room) -> None:
        """Adiciona uma sala à masmorra"""
        self.rooms.append(room)

    # NOTE: remover caso não seja usado
    def insert_rooms(self, rooms: list[Room]) -> None:
        """Insere todas as salas da lista à masmorra"""
        self.rooms.extend(rooms)

    def insert_corridor(self, corridor: Corridor) -> None:
        """Insere um corredor à masmorra"""
        self.corridors.append(corridor)

    # NOTE: remover caso não seja usado
    def insert_corridors(self, corridors: list[Corridor]) -> None:
        self.corridors.extend(corridors)

    def generate_corridor(self, room1: Room, room2: Room, *, id: str) -> None:
        """gera um corredor conectado as salas oferecidas com o id fornecido"""
        corr = Corridor(id, origin=room1, destination=room2)
        self.insert_corridor(corr)
        if room1 not in self.rooms:
            self.insert_room(room1)
        if room2 not in self.rooms:
            self.insert_room(room2)

    # NOTE: remover caso não seja usado
    def remove_room(self, room: Room) -> None:
        self.corridors = [
            corr for corr in self.corridors if room not in corr.endpoints()
        ]
        if room in self.rooms:
            self.rooms.remove(room)

    # NOTE: remover caso não seja usado
    def remove_corridor(self, corridor: Corridor) -> None:
        self.corridors.remove(corridor)

    # TODO: transformar a dungeon em um markdown bem formatado
    def to_markdown(self) -> str:
        """Gera um texto markdown formatado com os atributos da masmorra"""
        ...

    @staticmethod
    def generate_random_dungeon(*, boss: bool = False) -> Dungeon:
        """Gera uma masmorra aleatória"""
        dungeon = Dungeon()
        size = choice([6, 8, 10]) + (1 if boss else 0)

        for r in range(size):
            # TODO: permitir que a dungeon tenha caminhos birfurcados
            # no momento ela so consegue criar caminhos lineares
            pastroom = None if dungeon.rooms_count() == 0 else dungeon.rooms[r - 1]
            if pastroom is None:
                # aqui eh a sala raiz
                dungeon.insert_room(room=Room.generate_random(id=r + 1))
                continue
            # aqui eh uma sala conectada por um corredor
            currroom = Room.generate_random(id=r + 1)
            # TODO: permitir que os ids dos corredores possam receber uma letra
            # em ordem alfabetica
            dungeon.generate_corridor(pastroom, currroom, id="A")

        return dungeon


def main():
    dun = Dungeon.generate_random_dungeon()
    print(dun)


if __name__ == "__main__":
    main()
