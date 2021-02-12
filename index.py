from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.treeview import *
from kivy.clock import Clock
from database import dbRef
import time

#Nombre, Privilegios, Hora de Loggeo (En minutos absolutos)
usuarioActual = ["", 3, 0]


class MyLayout(Widget):
    #Prototipo de creación de usuario
    #Pop-Up
    def popUpNuevoUsuario(self):
        view = ModalView(size_hint=(None, None), size=(400, 400))
        layout = BoxLayout(orientation='vertical')
        tinput1 = TextInput(text="", hint_text="Nombre")
        tinput2 = TextInput(text="", hint_text="Password", password=True)
        label1 = Label(text="Nombre de Usuario:")
        label2 = Label(text="Contraseña:")
        spinner1 = Spinner(text="Administrador", values=("Administrador", "Usuario con privilegios", "Usuario comun"))
        layout.add_widget(label1)
        layout.add_widget(tinput1)
        layout.add_widget(label2)
        layout.add_widget(tinput2)
        layout.add_widget(spinner1)
        btn1 = Button(text="Agregar nuevo usuario", on_press=lambda a:dbRef.agregarUsuario(tinput1.text, tinput2.text, spinner1.text, usuarioActual[1]))
        layout.add_widget(btn1)
        view.add_widget(layout)

        view.open()
    
    #Prototipo de loggeo de usuario
    def logginUsuario(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        condition = [False]
        privi = [3]
        dbRef.loggearUsuario(username, password, condition, privi)
        if condition[0] == True:
            print("Bienvenido")
            usuarioActual[0] = username
            usuarioActual[1] = privi[0]
            minutos = int(time.ctime()[len(time.ctime())-10]+time.ctime()[len(time.ctime())-9])
            hora = int(time.ctime()[len(time.ctime())-13]+time.ctime()[len(time.ctime())-12])*60
            horaverdadera = (minutos+hora)
            usuarioActual[2] = (horaverdadera)
            self.ids.usuario_label.text = "Usuario: "+ username+" Privilegios: "+ str(privi[0]) + " Minuto de Loggeo: " + str(horaverdadera)
            self.clockyClock()
        else:
            print("Algo salió mal")

    #Prototipo de desloggeo de usuario
    def desloggearUsuario(self):
        print("Chauchis")
        usuarioActual[0] = ""
        usuarioActual[1] = 3
        usuarioActual[2] = 0
        self.ids.usuario_label.text = "Usuario: "

    #Funcion para comparar el tiempo actual con el tiempo de loggeo; en caso de que hayan pasado 30
    #minutos y el usuario tenga privilegios de Administrador o SuperAdministrador se desencadena el
    #desloggeo
    #def tiempoModulo(self):
    #    minutos = int(time.ctime()[len(time.ctime())-10]+time.ctime()[len(time.ctime())-9])
    #    hora = int(time.ctime()[len(time.ctime())-13]+time.ctime()[len(time.ctime())-12])*60
    #    horaverdadera = (minutos+hora)
    #    if horaverdadera >= usuarioActual[2]+30 and usuarioActual[1] < 2:
    #        self.desloggearUsuario()
    #    else:
    #        print("Actual: "+str(horaverdadera) + " ... Loggeo: "+ str(usuarioActual[2]))
    
    def clockyClock(self):
        minuto = 60
        mediahora = 30*minuto
        event = Clock.schedule_once(lambda dt:self.desloggearUsuario(), mediahora)

    #Funciones de manipulacion de la tabla en Modulo 1. Primero las funciones de creación y lectura
    #de las tablas. Luego las funciones de Agregar, Modificar, Borrar en virtud de los privilegios.
    def tablaModulo1(self):
        if self.ids.spinner_modulo1.text == "Materia Prima":
            dat1a = []
            dat2a = []
            dat3a = []
            dat4a = []
            dat5a = []
            dbRef.leerMateriaPrima(dat1a, dat2a, dat3a, dat4a, dat5a)
            self.ids.tabla_modulo1.clear_widgets()
            matpriTv1 = TreeView(root_options={"text":"Id"}, size_hint=(0.3,1))
            matpriTv2 = TreeView(root_options={"text":"Insumo"})
            matpriTv3 = TreeView(root_options={"text":"Costo"}, size_hint=(0.4,1))
            matpriTv4 = TreeView(root_options={"text":"Cantidad(Kg)"}, size_hint=(0.8,1))
            matpriTv5 = TreeView(root_options={"text":"Factor/Porcion"}, size_hint=(0.5,1))
            i = 0
            while i < len(dat1a):
                matpriTv1.add_node(TreeViewLabel(text=str(dat1a[i])))
                matpriTv2.add_node(TreeViewLabel(text=dat2a[i]))
                matpriTv3.add_node(TreeViewLabel(text=dat3a[i]))
                matpriTv4.add_node(TreeViewLabel(text=dat4a[i]))
                matpriTv5.add_node(TreeViewLabel(text=dat5a[i]))
                i = i+1
            self.ids.tabla_modulo1.add_widget(matpriTv1)
            self.ids.tabla_modulo1.add_widget(matpriTv2)
            self.ids.tabla_modulo1.add_widget(matpriTv3)
            self.ids.tabla_modulo1.add_widget(matpriTv4)
            self.ids.tabla_modulo1.add_widget(matpriTv5)

        if self.ids.spinner_modulo1.text == "Productos":
            dat1b = []
            dat2b = []
            dat3b = []
            dat4b = []
            dbRef.leerProductos(dat1b, dat2b, dat3b, dat4b)
            self.ids.tabla_modulo1.clear_widgets()
            prodTv1 = TreeView(root_options={"text":"Id"}, size_hint=(0.3,1))
            prodTv2 = TreeView(root_options={"text":"Producto"}, size_hint=(0.8,1))
            prodTv3 = TreeView(root_options={"text":"Costo"}, size_hint=(0.4,1))
            prodTv4 = TreeView(root_options={"text":"Receta"})
            i = 0
            for coso in dat4b:
                j = 0
                obb = coso.split(",")
                while j < len(obb):
                    obb[j] = obb[j].split("xhx")[0]+"("+obb[j].split("xhx")[1]+")"
                    j = j+1
                h = 0
                mak = ""
                while h < len(obb):
                    mak += obb[h]
                    h = h+1
                coso = mak
                print(coso)

            while i < len(dat1b):
                prodTv1.add_node(TreeViewLabel(text=str(dat1b[i])))
                prodTv2.add_node(TreeViewLabel(text=dat2b[i]))
                prodTv3.add_node(TreeViewLabel(text=dat3b[i]))
                prodTv4.add_node(TreeViewLabel(text=dat4b[i]))
                i = i+1
            self.ids.tabla_modulo1.add_widget(prodTv1)
            self.ids.tabla_modulo1.add_widget(prodTv2)
            self.ids.tabla_modulo1.add_widget(prodTv3)
            self.ids.tabla_modulo1.add_widget(prodTv4)



class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    MyApp().run()
    