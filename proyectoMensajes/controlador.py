import sqlite3
from unittest import result


def verEnviados(correo):
    db = sqlite3.connect("mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select m.asunto, m.mensaje, m.fecha, m.hora, u.nombreusuario from usuarios u, mensajeria m where u.correo=m.id_usu_recibe and m.id_usu_envia = '"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado


def verRecibidos(correo):
    db = sqlite3.connect("mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select m.asunto, m.mensaje, m.fecha, m.hora, u.nombreusuario from usuarios u, mensajeria m where u.correo=m.id_usu_envia and m.id_usu_recibe = '"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado


def verificarUsuario(correo, password):
    db = sqlite3.connect("mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select * from usuarios where correo = '"+correo+"' and password = '"+password+"' and estado = '1'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def listaDestinatarios(usuario):
    db = sqlite3.connect("mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select * from usuarios where correo <> '"+usuario+"'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def registrarUsuario(nombre, email, passregistro,codEncript):
    try:
        db = sqlite3.connect("mensajes.s3db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        consulta = "insert into usuarios (nombreusuario,correo,password,estado,codigoactivacion) values('"+nombre+"','"+email+"','"+passregistro+"','0','"+codEncript+"')"
        cursor.execute(consulta)
        db.commit()
        return "Usuario registrado satisfactoriamente"
    except :

        return "Error!! No es posible registrar al usuario debido a que el correo y/o el nombre estan registrados"
    

def activarUsuario(codigo):
    db = sqlite3.connect("mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update usuarios set estado = '1' where codigoactivacion = '"+codigo+"'"
    cursor.execute(consulta)
    db.commit()

    consulta2 = "select * from usuarios where codigoactivacion = '"+codigo+"' and estado = '1'"
    cursor.execute(consulta2)
    resultado = cursor.fetchall()
    return resultado


def registrarMail(origen, destino, asunto, mensaje):
    db = sqlite3.connect("mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "insert into mensajeria (asunto,mensaje,fecha,hora,id_usu_envia,id_usu_recibe,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def actualizaPassw(password, correo):
    db = sqlite3.connect("mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update usuarios set password='"+password+"' where correo='"+correo+"' "
    cursor.execute(consulta)
    db.commit()
    return "1"