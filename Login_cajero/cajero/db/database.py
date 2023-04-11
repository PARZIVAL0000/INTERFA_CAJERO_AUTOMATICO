#!/usr/bin/python3
#_*_ coding:utf-8 _*_ 

import os
from easymysql.mysql import mysql 

try:
    db = mysql("", "root", "D3nn7sP0nc31754090106@001001", "cajero_automatico")
except:
    print("[!] Error de conexion... Verificar el directorio: {}".format(os.getcwd()))


    