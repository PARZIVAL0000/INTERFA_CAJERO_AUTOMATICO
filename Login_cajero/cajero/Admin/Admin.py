#!/usr/bin/env python3
#_*_ coding:utf-8 _*_ 


"""
    La interfaz de nuestro administrador
    poseera un CRUD referente: CREAR USUARIOS (CLIENTE O ADMINISTRADOR) / LEER CUENTAS / ELIMINAR / 
    ACTUALIZAR TODAS LAS CUENTAS -> si es necesario hacerlo ....
"""

import tkinter as tk 
import threading
import time 
from tkinter import ttk 
from tkinter import messagebox
from tkinter import * 
from cajero import Login
from cajero.db import database as DB
from cajero.Admin.codigos_cedula import codigos


def admin(nombre, id):

    class Admin(Frame):

        def mostrar(self):
            #eliminamos algunos widgets de espacios anteriores.
            self.marco.destroy()
            self.Regresar.destroy()


            self.Descripcion['text'] = 'GESTIÓN DE CUENTAS BANCARIAS'
            self.ReadUsers.grid()
            self.CreateUsers.grid()
            self.DeleteUsers.grid()
            self.UpdateUsers.grid()

        def __init__(self, parent):
            super().__init__(parent)
            parent.title("ADMINISTRADOR {}".format(nombre))
            parent.configure(bg="#002643")
            # parent.configure(width=600, height=650)
            parent.geometry("600x650")


            self.headers = Label(self, text="ADMINISTRADOR : ", fg="white", bg="#005e99", font=("Arial", 12), width=15)
            self.headers.grid(row=0, column=0, ipady=15, ipadx=25)

            self.NombreAdministrador = Label(self, text="{}".format(nombre), fg="white", bg="#005e99", font=("Arial", 12), width=15, anchor="w")
            self.NombreAdministrador.grid(
                row=0, 
                column=1,
                ipady=15,
            )

            self.separador = Label(self, text="", fg="white", bg="#005e99", font=("Arial", 12), width=40)
            self.separador.grid(
                row=0, 
                column=2,
                ipady=15,
            )
            

            self.BotonLogout = Button(self, text='Cerrar Sesión', command=self.logout, anchor="e", border=0, bg="#840907", fg="white", cursor="hand1", activebackground="#5c0907", activeforeground="white", borderwidth=0)
            self.BotonLogout.grid(
                row=0, column=2,
                padx=10
            )


            self.Descripcion = Label(self, text="GESTIÓN DE CUENTAS BANCARIAS", bg="#00759f", fg="white", width=64, anchor="center")
            self.Descripcion.grid(
                row=1, 
                column=0,
                columnspan=4,
                ipady=10,
                ipadx=50,
                sticky="w"
            )

            #Crearemos una opciones en forma de boton para que el usuario los pueda eleguir .... 
            self.iconoRead = PhotoImage(file="./cajero/img/search.png")
            self.ReadUsers = Button(
            self, 
            text="VER CUENTAS", 
            border=0,
            width=175,
            height=120,
            font=("Arial", 12),
            bg="#e07500",
            fg="white",
            cursor="hand1",
            activebackground="#f19d1c",
            activeforeground="white",
            borderwidth=2,
            command=self.ejecutarReadUsers,
            image=self.iconoRead,
            compound=tk.TOP,
            padx=10
            )
            self.ReadUsers.grid(
                row=2, 
                column=0,
                pady=100,
                padx=35,
                columnspan=2
            )

            self.iconoCrear = PhotoImage(file="./cajero/img/crear.png")
            self.CreateUsers = Button(
            self, 
            text="CREAR CUENTAS", 
            border=0,
            width=175,
            height=120,
            font=("Arial", 12),
            bg="#26004c",
            fg="white",
            cursor="hand1",
            activebackground="#810053",
            activeforeground="white",
            borderwidth=2,
            command=self.ejecutarCreateUsers,
            image=self.iconoCrear,
            compound=tk.TOP
            )
            self.CreateUsers.grid(
                row=3, 
                column=0,
                pady=10,
                padx=35,
                columnspan=2
            )

            self.iconoDelete = PhotoImage(file="./cajero/img/eliminar.png")
            self.DeleteUsers = Button(
            self, 
            text="ELIMINAR CUENTAS", 
            border=0,
            width=175,
            height=120,
            font=("Arial", 12),
            bg="#680930",
            fg="white",
            cursor="hand1",
            activebackground="#b2283a",
            activeforeground="white",
            borderwidth=2,
            command=self.ejecutarDeleteUsers,
            image=self.iconoDelete,
            compound=tk.TOP
            )
            self.DeleteUsers.grid(
                row=2, 
                column=1,
                pady=100,
                padx=40,
                columnspan=2
            )

            self.iconoUpdate = PhotoImage(file="./cajero/img/update.png")
            self.UpdateUsers = Button(
            self, 
            text="ACTUALIZAR CUENTAS", 
            border=0,
            width=175,
            height=120,
            font=("Arial", 12),
            bg="#004800",
            fg="white",
            cursor="hand1",
            activebackground="#6f8800",
            activeforeground="white",
            borderwidth=2,
            command=self.ejecutarUpdateUsers,
            image=self.iconoUpdate,
            compound=tk.TOP
            )
            self.UpdateUsers.grid(
                row=3, 
                column=1,
                pady=10,
                padx=35,
                columnspan=2
            )


            self.grid(sticky="nsew")    
            self.configure(bg="#002643")


        def ejecutarDesplazamiento(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            
            #CORREGIR LOS SIGUIENTES ERRORES:
                # 1.-) QUE NO TIEMBLE AL MOMENTO DE HACER UN DESPLAZAMIENTO LENTO.
                # 2.-) QUE LA INTERFAZ PUEDA DESPLAZARSE LENTAMENTE..... NO GENERE UN GOLPETEO A LA IZQUIERDA
            try:
               
                if(args[0].x >= 0):
                    if(aumentarAncho > 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerNombre['width'] = aumentarAncho
                        self.ListadoNombres['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerNombre['width'] = aumentarAncho
                        self.ListadoNombres['width'] = aumentarAncho
                

                #este es el control para que pueda funcionar el scroll horizontal.
                if(args[0].key == 6):
                    time.sleep(1)
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass


        def ejecutarDesplazamiento2(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerCedula['width'] = aumentarAncho
                        self.ListadoCedula['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerCedula['width'] = aumentarAncho
                        self.ListadoCedula['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass


        def ejecutarDesplazamiento3(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerTelefono['width'] = aumentarAncho
                        self.ListadoTelefono['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerTelefono['width'] = aumentarAncho
                        self.ListadoTelefono['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass


        def ejecutarDesplazamiento4(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerEmail['width'] = aumentarAncho
                        self.ListadoEmail['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerEmail['width'] = aumentarAncho
                        self.ListadoEmail['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass

        def ejecutarDesplazamiento5(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerProvincia['width'] = aumentarAncho
                        self.ListadoProvincia['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerProvincia['width'] = aumentarAncho
                        self.ListadoProvincia['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass


        def ejecutarDesplazamiento6(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerPermisos['width'] = aumentarAncho
                        self.ListadoPermisos['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerPermisos['width'] = aumentarAncho
                        self.ListadoPermisos['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass

        def ejecutarDesplazamiento7(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerPresupuesto['width'] = aumentarAncho
                        self.ListadoPresupuesto['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerPresupuesto['width'] = aumentarAncho
                        self.ListadoPresupuesto['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass
    

        def ejecutarEvento(self,*args):
            #este es para el primero evento
            self.anchura = self.headerNombre['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento(self.anchura, args[0]))
            self.hiloEjecucion.start() 


        def ejecutarEvento2(self,*args):
            #este es para el primero evento
            self.anchura = self.headerCedula['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento2(self.anchura, args[0]))
            self.hiloEjecucion.start() 


        def ejecutarEvento3(self,*args):
            #este es para el primero evento
            self.anchura = self.headerTelefono['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento3(self.anchura, args[0]))
            self.hiloEjecucion.start()


        def ejecutarEvento4(self,*args):
            #este es para el primero evento
            self.anchura = self.headerEmail['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento4(self.anchura, args[0]))
            self.hiloEjecucion.start()


        def ejecutarEvento5(self,*args):
            #este es para el primero evento
            self.anchura = self.headerProvincia['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento5(self.anchura, args[0]))
            self.hiloEjecucion.start()


        def ejecutarEvento6(self,*args):
            #este es para el primero evento
            self.anchura = self.headerPermisos['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento6(self.anchura, args[0]))
            self.hiloEjecucion.start() 


        def ejecutarEvento7(self,*args):
            #este es para el primero evento
            self.anchura = self.headerPresupuesto['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento7(self.anchura, args[0]))
            self.hiloEjecucion.start() 



        """
        =======================================================
                VERIFICAR USUARIOS [1.- DE UN CRUD]
        =======================================================
        """
        def ejecutarReadUsers(self):
            self.ReadUsers.grid_remove() 
            self.CreateUsers.grid_remove() 
            self.DeleteUsers.grid_remove() 
            self.UpdateUsers.grid_remove() 

            self.Descripcion['text'] = 'VER CUENTAS DE USUARIOS'

            #configurar boton con una flecha.
            self.icono = PhotoImage(file="./cajero/img/flecha_izquierda.png")
            self.Regresar = Button(self, image=self.icono, command=self.mostrar, cursor="hand1", border=0, fg="white", bg="#00759f", activebackground="#00759f", activeforeground="white", borderwidth=0)
            self.Regresar.grid(
                row=1, 
                column=0
            )

            
            self.marco = LabelFrame(self, text="")
            self.marco.configure(width=585, height=490, bg="#928aa5")
            self.marco.grid(
                row=2,
                column=0, 
                sticky="w",
                columnspan=4,
                pady=40,
                padx=5
            )

            self.marco.grid_propagate(False)
    
            #dentro de esta seccion lo que haremos es generar un listado de todos los datos 
            #sacados de nuestra base de datos.
            self.headerNombre = Label(self.marco, text='NOMBRE', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=15)
            self.headerNombre.grid(
                row=2, 
                column=0,
                sticky="nsew",
                ipady=5
            )
            
            self.LineaDivisora = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora.bind('<Button1-Motion>' , self.ejecutarEvento)
            self.LineaDivisora.grid(
                row=2,
                column=1, 
                sticky="nsew"
            )

            self.headerCedula = Label(self.marco, text='CÉDULA', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerCedula.grid(
                row=2, 
                column=2,
                sticky="nsew",
               
            )

            self.LineaDivisora2 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora2.bind('<Button1-Motion>', self.ejecutarEvento2)
            self.LineaDivisora2.grid(
                row=2,
                column=3, 
                sticky="nsew",
            
            )


            self.headerTelefono = Label(self.marco, text='TELÉFONO', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerTelefono.grid(
                row=2, 
                column=4,
                sticky="nsew",
              
            )

            self.LineaDivisora3 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora3.bind('<Button1-Motion>', self.ejecutarEvento3)
            self.LineaDivisora3.grid(
                row=2,
                column=5, 
                sticky="nsew",
              
            )

            self.headerEmail = Label(self.marco, text='EMAIL', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerEmail.grid(
                row=2, 
                column=6,
                sticky="nsew",
               
            )

            self.LineaDivisora4 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora4.bind('<Button1-Motion>', self.ejecutarEvento4)
            self.LineaDivisora4.grid(
                row=2,
                column=7, 
                sticky="nsew",
               
            )


            self.headerProvincia = Label(self.marco, text='PROVINCIA', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerProvincia.grid(
                row=2, 
                column=8,
                sticky="nsew"
            )


            self.LineaDivisora5 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora5.bind('<Button1-Motion>', self.ejecutarEvento5)
            self.LineaDivisora5.grid(
                row=2,
                column=9, 
                sticky="nsew",
               
            )

            self.headerPermisos = Label(self.marco, text='PERMISOS', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerPermisos.grid(
                row=2, 
                column=10,
                sticky="nsew"
            )

            self.LineaDivisora6 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora6.bind('<Button1-Motion>', self.ejecutarEvento6)
            self.LineaDivisora6.grid(
                row=2,
                column=11, 
                sticky="nsew",
                
            )

            self.headerPresupuesto = Label(self.marco, text='PRESUPUESTO', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerPresupuesto.grid(
                row=2, 
                column=12,
                sticky="nsew"
            )

            #generaremos informacion...
            #=============================================================================
            #                INFORMACION OBTENIDA DE LA BASE DE DATOS
            #=============================================================================
            self.query = DB.db.select('usuarios')
           
            self.ListadoNombres = Listbox(self.marco, width=0)
            self.ListadoNombres.grid(
                row = 3, 
                column=0, 
                sticky="nsew"
            )
            
            self.ListadoCedula = Listbox(self.marco, border=0)
            self.ListadoCedula.grid(
                row = 3, 
                column=2, 
                sticky="nsew"
            )

            self.ListadoTelefono = Listbox(self.marco, border=0)
            self.ListadoTelefono.grid(
                row = 3, 
                column=4,  
                sticky="nsew"
            )

            self.ListadoEmail = Listbox(self.marco, border=0)
            self.ListadoEmail.grid(
                row = 3, 
                column=6,  
                sticky="nsew"
            )

            self.ListadoProvincia = Listbox(self.marco, border=0)
            self.ListadoProvincia.grid(
                row = 3, 
                column=8,  
                sticky="nsew"
            )

            self.ListadoPermisos = Listbox(self.marco, border=0)
            self.ListadoPermisos.grid(
                row = 3,
                column=10,  
                sticky="nsew"
            )

            self.ListadoPresupuesto = Listbox(self.marco, border=0)
            self.ListadoPresupuesto.grid(
                row = 3, 
                column=12,  
                sticky="nsew"
            )

            self.ListadoNombres.configure(height=120)
            self.ListadoCedula.configure(height=120)
            self.ListadoTelefono.configure(height=120)
            self.ListadoEmail.configure(height=120)
            self.ListadoProvincia.configure(height=120)
            self.ListadoPermisos.configure(height=120)
            self.ListadoPresupuesto.configure(height=120)
        
            for i in self.query:
                self.ListadoNombres.insert(tk.END, i['Nombre'])
                self.ListadoCedula.insert(tk.END, i['Cedula'])
                self.ListadoTelefono.insert(tk.END, i['Telefono'])
                self.ListadoEmail.insert(tk.END, i['Email'])
                self.ListadoProvincia.insert(tk.END, i['Provincia'])
                self.ListadoPermisos.insert(tk.END, i['Permisos'])
                self.ListadoPresupuesto.insert(tk.END, i['Presupuesto'])

                
        def validarEntrada(self, entrada):
            return not entrada.isdigit()


        def validarEntrada2(self, entrada):
            return entrada.isdigit()

        def verificandoEntradas(self):
            self.Nombres = self.EntradaNombreCuenta.get()
            self.Telefono = self.EntradaTelefonoCuenta.get()
            self.Cedula = self.EntradaCedulaCuenta.get()
            self.Email = self.EntradaEmailCuenta.get()
            self.TipoUsuario = self.EntradaTipoUsuarioCuenta.get()
            self.Password = self.EntradaPasswordCuenta.get()
            self.Presupuesto = self.EntradaPresupuestoCuenta.get()

            if(self.Nombres == "" or self.Telefono == "" or self.Cedula == "" or 
               self.Email == "" or self.TipoUsuario == "" or self.Password == "" or self.Presupuesto == ""):
                #highlightcolor

                self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaTelefonoCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaCedulaCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaEmailCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                # self.EntradaTipoUsuarioCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaPasswordCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaPresupuestoCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)

                messagebox.showwarning('CREAR CUENTA', 'TODOS LOS CAMPOS SON OBLIGATORIOS')
            else:
                #cuando todos los campos sean llenaos por completo... lo que haremos a continuacion es verificar por si se han 
                #introducido correctamente los datos.


                #El diccionario nos ayudara mucho para guardar la informacion en la base de datos de manera mucho mas flexible.
                self.informacion = {
                    "Nombre" : "",
                    "Telefono" : "",
                    "Cedula" : "",
                    "Email" : "",
                    "Provincia" : "",
                    "Permisos" : "",
                    "Password" : "",
                    "Presupuesto" : ""
                }


                if(len(self.Nombres.split(" ")) != 2):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta['text'] = 'DEBES INSERTAR UN NOMBRE Y UN APELLIDO'
                    self.MensajeAlerta.grid_configure(
                        row = 2, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    try:
                        self.informacion["Nombre"] = self.Nombres
                        self.EntradaNombreCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                        self.MensajeAlerta.destroy()
                    except (AttributeError, NameError):
                        pass 
                   

                if(len(self.Telefono) != 10):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta2['text'] = 'NÚMERO TELEFÓNICO INVÁLIDO'
                    self.MensajeAlerta2.grid_configure(
                        row = 4, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    try:
                        self.informacion["Telefono"] = self.Telefono
                        self.EntradaTelefonoCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                        self.MensajeAlerta2.destroy()
                    except (AttributeError, NameError):
                        pass 


                if(len(self.Cedula) != 10):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta3['text'] = 'EL NUMERO DE CÉDULA DEBE POSEER UNA LONGITUD DE 10'
                    self.MensajeAlerta3.grid_configure(
                        row = 6, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    #VAMOS A REALIZAR UNAS CUANTAS VALIDACIONES A NUESTRO CODIGO...
                    
                    impares = self.Cedula[0::2]
                    save_valores = []
                    for i in range(len(impares)):
                        numero = int(impares[i]) * 2 
                        if(numero > 9):
                            numero -= 9 
                            save_valores.append(numero)
                        else:
                            save_valores.append(numero)

                    resultado_impares = 0
                    for j in range(len(save_valores)):
                        if(resultado_impares == 0):
                            resultado_impares = save_valores[j]
                        else:
                            resultado_impares += save_valores[j]


                    #Procedimiento que haremos para los numeros pares.
                    pares =  self.Cedula[1:-2:2]

                    resultado_pares = 0
                    for i in range(len(pares)):
                        if(resultado_pares == 0):
                            resultado_pares = int(pares[i])
                        else:
                            resultado_pares += int(pares[i])


                    #Calculamos para poder verificar por el ultimo numero y ver si coincide....
                    suma_total = resultado_pares + resultado_impares

                    restante = suma_total%10 
                
                    #sacamos modulo 10.
                    if(not restante == 0):
                        #si es distinto de 0 ....
                        numero_verificador = 10 - restante

                        if(numero_verificador == int(self.Cedula[-1])):
                            self.informacion["Provincia"] = codigos.provincias[self.Cedula[0:2]]
                            self.informacion["Cedula"] = self.Cedula

                            try:
                                self.EntradaCedulaCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta3.destroy()
                            except (AttributeError, NameError):
                                pass 
                        else:
                            self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta3['text'] = 'NÚMERO DE CÉDULA INCORRECTA'
                            self.MensajeAlerta3.grid_configure(
                                row = 6, 
                                column = 1,
                                sticky="ew",
                                padx=5
                            )
                        
                    else:
                        if(restante == int(self.Cedula[-1])):
                            self.informacion["Provincia"] = codigos.provincias[self.Cedula[0:2]]
                            self.informacion["Cedula"] = self.Cedula

                            try:
                                self.EntradaCedulaCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta3.destroy()
                            except (AttributeError, NameError):
                                pass 
                        else:
                            self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta3['text'] = 'NÚMERO DE CÉDULA INCORRECTA'
                            self.MensajeAlerta3.grid_configure(
                                row = 6, 
                                column = 1,
                                sticky="ew",
                                padx=5
                            )

                    


                if(self.Email.find('@') == -1):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta4['text'] = 'DEBES INSERTAR UN EMAIL VÁLIDO'
                    self.MensajeAlerta4.grid_configure(
                        row = 8, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    #Realicemos una ultima validacion con respecto a....
                    try:
                        self.EntradaEmailCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                        self.MensajeAlerta4.destroy()
                    except (AttributeError, NameError):
                        pass 

                #TIPOS DE USUARIO
                if(self.TipoUsuario == ""):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta5['text'] = 'DEBES INSERTAR UN TIPO DE USUARIO'
                    self.MensajeAlerta5.grid_configure(
                        row = 2, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    try:
                        self.EntradaNombreCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                        self.MensajeAlerta5.destroy()
                    except (AttributeError, NameError):
                        pass 


                if(len(self.Password) != 5):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta6['text'] = 'TU CONTRASEÑA DEBE TENER UNA LONGITUD DE 5'
                    self.MensajeAlerta6.grid_configure(
                        row = 12, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    try:
                        self.EntradaPasswordCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                        self.MensajeAlerta6.destroy()
                    except (AttributeError, NameError):
                        pass 

                
                if(self.Presupuesto != ""):
                    self.EntradaPresupuestoCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)


        def ejecutarCreateUsers(self):
            self.ReadUsers.grid_remove() 
            self.CreateUsers.grid_remove() 
            self.DeleteUsers.grid_remove() 
            self.UpdateUsers.grid_remove() 

            self.Descripcion['text'] = 'CREAR CUENTA DE USUARIO'

            #configurar boton con una flecha.
            self.icono = PhotoImage(file="./cajero/img/flecha_izquierda.png")
            self.Regresar = Button(self, image=self.icono, command=self.mostrar, cursor="hand1", border=0, fg="white", bg="#00759f", activebackground="#00759f", activeforeground="white", )
            self.Regresar.grid(
                row=1, 
                column=0
            )

            #lo que vamos hacer desntro de esta parte es generar un formulario con datos para que se comience a generar el perfil de
            #nuestro usuario....
            self.marco = LabelFrame(self, text='', width=590, height=515, border=0, bg="#125160")
            self.marco.grid(
                row=2, 
                column=0, 
                columnspan=3,
                pady=30,
                padx=5,
                sticky="w"
            )
            self.marco.grid_propagate(False)

            self.headerFormulario = Label(self.marco, text='INSERTA LOS DATOS A CONTINUACIÓN', bg="#ef8200", fg="white", font=("Arial", 11))
            self.headerFormulario.grid(
                row=0, 
                column=0, 
                columnspan=3,
                sticky="w", 
                ipadx=155
            )

            """
            Desactivar para otra ocasion el siguiente codigo comentado para posibles soluciones a otras cosas.
            """
            #==========================================================================================================
            self.NombreCuenta = Label(self.marco, text='INSERTA NOMBRES: ', fg="white", bg="#125160", justify="left")
            self.NombreCuenta.grid(
                row=1, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )

            self.EntradaNombreCuenta = Entry(
                self.marco, 
                width=40, 
                validate="key", 
                validatecommand=(self.register(self.validarEntrada),"%S"), 
            )
            self.EntradaNombreCuenta.grid(
                row=1, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )

            self.MensajeAlerta = Label(self.marco, text="DEBES INTRODUCIR DOS NOMBRES", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 2, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )

            # =====================================================================================================

            self.TelefonoCuenta = Label(self.marco, text='INSERTA TELÉFONO: ', fg="white", bg="#125160")
            self.TelefonoCuenta.grid(
                row=3, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaTelefonoCuenta = Entry(
                self.marco, 
                width=40,
                validate="key", 
                validatecommand=(self.register(self.validarEntrada2),"%S")
            )
            self.EntradaTelefonoCuenta.grid(
                row=3, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )

            self.MensajeAlerta2 = Label(self.marco, text="DEBES INTRODUCIR UN NÚMERO TELEFÓNICO", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 4, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )


            self.CedulaCuenta = Label(self.marco, text='INSERTA CÉDULA: ', fg="white", bg="#125160")
            self.CedulaCuenta.grid(
                row=5, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaCedulaCuenta = Entry(
                self.marco, 
                width=40,
                validate="key", 
                validatecommand=(self.register(self.validarEntrada2),"%S")
            )
            self.EntradaCedulaCuenta.grid(
                row=5, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3,
            )

            self.MensajeAlerta3 = Label(self.marco, text="DEBES INTRODUCIR UN NÚMERO DE CÉDULA", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 6, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )


            self.EmailCuenta = Label(self.marco, text='INSERTA EMAIL: ', fg="white", bg="#125160")
            self.EmailCuenta.grid(
                row=7, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaEmailCuenta = Entry(self.marco, width=40)
            self.EntradaEmailCuenta.grid(
                row=7, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )

            self.MensajeAlerta4 = Label(self.marco, text="DEBES INTRODUCIR UN EMAIL", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 8, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )


            self.TipoUsuarioCuenta = Label(self.marco, text='INSERTA TIPO DE USUARIO: ', fg="white", bg="#125160")
            self.TipoUsuarioCuenta.grid(
                row=9, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaTipoUsuarioCuenta = ttk.Combobox(self.marco, width=40, values=['CLIENTE', 'ADMINISTRADOR'], state='readonly', background="white")
            self.EntradaTipoUsuarioCuenta.grid(
                row=9, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )


            self.MensajeAlerta5 = Label(self.marco, text="INSERTA EL TIPO DE USUARIO", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 10, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )


            self.PasswordCuenta = Label(self.marco, text='INSERTA CONTRASEÑA: ', fg="white", bg="#125160")
            self.PasswordCuenta.grid(
                row=11, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaPasswordCuenta = Entry(self.marco, width=40, show="*")
            self.EntradaPasswordCuenta.grid(
                row=11, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )

            self.MensajeAlerta6 = Label(self.marco, text="CREA UNA CONTRASEÑA PARA LA CUENTA", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 12, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )

            self.PresupuestoCuenta = Label(self.marco, text='INSERTA PRESUPUESTO CUENTA: ', fg="white", bg="#125160")
            self.PresupuestoCuenta.grid(
                row=13, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaPresupuestoCuenta = Entry(
                self.marco, 
                width=40,
                validate="key", 
                validatecommand=(self.register(self.validarEntrada2),"%S")
            )
            self.EntradaPresupuestoCuenta.grid(
                row=13, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3,
            )
 
            self.MensajeAlerta7 = Label(self.marco, text="DIGITA UN PRESUPUESTO", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 14, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )

            self.BotonCuenta = Button(
                self.marco, 
                text='GENERAR CUENTA', 
                font=("Arial", 9), width=50, 
                bg="#aa054a", 
                fg="white", 
                border=0, 
                cursor="hand1", 
                activebackground="#fe0041", 
                activeforeground="white",
                command=self.verificandoEntradas)
            self.BotonCuenta.grid(
                row=15, 
                column=0, 
                columnspan=2,
                pady=10
            )
            #A CONTINUACION SERA LA CREACION DE UN FORMULARIO... CADA UNO DE LOS CAMPOS SERA VALIDADO A CORDE A LO QUE SE PIDA.



        def ejecutarDeleteUsers(self):
            self.ReadUsers.grid_remove() 
            self.CreateUsers.grid_remove() 
            self.DeleteUsers.grid_remove() 
            self.UpdateUsers.grid_remove() 

            self.Descripcion['text'] = 'ELIMINAR CUENTA DE USUARIO'

            #configurar boton con una flecha.
            self.icono = PhotoImage(file="./cajero/img/flecha_izquierda.png")
            self.Regresar = Button(self, image=self.icono, command=self.mostrar, cursor="hand1", border=0, fg="white", bg="#00759f", activebackground="#00759f", activeforeground="white", )
            self.Regresar.grid(
                row=1, 
                column=0
            )

        def ejecutarUpdateUsers(self):
            self.ReadUsers.grid_remove() 
            self.CreateUsers.grid_remove() 
            self.DeleteUsers.grid_remove() 
            self.UpdateUsers.grid_remove() 

            self.Descripcion['text'] = 'ACTUALIZAR CUENTA DE USUARIO'

            #configurar boton con una flecha.
            self.icono = PhotoImage(file="./cajero/img/flecha_izquierda.png")
            self.Regresar = Button(self, image=self.icono, command=self.mostrar, cursor="hand1", border=0, fg="white", bg="#00759f", activebackground="#00759f", activeforeground="white", )
            self.Regresar.grid(
                row=1, 
                column=0
            )


        def logout(self):
            root.destroy()
            Login.login()
            return 


    root = Tk()
    start = Admin(root)
    root.resizable(0,0)
    root.mainloop()
