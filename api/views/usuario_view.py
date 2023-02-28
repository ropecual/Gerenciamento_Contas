from flask_restful import Resource
from ..schemas import usuario_schema
from flask import request, make_response, jsonify
from ..entidades import usuario
from ..services import usuario_service
from api import api
import uuid
from api.decorators.decorator import admin_required
from flask_jwt_extended import jwt_required

class UsuarioList(Resource):
    @jwt_required()
    def get(self):
        usuarios = usuario_service.listar_usuarios()
        us = usuario_schema.UsuarioSchema(many=True)
        return make_response(us.jsonify(usuarios), 200)

    @jwt_required()
    def post(self):
        us = usuario_schema.UsuarioSchema()
        validade = us.validate(request.json)
        if validade:
            return make_response(jsonify(validade), 400)
        else:
            nome = request.json["nome"]
            email = request.json["email"]
            senha = request.json["senha"]
            is_admin = request.json["is_admin"]
            api_key = str(uuid.uuid4())
            usuario_novo = usuario.Usuario(nome=nome, email=email, senha=senha, is_admin=is_admin, api_key=api_key)
            resultado = usuario_service.cadastrar_usuario(usuario_novo)
            return make_response(us.jsonify(resultado), 201)


class UsuarioDetails(Resource):
    @jwt_required()
    def get(self, id):
        usuario_listar = usuario_service.listar_usuario_id(id)
        if usuario_listar is None:
            return make_response(jsonify("Erro: Usuario Inexistente"), 404)
        else:
            us = usuario_schema.UsuarioSchema()
            return make_response(us.jsonify(usuario_listar), 200)

    @jwt_required()
    def put(self, id):
        usuario_anterior = usuario_service.listar_usuario_id(id)
        if usuario_anterior is None:
            return make_response(jsonify("Erro: Usuario Inexistente"), 404)
        else:
            us = usuario_schema.UsuarioSchema()
            validacao = us.validate(request.json)
            if validacao:
                return make_response(jsonify(validacao), 400)
            else:
                nome_novo = request.json["nome"]
                email_novo = request.json["email"]
                senha_nova = request.json["senha"]
                is_admin = request.json["is_admin"]
                api_key = str(uuid.uuid4())
                usuario_novo = usuario.Usuario(nome=nome_novo,
                                               email=email_novo,
                                               senha=senha_nova,
                                               is_admin=is_admin,
                                               api_key=api_key)
                usuario_service.atualiza_usuario_id(usuario_anterior, usuario_novo)
                usuario_atualizado = usuario_service.listar_usuario_id(id)
                return make_response(us.jsonify(usuario_atualizado), 200)

    @admin_required
    def delete(self, id):
        usuario_deletado = usuario_service.listar_usuario_id(id)
        if usuario_deletado is None:
            return make_response(jsonify("Erro: Usuario inexistente"), 404)
        else:
            usuario_service.remove_usuario_id(usuario_deletado)
            usuarios = usuario_service.listar_usuarios()
            us = usuario_schema.UsuarioSchema(many=True)
            return make_response(us.jsonify(usuarios), 201)


api.add_resource(UsuarioList, '/usuarios')
api.add_resource(UsuarioDetails, '/usuarios/<int:id>')
