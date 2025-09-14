"""
Esse código manterá todas as informações e lógica
para a geração de dungeons
"""

from __future__ import annotations

from typer import Context, Typer
from random import choice, randint, random

from darkest_gen.data import State
from darkest_gen.data.tree import CorridorNode, RoomNode

gen = Typer(name="generate")


@gen.callback(invoke_without_command=True)
def generate_dungeon(
    ctx: Context, path: str = "./datasym/output.md", boss: bool = False
):
    """Gera uma dungeon"""
    # state: State = ctx.obj  # estado atual da aplicação

    depth = choice([6, 8, 10]) + 1 if boss else 0
    # ^ A "profundidade" da dungeon. Quantas salas possui. Caso tenha um boss será adicionada 1 sala
    rooms = []

    def gen_corridor(parent: RoomNode) -> CorridorNode | None:
        if len(rooms) >= depth:
            return None
            # ^ caso a quantidade de salas for igual a `depth` então não retornamos nada
        corr = CorridorNode(parent=parent)
        corr.child = gen_room(corr)
        return corr

    def gen_room(parent: CorridorNode) -> RoomNode:
        room = RoomNode(parent=parent)

        randchance = random() < 0.3
        # ^ random chance to have more than one corridor

        num_of_corridors = randint(1, 3) if randchance else 1
        children = [gen_corridor(room) for _ in range(num_of_corridors)]
        # ^ habilidade incrível do python de colocar "for loops" dentro de uma
        # lista para gerar ela

        room.children = children
        rooms.append(room)
        # ^ colocando cada sala gerada em uma lista eu posso manter acesso rápido
        # a cada sala e tbm saber Quantas salas foram geradas
        return room

    root = RoomNode()
    rooms.append(root)
    root.children.append(gen_corridor(root))
