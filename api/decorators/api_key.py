from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import make_response, jsonify, request
from api.services.usuario_service import listar_usuario_api_key


def require_apikey(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        api_key = request.args.get('api_key')
        # Se eu tiver uma api_key e se ela estiver no banco de dados, cuidado com as aspas onde não existe
        if api_key and listar_usuario_api_key(api_key):
            return fn(*args, **kwargs)
        else:
            return make_response(jsonify(message='Não é permitido, api_tokens válidos'), 401)
    return wrapper
