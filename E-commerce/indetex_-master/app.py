
from datetime import date, datetime
import email
from flask import Flask, render_template, url_for, request, redirect,flash,session
import controller
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.secret_key='Mi clave Secreta'+str(datetime.now)

@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/Admin')
def Admin():
    return render_template('bannerControl.html')

@app.route('/AdminPro')
def AdminPro():
    return render_template('adminProduct.html')


@app.route('/AdminUser')
def AdminUser():
    # controller.listarusuario(nombre,apellido,email,rol)

    return render_template('adminuser.html')

@app.route('/listaUser')
def listaUser():
    lista= controller.listarusuario()

    return lista




@app.route('/eliminaruser/<id>')
def eliminar(id):
    dato=controller.eliminiar(id)
    if dato=='':
        flash('No es posible hacer eliminar')
    else:
        return redirect(url_for('AdminUser'))



@app.route('/editaruser/<id>')
def editar_user(id):

    dato= controller.editarUsuario(id)
    if dato=='':
        flash('No es posible hacer esta operación')
    else:
        return render_template('gestorUsuario.html', dato=dato)



@app.route('/asignarrol/<id>', methods=['POST'])
def asignar(id):

    datos=request.form
    rol=datos['rol']
    # codigo=datos['codigo']

    actualizar= controller.actualizarrole(rol,id)
    
    return redirect(url_for('AdminUser'))
    

@app.route('/roles')
def roles():
    lista= controller.roles()
    return  lista



@app.route('/BlogDetail')
def BlogD():
    return render_template('blog-detail.html')

@app.route('/Blog')
def Blog():
    return render_template('blog.html')

@app.route('/producto')
def producto():
    return render_template('product.html')


################Registros & Login ################


@app.route('/activar')
def activar():
    return render_template('activar.html')

@app.route('/activarcuenta', methods=['POST'])
def activar_cuenta():
    datos=request.form
    email=datos['email']
    codigo=datos['codigo']
    resultado=controller.activar_cuenta(email,codigo)
    if resultado=='SI':
        flash('Cuenta Activada Satisfactoriamente')
        return redirect(url_for('login'))     
    else:
        flash('Error en Activacion')

    return redirect(url_for('activar'))  

    # return render_template('activar.html')




@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session and 'nombre' in session:
        session.pop('username')
        session.pop('nombre')
    return redirect(url_for('login'))

    

@app.route('/validarlogin',methods=['POST'])
def validar_login():
    datos=request.form
    email=datos['email']
    password=datos['password']

    if email=='' or password=='':
        flash('Datos Incompletos')
        return redirect(url_for('login'))
    else:
        resultado=controller.validar_login(email)
        if resultado==False:
            flash('Error en consulta')
            return redirect(url_for('login'))
        else:
            # print(resultado[0]['verificado'])
            if resultado[0]['verificado']==1:
                if check_password_hash(resultado[0]['password'],password):
                    session['username']=email
                    session['nombre']= resultado[0]['nombre']+" "+ resultado[0]['apellido']
                    session['rol']=resultado[0]['rol']
                    return redirect(url_for('inicio'))
                else:
                    flash('Contraseña Incorrecta')            
                    return redirect(url_for('login'))
            else:
                # flash(resultado[0]['verificado'])
                return redirect(url_for('activar'))
    



@app.route('/registro')
def registro():
    return render_template('registro.html')

# Clave secreta

@app.route('/registrar', methods=['POST'])
def registrar():
    datos=request.form
    nombre=datos['nombre']
    apellido=datos['apellido']
    email=datos['email']
    password=datos['password']
    password2=datos['password2']


    passwordHash=generate_password_hash(password)
# Crear una validacion mas acertada

    if nombre!='' and apellido!='' and email!='' and password!='' and password2 !='':
        if password!=password2:
            # return '<h2>Las contraseñas no coinciden </h2>'
            flash('Las contraseñas no coinciden')
        elif len(password)<8:
            # return '<h2>Verificar las constraseñas</h2>'
            flash('La contraseña no cumple con el minimo de caracteres')
        else:
            # return '<h3>'+nombre+apellido+email+password+password2+'</h3>'
            res=controller.registar(nombre,apellido,email,passwordHash)
            if res:
                flash('Registro Realizado Correctamente')
                return redirect(url_for('activar'))
            else: 
                flash('Error en la Base datos')
    else:
        # return '<h2>Los datos son imcompletos</h2>'
        flash('Los datos son imcompletos')

    return redirect(url_for('registro'))

    

@app.route('/contactanos')
def contac():
    return render_template('contact.html')

@app.route('/crearProducto')
def crear():
    return render_template('crearProducto.html')

@app.route('/EditarProducto')
def editar():
    return render_template('editarProducto.html')

@app.route('/Favoritos')
def favoritos():
    return render_template('favoritos.html')

@app.route('/DetallePro')
def detallePro():
    return render_template('product-detail.html')

@app.route('/ShopingCart')
def carroCom():
    return render_template('shoping-cart.html')


@app.route('/prueba')
def prueba():
        return render_template('prueba.html')






if  __name__=='__main__':
     app.run(debug=True) 