from dataclasses import replace
from datetime import datetime
import sqlite3
from unittest import result

from flask import flash

import enviaremail

DB_NAME='indetex.s3db'

# Definimos la conexion a la base de datos
def conexion():
    conn=sqlite3.connect(DB_NAME)
    return conn


def registar(nombre,apellido,email,password):
    cod_ver=str(datetime.now())
    cod_ver=cod_ver.replace("-","")
    cod_ver=cod_ver.replace(" ","")
    cod_ver=cod_ver.replace(":","")
    cod_ver=cod_ver.replace(".","")

    # Excepciones para definir si hay algun error
    try:
        db=conexion()
        cursor=db.cursor()
        sql='INSERT INTO usuarios(nombre,apellido,email,password,cod_verificacion,verificado,rol) VALUES(?,?,?,?,?,?,?)'
        cursor.execute(sql,[nombre,apellido,email,password,cod_ver,False,'user'])
        db.commit()
        # enviaremail.enviar_email(email,cod_ver)
        return True
    except:
        return False



def validar_login(email):

    try:
        db=conexion()
        cursor=db.cursor()
        sql='SELECT * FROM usuarios WHERE email=?'
        cursor.execute(sql,[email])

        resultado=cursor.fetchone()
        datos=[
                {
                    'id':resultado[0],
                    'nombre': resultado[1],
                    'apellido':resultado[2],
                    'email':resultado[3],
                    'password':resultado[4],
                    'cod_verificacion':resultado[5],
                    'verificado':resultado[6],
                    'rol':resultado[7]
                }
                ]

        return datos

    except:
        return False



def activar_cuenta(email,codigo):
    try:
        db=conexion()
        cursor=db.cursor()
        sql='UPDATE usuarios SET verificado=1 WHERE email=? AND cod_verificacion=?'
        cursor.execute(sql,[email,codigo])
        db.commit()
        sql1='SELECT * FROM usuarios WHERE email=? AND verificado=1'
        cursor.execute(sql1,[email])
        resultado=cursor.fetchone()
        if resultado != None:
            return 'SI'
        else:
            return 'NO'
    except:
            return False





def listarusuario():
        try:
            db=conexion()
            cursor=db.cursor()
            # sql='SELECT * FROM usuario WHERE email<>?'
            sql='SELECT * FROM usuarios'
            cursor.execute(sql)
            resultado=cursor.fetchall()
            usuarios=[]
            for u in resultado:
                registro={
                        'id':u[0],
                        'nombre':u[1],
                        'apellido':u[2],
                        'email':u[3],
                        'rol':u[7]
                    }
                usuarios.append(registro)        
                        
            return usuarios
        except:
            return False   

def editarUsuario(id):
    try:
        db=conexion()
        cursor=db.cursor()
        sql='SELECT * FROM usuarios WHERE id=?'
        cursor.execute(sql,[id])
        resultado=cursor.fetchone()
        if resultado != None:
            return resultado
        else:
            return 'NO'

    except:
        return False



def roles():
    try:
        db=conexion()
        cursor=db.cursor()
        # sql='SELECT * FROM usuario WHERE email<>?'
        sql='SELECT * FROM roles'
        cursor.execute(sql)
        resultado=cursor.fetchall()
        usuarios=[]
        for u in resultado:
            registro={
                    'id':u[0],
                    'tiporol':u[1],
                                    }
            usuarios.append(registro)        
                    
        return usuarios
    except:
        return False   

def actualizarrole(rol,id):
    try: 
        db=conexion()
        cursor=db.cursor()
        # UPDATE Customers SET ContactName = 'Alfred Schmidt', City= 'Frankfurt' WHERE CustomerID = 1;
        sql='UPDATE usuarios SET rol=? WHERE id=?'
        cursor.execute(sql,[rol,id])
        db.commit()
        return True
    except:
        return False


def eliminiar(id):
    try: 
        db=conexion()
        cursor=db.cursor()
        # UPDATE Customers SET ContactName = 'Alfred Schmidt', City= 'Frankfurt' WHERE CustomerID = 1;
        sql='DELETE FROM usuarios WHERE id=?;'
        cursor.execute(sql,[id])
        db.commit()
        return True
    except:
        return False
