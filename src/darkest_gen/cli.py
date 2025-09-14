from typer import Typer, Context, echo
# ^ typer é uma biblioteca python criada para facilitar a criação de CLIs
# (interfaces de linha de comando). Aqui importamos algumas funções que usaremos.

from platformdirs import user_data_dir
# ^ platformdirs é uma biblioteca para ajudar a encontrar pastas comuns em diferentes
# plataformas. O user_data_dir pode retornar caminhos de pasta diferentes dependendo
# do OS:
# |  linux: `/home/{user}/.local/share/darkest-gen`
# |  windows: `C:\Users\{user}\AppData\Local\kodiitulip\darkest-gen`

import os
# ^ biblioteca padrao do python para trabalhar com coisas do OS

from darkest_gen.data import State
# ^ State é uma classe contendo informações para o estado atual da aplicação

from darkest_gen.data.objects import CorridorObject
# ^ importando classes de dados sobres os diferentes objetos usados nas dungeons

from darkest_gen.gen import gen

APP_NAME: str = "darkest-gen"
APP_AUTHOR: str = "kodiitulip"
APP_HELP: str = "Uma ferramenta de geração de dungeons"

data_dir: str = user_data_dir(
    APP_NAME, APP_AUTHOR
)  # caminho do diretório de dados da aplicação
data_objects_dir: str = (
    data_dir + "/objects"
)  # caminho do diretório de dados sobre os objetos usados

if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    # caso o diretório nao existe, crie-o

if not os.path.exists(data_objects_dir):
    os.makedirs(data_objects_dir)
    # caso o diretório nao existe, crie-o

app = Typer(name=APP_NAME, help=APP_HELP)
# ^ funcão criada com o Typer que mantem a aplicação funcionando
app.add_typer(gen)
# ^ adicionando a lógica da geração de dungeons


# `@app.callback()` é um marcador para indicar ao Typer que isso é um comando
# existente da aplicação
@app.callback(invoke_without_command=True)
def main(ctx: Context):
    ctx.obj = State()  # `ctx.obj` é um objeto genérico que nos permite salvar o estado
    state: State = ctx.obj  # essa linha existe puramente por questões de autocomplete

    state.corridor_objects = CorridorObject.from_toml(
        data_objects_dir + "/corridor.toml"
    )  # salvando informações sobre os objetos de corredor baseado no arquivo `corridor.toml`

    if ctx.invoked_subcommand is None:
        return echo(ctx.get_help())
        # caso o usuário não chame nenhum comando específico, mostar o texto de ajuda


def no_args_help(ctx: Context):
    """Callback para chamar --help quando não tiver subcomandos"""
    if ctx.invoked_subcommand is None:
        echo(ctx.get_help())
        # caso o usuário não chame nenhum comando específico, mostar o texto de ajuda


if __name__ == "__main__":
    app()
