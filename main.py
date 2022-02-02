#!/usr/bin/python
# -*- coding: utf-8 -*-
#Comentario de Modificacion

import os
import sqlite3

DB_FILE = "data.db"

# Creación de las tablas y  schemas
crear_tabla_estudiante_sql = """ CREATE TABLE IF NOT EXISTS estudiantes (
                                        id integer PRIMARY KEY,
                                        nombre text NOT NULL,
                                        apellido text NOT NULL,
                                        cedula text NOT NULL,
                                        estado interger
                                ); """

crear_tabla_transaccion_sql = """ CREATE TABLE IF NOT EXISTS transacciones (
                                        id integer PRIMARY KEY,
                                        fechahora TEXT NOT NULL,
                                        referencia TEXT ,
                                        id_estudiante INTEGER,
                                        cantidad REAL,
                                        FOREIGN KEY(id_estudiante) REFERENCES estudiantes(id)
                                ); """


def check(db_file):
    "verificamos si la bd existe"
    if os.path.isfile(db_file):
        print ("Base de datos encontrada")
    else:
        print ("Base de datos no existe se va a crear una nueva")


def crear_coneccion(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        c.close()
    except sqlite3.Error as e:
        print(e)


def saldo(conn, cedula):
    c = conn.cursor()
    c.execute("SELECT sum(cantidad) FROM transacciones WHERE id_estudiante=(SELECT id FROM estudiantes WHERE cedula=?)",[cedula])
    out = c.fetchall()
    c.close()
    return out[0][0]

def verificar(conn):
    print("**CONSULTA DE SALDO**")
    print("Introduzca la cedula")
    cedula = input(" > ")

    s = saldo(conn, cedula)
    if s is None:
        print("Cedula no encontrada")
    else:
        print(" Saldo: " + str(s))


def cobrar(conn):
    print("**COBRO DE SERVICIOS**")
    cedula = input("Cedula: ")
    cantidad = float(input("Cantidad: "))
    
    s = saldo(conn, cedula)
    print(" Saldo antes del cobro: "+str(s))
    if float(s)-cantidad < 0:
        print( "NO SE PUEDE COBRAR. NO HAY SUFICIENTE SALDO")
        return
    c = conn.cursor()
    c.execute("INSERT INTO transacciones(fechahora,referencia,id_estudiante,cantidad) VALUES (date('now'),'COBRO',(SELECT id FROM estudiantes WHERE cedula=?),?)", [cedula,-cantidad])
    conn.commit()
    c.close()
    print(" Nuevo actual: "+str(float(s)-cantidad))


def agregar_saldo(conn):
    cedula = input("Cedula: ")
    cantidad = float(input("Cantidad: "))
    c = conn.cursor()
    c.execute("INSERT INTO transacciones(fechahora,referencia,id_estudiante,cantidad) VALUES (date('now'),'BONO',(SELECT id FROM estudiantes WHERE cedula=?),?)", [cedula,cantidad])
    conn.commit()
    c.close()


def agregar_usuario(conn):
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    cedula = input("Cedula: ")
    c = conn.cursor()
    c.execute("INSERT INTO estudiantes (nombre,apellido,cedula,estado) VALUES (?,?,?,1)", [nombre,apellido,cedula])
    conn.commit()
    c.close()


def reporte(conn):
    cedula = input("Cedula: ")
    c = conn.cursor()
    c.execute("SELECT id,id_estudiante, fechahora,referencia,cantidad FROM transacciones WHERE id_estudiante=(SELECT id FROM estudiantes WHERE cedula=?)", [cedula])
    print("id\tid_estudiante,\tfechahora,\treferencia,\tcantidad")
    for e in c.fetchall():
        print("\t".join(map(str,e)))
    c.close()


def admin(conn):
    while True:
        print("**Tareas administrativas**")
        print(" 1 - Agregar usuario")
        print(" 2 - Agregar saldo a todos")
        print(" 3 - Reporte de usuario")
        print(" 4 - Regresar a menu principal")
        i = int(input(" > "))
        if i == 1:
            agregar_usuario(conn)
        elif i == 2:
            agregar_saldo(conn)
        elif i == 3:
            reporte(conn)
        elif i == 4:
            break
        else:
            print("opción invalida\n")

def menu(c):
    while True:
        print("\n**** MENU PRINCIPAL ****")
        print("\nQue desea hacer:")
        print("1 - Verificar saldo")
        print("2 - Cobrar")
        print("3 - Tareas administrativas")
        print("4 - Salir")
        i = int(input(" > "))
        if i == 1:
            verificar(c)
        elif i == 2:
            cobrar(c)
        elif i == 3:
            admin(c)
        elif i == 4:
            break
        else:
            print("opción invalida\n")

def main():
    print("\n - Sistema de Vale UTP - Version 0 \n")

    #verificar
    check(DB_FILE)
    conn = crear_coneccion(DB_FILE)

    # create tasks table
    create_table(conn, crear_tabla_estudiante_sql)
    create_table(conn, crear_tabla_transaccion_sql)

    #menu principal
    menu(conn)


if __name__ == "__main__" :
    main()