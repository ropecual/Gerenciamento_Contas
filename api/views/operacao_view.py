from flask_restful import Resource
from ..schemas import operacao_schema
from flask import request, make_response, jsonify
from ..entidades import operacao
from ..services import operacao_service, conta_service
from api import api
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..decorators.autorizacao import user_operacao


class OperacaoList(Resource):
    @jwt_required()
    def get(self):
        # mesma coisa aqui, para retornar apenas as operações do usuario e não de outros
        usuario_logado = get_jwt_identity()
        operacoes = operacao_service.listar_operacoes(usuario_id=usuario_logado)
        os = operacao_schema.OperacaoSchema(many=True)
        return make_response(os.jsonify(operacoes), 201)

    @jwt_required()
    def post(self):
        os = operacao_schema.OperacaoSchema()
        validate = os.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            resumo = request.json["resumo"]
            custo = request.json["custo"]
            tipo = request.json["tipo"]
            conta_id = request.json["conta_id"]
            if conta_service.listar_conta_id(conta_id) is None:
                return make_response("Erro: Conta não existe", 404)
            else:
                operacao_nova = operacao.Operacao(
                    nome=nome,
                    resumo=resumo,
                    custo=custo,
                    tipo=tipo,
                    conta_id=conta_id
                )
            resultado = operacao_service.cadastrar_operacao(operacao_nova)
            return make_response(os.jsonify(resultado), 201)


class OperacaoDetail(Resource):
    @user_operacao
    def get(self, id):
        operacao_id = operacao_service.listar_operacao_id(id)
        if operacao_id is None:
            return make_response(jsonify("Operação Não Encontrada"), 404)
        os = operacao_schema.OperacaoSchema()
        return make_response(os.jsonify(operacao_id), 200)

    @user_operacao
    def put(self, id):
        operacao_bd = operacao_service.listar_operacao_id(id)
        if operacao_bd is None:
            return make_response(jsonify("Operação Não Encontrada"), 404)
        os = operacao_schema.OperacaoSchema()
        validate = os.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome_novo = request.json["nome"]
            resumo_novo = request.json["resumo"]
            custo_novo = request.json["custo"]
            tipo_novo = request.json["tipo"]
            conta_id_nova = request.json["conta_id"]
            if conta_service.listar_conta_id(conta_id_nova) is None:
                return make_response("Erro: Conta não existe", 404)
            else:
                operacao_nova = operacao.Operacao(
                    nome=nome_novo,
                    resumo=resumo_novo,
                    custo=custo_novo,
                    tipo=tipo_novo,
                    conta_id=conta_id_nova
                )
            resultado = operacao_service.atualizar_operacao(operacao_bd, operacao_nova)
            return make_response(os.jsonify(resultado), 201)

    @user_operacao
    def delete(self, id):
        operacao_deletada = operacao_service.listar_operacao_id(id)
        if operacao_deletada is None:
            return make_response(jsonify("Operação Não Encontrada"), 404)
        operacao_service.exclui_operacao(operacao_deletada)
        return make_response(jsonify(""), 204)


api.add_resource(OperacaoList, '/operacoes')
api.add_resource(OperacaoDetail, '/operacoes/<int:id>')
