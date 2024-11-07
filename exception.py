class PizzaNotFoundError(Exception):
    def __init__(self, sabor):
        super().__init__(f"Pizza com sabor '{sabor}' não encontrada.")