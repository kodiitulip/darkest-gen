# esse arquivo é especial pois é executado quando o programa
# é executado como um módulo python:
# | `python -m darkest_gen`
# | `uv run -m darkest_gen`


from darkest_gen.cli import app
# ^ importando `app()` de `darkest_gen/cli.py`

if __name__ == "__main__":
    # ^ isso é usado para que o código a seguir somente aconteça
    # caso esse arquivo seja o arquivo sendo executado
    app()
