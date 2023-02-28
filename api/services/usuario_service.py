from ..models import usuario_model
from api import db


def cadastrar_usuario(usuario):
    usuario_db = usuario_model.Usuario(nome=usuario.nome,
                                       email=usuario.email,
                                       senha=usuario.senha,
                                       is_admin=usuario.is_admin,
                                       api_key=usuario.api_key
                                       )

    usuario_db.cripto_senha()
    db.session.add(usuario_db)
    db.session.commit()
    return usuario_db


def listar_usuarios():
    usuarios = usuario_model.Usuario.query.all()
    return usuarios


def listar_usuario_id(id):
    usuario_id = usuario_model.Usuario.query.filter_by(id=id).first()
    return usuario_id


def atualiza_usuario_id(usuario_anterior, usuario_novo):
    usuario_anterior.nome = usuario_novo.nome
    usuario_anterior.email = usuario_novo.email
    usuario_anterior.senha = usuario_novo.senha
    usuario_anterior.is_admin = usuario_novo.is_admin
    usuario_anterior.api_key = usuario_novo.api_key
    usuario_anterior.cripto_senha()
    db.session.commit()


def remove_usuario_id(usuario):
    db.session.delete(usuario)
    db.session.commit()


def listar_usuario_email(email):
    usuario_email = usuario_model.Usuario.query.filter_by(email=email).first()
    return usuario_email


def listar_usuario_api_key(api_key):
    return usuario_model.Usuario.query.filter_by(api_key=api_key).first()

