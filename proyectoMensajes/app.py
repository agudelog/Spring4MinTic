from dataclasses import dataclass
from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

email_origen = ""

@app.route("/")
def inicio():
    return render_template("login.html")


@app.route("/verificarUsuario",methods=["GET","POST"])
def verificarUsuario():

    if request.method=="POST":
        usuario = request.form["txtusuario"]
        usuario = usuario.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")
        
        password = request.form["txtpass"]
        password = password.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")
        
        passhash = password.encode()
        passhash = hashlib.sha384(passhash).hexdigest()
        
        respuesta = controlador.verificarUsuario(usuario, passhash)

        global email_origen

        if len(respuesta)==0:
            email_origen =""
            mensaje = "Error de Autenticacion, verifique su usuario y contraseña"
            return render_template("informacion.html", infoMensaje = mensaje)
        else:
            #print("correo Electronico = " + correo)
            #print("Contraseña = " + password)
            #print("Contraseña codificada = " + passhash)
            email_origen =usuario
            respuesta2 = controlador.listaDestinatarios(usuario)
            return render_template("principal.html", infoMensaje = respuesta2)

@app.route("/registrarUsuario",methods=["GET","POST"])
def registrarUsuario():

    if request.method=="POST":
        nombre = request.form["txtnombre"]
        nombre = nombre.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")

        email = request.form["txtusuarioregistro"]
        email = email.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")

        password = request.form["txtpassregistro"]
        password = password.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")
        
        passregistro = password.encode()
        passregistro = hashlib.sha384(passregistro).hexdigest()

        codigo = datetime.now()
        codEncript = str(codigo)
        codEncript = codEncript.replace("-","")
        codEncript = codEncript.replace(" ","")
        codEncript = codEncript.replace(":","")
        codEncript = codEncript.replace(".","")
        #print(codigo)
        #print(codEncript)

        mensaje = "Hola "+nombre+", su codigo de activacion es :\n\n"+codEncript+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"

        envioemail.enviar(email,mensaje, "Codigo de Activacion")
        
        respuesta = controlador.registrarUsuario(nombre, email, passregistro, codEncript)

        #mensaje = "El Usuario "+nombre+", se ha registrado en el sistema"
        return render_template("informacion.html", infoMensaje = respuesta)


@app.route("/enviarMAIL",methods=["GET","POST"])
def enviarMAIL():

    if request.method=="POST":
        emailDestino = request.form["emailDestino"]
        emailDestino = emailDestino.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")

        asunto = request.form["asunto"]
        asunto = asunto.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")

        mensaje = request.form["mensaje"]
        mensaje = mensaje.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")

        controlador.registrarMail(email_origen,emailDestino,asunto,mensaje)
        
        mensaje2 = "Recibiste un mensaje Nuevo, verifica en la plataforma el mensaje, en la pestaña Historial. \n\n Muchas Gracias"
        envioemail.enviar(emailDestino,mensaje2,"Nuevo Mensaje Enviado")
        return "Email enviado satisfactoriamente"


@app.route("/activarUsuario",methods=["GET","POST"])
def activarUsuario():

    if request.method=="POST":
        codigo = request.form["txtcodigo"]
        codigo = codigo.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")

        respuesta = controlador.activarUsuario(codigo)

        if len(respuesta)==0:
            mensaje = "El codigo de activacion es erroneo, por favor validar nuevamente"
        else:
            mensaje = "El usuario se ha activado correctamente"

        return render_template("informacion.html", infoMensaje = mensaje)


@app.route("/historialEnviados",methods=["GET","POST"])
def historialEnviados():

    if request.method=="POST":
       
       resultado = controlador.verEnviados(email_origen)

    return render_template("respuesta.html", infoMensaje = resultado)


@app.route("/historialRecibidos",methods=["GET","POST"])
def historialRecibidos():

    if request.method=="POST":
       
       resultado = controlador.verRecibidos(email_origen)

    return render_template("respuesta2.html", infoMensaje = resultado)


@app.route("/actualizaPassword",methods=["GET","POST"])
def actualizaPassword():

    if request.method=="POST":
        passW = request.form["passW"]
        passW = passW.replace("SELECT","").replace("INSERT","").replace("UPDATE","").replace("DELETE","").replace("WHERE","")
        
        passhash = passW.encode()
        passhash = hashlib.sha384(passhash).hexdigest()

        controlador.actualizaPassw(passhash, email_origen)

        return "Actualizacion de Password Satisfactoria"