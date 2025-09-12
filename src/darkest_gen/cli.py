from typer import Typer, Context, echo
from platformdirs import user_data_dir
import os

from darkest_gen.data import State
from darkest_gen.data.objects import CorridorObject

APP_NAME: str = "darkest-gen"
APP_AUTHOR: str = "kodiitulip"
APP_HELP: str = "Uma ferramenta de geração de dungeons"

data_dir: str = user_data_dir(APP_NAME, APP_AUTHOR)
data_objects_dir: str = data_dir + "/objects/"

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(data_objects_dir):
    os.makedirs(data_objects_dir)

app = Typer(name=APP_NAME, help=APP_HELP)


@app.callback(invoke_without_command=True)
def main(ctx: Context):
    ctx.obj = State()
    state: State = ctx.obj
    state.corridor_objects = CorridorObject.from_toml(
        data_objects_dir + "/corridor.toml"
    )

    if ctx.invoked_subcommand is None:
        echo(ctx.obj, color=True)
        return echo(ctx.get_help())


def no_args_help(ctx: Context):
    """Callback para chamar --help quando não tiver subcomandos"""
    if ctx.invoked_subcommand is None:
        echo(ctx.get_help())


if __name__ == "__main__":
    app()
