from datetime import date, datetime
from flask import Flask, render_template, url_for, request, redirect,flash

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/AdminPro')
def Adminpro():
    return render_template('adminProduct.html')

@app.route('/BlogDetail')
def BlogD():
    return render_template('blog-detail.html')

@app.route('/Blog')
def Blog():
    return render_template('blog.html')

@app.route('/producto')
def producto():
    return render_template('product.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contactanos')
def contac():
    return render_template('contact.html')

@app.route('/CrearProducto')
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

if  __name__=='__main__':
     app.run(debug=True) 