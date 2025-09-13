# Esse arquivo é um arquivo especial que permite que o python
# use a pasta atual como um "pacote"


def main():
    from darkest_gen.cli import app
    # ^ estamos importando do arquivo `darkest_gen/cli.py`
    # a função `app`

    app()


if __name__ == "__main__":
    # ^ isso é usado para que o código a seguir somente aconteça
    # caso esse arquivo seja o arquivo sendo executado
    main()
