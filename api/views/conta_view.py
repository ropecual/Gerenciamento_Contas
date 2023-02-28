from flask_restful import Resource
from ..schemas import conta_schema
from flask import request, make_response, jsonify
from ..entidades import conta
from ..services import conta_service, operacao_service
from api import api
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..decorators.autorizacao import user_conta


# Muitas modificações no código devem-se as aulas 47 em diante, qndo criamos um decorator e eliminamos muito codigo
# de validação que não é mais util


class ContaList(Resource):
    @jwt_required()
    def get(self):
        usuario_logado = get_jwt_identity()
        contas = conta_service.listar_contas(usuario=usuario_logado)
        cs = conta_schema.ContaSchema(many=True)
        return make_response(cs.jsonify(contas), 200)

    @jwt_required()
    def post(self):
        cs = conta_schema.ContaSchema()
        validade = cs.validate(request.json)
        if validade:
            return make_response(jsonify(validade), 400)
        else:
            nome = request.json["nome"]
            resumo = request.json["resumo"]
            valor = request.json["valor"]
            usuario_id = get_jwt_identity()
            conta_nova = conta.Conta(nome=nome, resumo=resumo, valor=valor, usuario_id=usuario_id)
            resultado = conta_service.cadastrar_conta(conta_nova)
            return make_response(cs.jsonify(resultado), 201)


# Muitas modificações no código devem-se as aulas 47 em diante, qndo criamos um decorator e eliminamos muito codigo
# de validação que não é mais util
class ContasDetails(Resource):
    @user_conta
    def get(self, id):
        conta_listar = conta_service.listar_conta_id(id)
        cs = conta_schema.ContaSchema()
        return make_response(cs.jsonify(conta_listar), 200)

    @user_conta
    def put(self, id):
        conta_anterior = conta_service.listar_conta_id(id)
        cs = conta_schema.ContaSchema()
        validacao = cs.validate(request.json)
        if validacao:
            return make_response(jsonify(validacao), 400)
        else:
            nome_novo = request.json["nome"]
            resumo_novo = request.json["resumo"]
            valor_novo = request.json["valor"]
            usuario_id_novo = get_jwt_identity()

            conta_nova = conta.Conta(nome=nome_novo,
                                     resumo=resumo_novo,
                                     valor=valor_novo,
                                     usuario_id=usuario_id_novo
                                     )
            conta_service.atualiza_conta_id(conta_anterior, conta_nova)
            conta_atualizada = conta_service.listar_conta_id(id)
            return make_response(cs.jsonify(conta_atualizada), 200)

    @user_conta
    def delete(self, id):
        conta_deletada = conta_service.listar_conta_id(id)
        # Esse for aqui serve para percorrer cada operacao existente a partir do conta_id na tabela operacao
        # e apagar um por um, para depois dai apagar a conta, facilita a limpeza, ja q n há uma conta vinculada
        # não tem o pq existir operações
        operacoes = operacao_service.listar_operacao_conta_id(id)
        for operacao in operacoes:
            operacao_service.exclui_operacao(operacao)
        conta_service.remove_conta_id(conta_deletada)
        contas = conta_service.listar_contas()
        cs = conta_schema.ContaSchema(many=True)
        return make_response(cs.jsonify(contas), 201)


api.add_resource(ContaList, '/contas')
api.add_resource(ContasDetails, '/contas/<int:id>')
