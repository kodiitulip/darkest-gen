from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import TypedDict
from random import randint, choice, random
from snakemd import Document, Heading, MDList
from odf.opendocument import OpenDocumentText

ALPHAIDS = "abcdefghijklmnopqrstuvwxyz"


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
CORRIDOR_OBJECTS_TABLE = {
    1: DungeonObject(
        name="Confessionário",
        description="Lodo da Madre - Recupera 2d4 de **SAN**",
        treasure=TreasureRank.GRAUI,
        danger=DangerType.NONE,
    ),
    2: DungeonObject(
        name="Urna de Votos",
        description="Lodo da Madre - Aumenta o tesouro pra II",
        treasure=TreasureRank.GRAUI,
        danger=DangerType.NONE,
    ),
    3: DungeonObject(
        name="Gabinete de Objetos",
        description="Grampos de Ferro - Aumenta o tesouro pra II",
        treasure=TreasureRank.GRAUI,
        danger=DangerType.POISON,
    ),
    4: DungeonObject(
        name="Estante de Livros",
        description="",
        treasure=TreasureRank.GRAUI,
        danger=DangerType.DISTURB,
    ),
    5: DungeonObject(
        name="Mesa de Químicos",
        description="Ervas Batidas - Evitar o perigo",
        treasure=TreasureRank.GRAUI,
        danger=DangerType.DISEASE,
    ),
    6: DungeonObject(
        name="Caixas e Mochilas",
        description="",
        treasure=TreasureRank.GRAUI,
        danger=DangerType.NONE,
    ),
    7: DungeonObject(
        name="Altar de Ossos",
        description="Incenso de Cera - Evita o perigo e cura 2d4 **SAN**",
        treasure=TreasureRank.NONE,
        danger=DangerType.DISTURB,
    ),
    8: DungeonObject(
        name="Haste com Cristal",
        description="Nada - Ganha um Cristal Ígneo",
        treasure=TreasureRank.NONE,
        danger=DangerType.NONE,
    ),
    9: DungeonObject(
        name="Parede de Escombros",
        description="Pá e Picareta - elimina o obstáculo",
        treasure=TreasureRank.NONE,
        danger=DangerType.TIRE,
    ),
    10: DungeonObject(
        name="Baú de Tesouro",
        description="Grampos de Ferro - Evita o Perigo",
        treasure=TreasureRank.GRAUII,
        danger=DangerType.BLEEDING,
    ),
}
ROOM_OBJECTS_TABLE = [
    DungeonObject(
        name="Altar Sacro",
        description="Lodo da Madre - Receba +1d6 de _atk_ ou _dano_",
        treasure=TreasureRank.NONE,
        danger=DangerType.NONE,
    ),
    DungeonObject(
        name="Pedra de Sacrifício",
        description="Incenso de Cera",
        treasure=TreasureRank.GRAUI,
        danger=DangerType.DISTURB,
    ),
    DungeonObject(
        name="Sarcófago",
        description="Ervas Batidas - Aumenta tesouro para III",
        treasure=TreasureRank.GRAUII,
        danger=DangerType.DISEASE,
    ),
    DungeonObject(
        name="Tenda de Acampamento",
        description="Incenso de Cera",
        treasure=TreasureRank.GRAUII,
        danger=DangerType.DISTURB,
    ),
]


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

    def get_markdown(self) -> tuple[ Heading , list[ MDList ] ]:
        heading = Heading(f"Sala {self.id}", 3)
        combat_list = MDList( [
            Heading("Combate\n", 4),
            MDList( [Heading( f"Inimigo Teste {i+1}" + ( "\n" if i != 3 else "" ), 5 ) for i in range(4) if self.combat], True )
        ] )
        treasure_list = MDList( [
            Heading("Tesouro III\n", 4),
            MDList( [Heading( "Item Teste" + ( "\n" if i != 2 else "" ), 5 ) for i in range(3) if self.treasure] )
        ] )
        attr = []
        if self.combat:
            attr.append(combat_list)
        if self.treasure:
            attr.append(treasure_list)
        return heading, attr


@dataclass(order=True, kw_only=True)
class Corridor:
    id: str = field(kw_only=False)
    origin: Room
    destination: Room
    attributes: CorridorAttributes
    objects: list[DungeonObject] = field(default_factory=list)

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
            content_dice = randint(1, 10)
            corr.objects.append(CORRIDOR_OBJECTS_TABLE[content_dice])

        return corr


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

    def generate_corridor(self, origin: Room, destination: Room, *, id: str) -> None:
        """gera um corredor conectado as salas oferecidas com o id fornecido"""
        corr = Corridor.generate_random(origin=origin, destination=destination, id=id)
        self.insert_corridor(corr)
        if origin not in self.rooms:
            self.insert_room(origin)
        if destination not in self.rooms:
            self.insert_room(destination)

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

    def to_markdown(self) -> Document:
        """Gera um texto em formato MARKDOWN, com as informações da masmorra formatado"""
        doc = Document()
        doc.add_heading("Masmorra")
        doc.add_heading("Mapa", 2)
        doc.add_raw("Inserir Mapa aqui")
        doc.add_heading("Salas", 2)
        doc.add_horizontal_rule()

        for room in self.rooms:
            heading, attr_list = room.get_markdown()
            doc.add_block(heading)
            for attr in attr_list:
                doc.add_block(attr)

        doc.add_raw("")
        doc.dump("TEST")
        return doc

    def to_odf_doc(self) -> None:
        doc = OpenDocumentText()
        doc.save("TEST.odt")
        ...

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
    print(dun.to_markdown())
    dun.to_odf_doc()


if __name__ == "__main__":
    main()
