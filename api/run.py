# arquivo para rodar a aplicação
# Importando a aplicação api
from api import app

# Verificando se é o módulo principal, se for, ele vai rodar a aplicação
if __name__ == "__main__":
    app.run()