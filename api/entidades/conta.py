class Conta():
    def __init__(self, nome, resumo, valor, usuario_id):
        self.__nome = nome
        self.__resumo = resumo
        self.__valor = valor
        self.__usuario_id = usuario_id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def resumo(self):
        return self.__resumo

    @resumo.setter
    def resumo(self, resumo):
        self.__resumo = resumo

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        self.__valor = valor

    @property
    def usuario_id(self):
        return self.__usuario_id

    @usuario_id.setter
    def usuario_id(self, usuario_id):
        self.__usuario_id = usuario_id

