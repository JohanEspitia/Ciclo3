
from datetime import date, datetime
from flask import Flask, jsonify, render_template, url_for, request, redirect,flash,session
import controlador
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.secret_key='Mi clave Secreta'+str(datetime.now)

###########Rutas para Captura de datos########

@app.route('/prueba')
def prueba():
    return True

@app.route('/consultamensajes')
def consulta_mensajes():
    usu='alexillo@gmail.com'
    resultado=controlador.listar_mensajes(usu)
    return jsonify(resultado)

@app.route('/consultamensajesind',methods=['POST'])
def consulta_mensajes_ind():
    datos=request.get_json()
    usu=datos['username']
    resultado=controlador.listar_mensajes(usu)
    return jsonify(resultado)

@app.route('/enviarmensaje', methods=['POST'])
def enviar_mensaje():
    datos=request.form
    rem=session['username']
    dest=datos['destinatario']
    asu=datos['asunto']
    mens=datos['cuerpo']
    resultado=controlador.adicionar_mensajes(rem,dest,asu,mens)
    if resultado:
        flash('Mensaje Enviar Exitosamente...')
    else:
        flash('Error Enviando Mensaje...')

    listaruser=controlador.listar_usuario(rem)
    return render_template('mensajeria.html', datauser=listaruser)    


@app.route('/activarcuenta', methods=['POST'])
def activar_cuenta():
    datos=request.form
    usu=datos['usuario']
    codver=datos['codverificacion']
    resultado=controlador.activar_cuenta(usu,codver)
    if resultado:
        flash('Cuenta Activada Satisfactoriamente')
    else:
        flash('Error en Activacion')
    return redirect(url_for('validar'))        



@app.route('/validarlogin', methods=['POST'])
def validar_login():
    datos=request.form
    usu=datos['usuario']
    passw=datos['passw']
    if usu=='' or passw=='':
        flash('Datos Incompletos')
        return redirect(url_for('login'))
    else:
        resultado=controlador.validacion_login(usu)
        if resultado==False:
            flash('Error en Consulta')
            return redirect(url_for('login'))
        else:
            print('VERIFICADO: ' + str(resultado[0]['verificado']))
            if resultado[0]['verificado']==1:
                if check_password_hash(resultado[0]['passwd'],passw):
                    session['username']=usu
                    session['nombre']=resultado[0]['nombre']+" "+resultado[0]['apellido']
                    listaruser=controlador.listar_usuario(usu)
                    print(listaruser)
                    return render_template('mensajeria.html', datauser=listaruser)
                else:
                    flash('Contrase??a Incorrecta')
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('validar'))                    




@app.route('/addregistro', methods=['POST'])
def add_registro():
    datos=request.form
    nom=datos['nombre']
    ape=datos['apellido']
    usu=datos['email']
    p1=datos['pass1']
    p2=datos['pass2']
   
    p1enc=generate_password_hash(p1)

    if nom==''and ape=='' and usu=='' and p1=='' and p2=='':
        #return '<h2>Datos Incompletos</h2>'
       flash('Datos Incompletos')
    elif p1!=p2:
        #return '<h2>Las Contrase??as no coinciden</h2>'
       flash('Las Constrase??as no Coinciden')
    elif len(p1)<8:
       #return '<h2>Verificar las constrase??as</h2>'     
       flash('Verificar Tama??o de la Contase??a')
    else:
       resultado=controlador.adicionar_registros(nom,ape,usu,p1enc)
       if resultado:
        flash('Registro Almacenado Correctamente')
       else:
        flash('Error en Base de Datos')

    return redirect(url_for('registro'))


##########Rutas de Navegacion#################
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/validar')
def validar():
    return render_template('validar.html')

@app.route('/mensajeria')
def mensajeria():
    return render_template('mensajeria.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/politicas')
def politicas():
    return render_template('politicas.html')


@app.route('/usuarios')
def menu_user():
    return render_template('usuarios.html')

@app.route('/productos')
def menu_productos():
    return render_template('productos.html')

@app.route('/carrito')
def menu_carrito():
    return render_template('carrito.html')

@app.route('/deseos')
def menu_deseos():
    return render_template('deseos.html')

@app.route('/gestion')
def menu_gestion():
    return render_template('gestionproducto.html')



if  __name__=='__main__':
     app.run(debug=True)  