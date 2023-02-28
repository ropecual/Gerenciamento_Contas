from api import db
from ..models import operacao_model, conta_model
from ..services import conta_service


def listar_operacoes(usuario_id):
    # aqui fazemos um join na tabela usuario, com o SQLAlchemy, para conseguir recuperar o id do usuario, através
    # da tabela conta
    operacoes = operacao_model.Operacao.query.join(conta_model.Conta).filter_by(usuario_id=usuario_id).all()
    return operacoes


def listar_operacao_id(id):
    operacao = operacao_model.Operacao.query.filter_by(id=id).first()
    return operacao


def cadastrar_operacao(operacao):
    # esse tratamento aqui eu inseri para melhorar o algoritmo de entrada e saida
    if operacao.tipo == "saida":
        if operacao.custo > 0:
            operacao.custo *= -1
    operacao_bd = operacao_model.Operacao(
        nome=operacao.nome,
        resumo=operacao.resumo,
        custo=operacao.custo,
        tipo=operacao.tipo,
        conta_id=operacao.conta_id
    )
    db.session.add(operacao_bd)
    db.session.commit()
    conta_service.altera_saldo_conta(operacao.conta_id, operacao, 1)

    return operacao_bd


def atualizar_operacao(operacao, operacao_nova):
    if operacao_nova.tipo == "saida":
        if operacao_nova.custo > 0:
            operacao_nova.custo *= -1
    print("operacao.custo valor antigo def atualizar_operacao: ", operacao.custo)
    print("operacao_nova.custo def atualizar_operacao: ", operacao_nova.custo)

    operacao_custo_antigo = operacao.custo
    operacao.nome = operacao_nova.nome
    operacao.resumo = operacao_nova.resumo
    operacao.custo = operacao_nova.custo
    operacao.tipo = operacao_nova.tipo
    operacao.conta_id = operacao_nova.conta_id
    db.session.commit()
    conta_service.altera_saldo_conta(operacao_nova.conta_id, operacao_nova, 2, operacao_custo_antigo)
    return operacao


def exclui_operacao(operacao):
    db.session.delete(operacao)
    db.session.commit()
    conta_service.altera_saldo_conta(operacao.conta_id, operacao, 3)


def listar_operacao_conta_id(id):
    operacao_conta_id = operacao_model.Operacao.query.filter_by(conta_id=id)
    return operacao_conta_id
