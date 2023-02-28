from ..models import conta_model, operacao_model
from api import db


def cadastrar_conta(conta):
    conta_bd = conta_model.Conta(nome=conta.nome, resumo=conta.resumo, valor=conta.valor, usuario_id=conta.usuario_id)
    db.session.add(conta_bd)
    db.session.commit()
    return conta_bd

# as alterações aqui, são para deixar a aplicação mais real, visto que o usuario não pode conseguir ver contas de
# outros utilizadores, dessa forma, enviamos o parametro id do usuario e realizamos o filtro para trazer apenas as
# contas dele

def listar_contas(usuario):
    contas = conta_model.Conta.query.filter_by(usuario_id=usuario).all()
    return contas


def listar_conta_id(id):
    conta_id = conta_model.Conta.query.filter_by(id=id).first()
    return conta_id


def atualiza_conta_id(conta_anterior, conta_nova):
    conta_anterior.nome = conta_nova.nome
    conta_anterior.resumo = conta_nova.resumo
    conta_anterior.valor = conta_nova.valor
    conta_anterior.usuario_id = conta_nova.usuario_id
    db.session.commit()


def remove_conta_id(conta):
    db.session.delete(conta)
    db.session.commit()


def altera_saldo_conta(conta_id, operacao_atualizada, tipo_funcao, operacao_custo_antigo=None):
    # tipo_funcao → 1 = Cadastro de Operação
    # tipo_funcao → 2 = Atualização de Operação
    # tipo_função → 3 = Remoção de Operação
    conta = listar_conta_id(conta_id)
    if tipo_funcao == 1:
        conta.valor += operacao_atualizada.custo
    print("\n")
    if tipo_funcao == 2:
        print("antes da operacao conta.valor: ", conta.valor)
        conta.valor -= operacao_custo_antigo
        print("conta.valor parte 1: ", conta.valor)
        conta.valor += operacao_atualizada.custo
        print("Nova conta.valor: ", conta.valor)
    if tipo_funcao == 3:
        conta.valor -= operacao_atualizada.custo

    db.session.commit()
