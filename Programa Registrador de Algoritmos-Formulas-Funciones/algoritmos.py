from tkinter import *
from tkinter import ttk, messagebox
from sqlite3 import *
import tkinter.scrolledtext as scrolledtext
import pyautogui
#Funciones de la ventana home
def coneccion_bd(sql, parametros=()):
	global cursor, coneccion
	coneccion=connect("database/database.db")
	cursor=coneccion.cursor()
	cursor.execute(sql, parametros)
	coneccion.commit()

def guardar_datos():
	if len(entry_titulo.get())==0 or len(text_texto.get(1.0, END))==0:
		messagebox.showwarning(message="No puede dejar campos en blanco", title="Error")
	else:	
		sql="INSERT INTO algoritmos VALUES(NULL,?,?)"
		parametros=(entry_titulo.get(), text_texto.get(1.0, END))
		coneccion_bd(sql, parametros)
		messagebox.showinfo(message="Datos guardados correctamente", title="Exito")
		entry_titulo.delete(0,END)
		text_texto.delete(1.0, END)
		llenar_lista()

#Funciones Ventana lista
def llenar_lista():
	elementos_tabla= titulos.get_children()
	for elemento in elementos_tabla:
		titulos.delete(elemento)

	sql="SELECT id, titulo FROM algoritmos"		
	parametros=()
	coneccion_bd(sql, parametros)
	datos=cursor.fetchall()
	cont=0			
	for fila in datos:
		titulos.insert("", END, text=datos[cont][0], values=(datos[cont][1],))
		cont+=1
def mostrar_contenido(event):
	try:
		text_titulos.delete(1.0, END)
		titulos.selection()[0]
		id_algoritmo=titulos.item(titulos.selection())['text']
		sql = "SELECT texto FROM algoritmos WHERE id = ?"
		parametros= (id_algoritmo,)
		coneccion_bd(sql,parametros)
		datos=cursor.fetchall()	
		text_titulos.insert(1.0, datos[0][0])	
	except IndexError as e:
		messagebox.showwarning(message="No ha seleccionado ningún item", title="Error")

def copiar_texto():
	if len(text_titulos.get(1.0, 'end-1c'))==0:
		messagebox.showwarning(message="No hay nada para copiar", title="Error")
	else:	
		text_titulos.focus()
		pyautogui.hotkey('ctrl', 'a')
		pyautogui.hotkey('ctrl', 'c')

def eliminar_texto():
	try:
		titulos.selection()[0]
		id_algoritmo=titulos.item(titulos.selection())['text']
		desicion=messagebox.askyesno(message="Si elimina un item, no hay forma de recuperar la información.\n ¿Desea Continuar?")
		if desicion:
			sql = "DELETE FROM algoritmos WHERE id = ?"
			parametros= (id_algoritmo,)
			coneccion_bd(sql,parametros)
			llenar_lista()
		else:
			pass		
	except IndexError as e:
		messagebox.showwarning(message="No ha seleccionado ningún item", title="Error")

def editar_texto():
	try:
		titulos.selection()[0]
		id_algoritmo=titulos.item(titulos.selection())['text']
		desicion=messagebox.askyesno(message="Sea cuidadoso al editar la información,\nno hay forma de recuperar la información de los cambios anteriores\n ¿Desea Continuar?")
		if desicion:
			sql="UPDATE algoritmos SET texto=? WHERE id=?"
			parametros=(text_titulos.get(1.0, END), id_algoritmo)
			coneccion_bd(sql,parametros)
			messagebox.showinfo(message="Se editó correctamente", title="Error")
			llenar_lista()
		else:
			pass	
	except IndexError as e:
		messagebox.showwarning(message="No ha seleccionado ningún item", title="Error")


root=Tk()
#Imágenes
fondo = PhotoImage(file = "images/fondo.png")
fondo2 = PhotoImage(file = "images/fondo2.png")

#Ventanas
root.geometry("750x650")
root.title("Libro de Algoritmos/Formulas/Funciones")
pestañas=ttk.Notebook(root, height=650, width=750)
pestañas.pack()
home = Frame(pestañas)
lista = Frame(pestañas)
pestañas.add(home, text="Agregar Algoritmo/Formula/Funcion")
pestañas.add(lista, text="Mis Algoritmos/Formulas/Funciones")

#ventana home
fondo_home = Canvas(home, height=750, width=650)
background_label = Label(home, image=fondo)
background_label.pack(fill=BOTH, expand=YES)
fondo_home.pack()

princ_frame_inicio=Frame(home, height=80, width=400, bg="#003f6f")
princ_frame_inicio.place(x=74, y=63)
label_titulo=Label(princ_frame_inicio, text="Título", bg="#003f6f", fg="white")
label_titulo.pack()
entry_titulo=Entry(princ_frame_inicio, width=78)
entry_titulo.pack()
entry_titulo['font'] = ('Arial', '10')
entry_titulo.focus()
second_frame_inicio=Frame(home, height=120, width=400, bg="#003f6f")
second_frame_inicio.place(x=75, y=120)
label_texto=Label(second_frame_inicio, text="Algoritmo", bg="#003f6f", fg="white")
label_texto.pack()
text_texto=scrolledtext.ScrolledText(second_frame_inicio, height=20, width=80)
text_texto['font'] = ('Arial', '10')
text_texto.pack(side=LEFT)
third_frame_inicio=Frame(home, height=20, width=400)
third_frame_inicio.place(x=570, y=480)
boton_guardar=Button(third_frame_inicio, text="Guardar", bg="#003f6f", fg="white", command=guardar_datos)
boton_guardar.pack()

#Ventana lista
fondo_home = Canvas(lista, height=700, width=800)
background_label = Label(lista, image=fondo2)
background_label.pack(fill=BOTH, expand=YES)
fondo_home.pack()

princ_frame_lista=LabelFrame(lista, height=500, bg="#003f6f")
princ_frame_lista.place(x=10, y=30)
label_lista_titulos=Label(princ_frame_lista, text="Lista de Algoritmos/Formulas/Funciones", bg="#003f6f", fg="white")
label_lista_titulos.pack()
scroll_y=ttk.Scrollbar(princ_frame_lista)
scroll_y.pack(side=LEFT, fill=Y)
scroll_x=ttk.Scrollbar(princ_frame_lista, orient=HORIZONTAL)
scroll_x.pack(side=BOTTOM, fill=X)
titulos= ttk.Treeview(princ_frame_lista, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=21)
titulos["columns"]=("one")
titulos.heading('#0', text = '', anchor = CENTER)
titulos.column("#0",stretch=YES, width=0)
titulos.heading('#1', text = '', anchor = "w")
titulos.column("#1",stretch=YES, minwidth=600)
titulos.pack()
titulos.bind("<<TreeviewSelect>>", mostrar_contenido)
scroll_y.config(command=titulos.yview)
scroll_x.config(command=titulos.xview)
second_frame_lista=Frame(lista, bg="#003f6f")
second_frame_lista.place(x=241, y=30)
label_texto_lista=Label(second_frame_lista, text="Contenido del Item", bg="#003f6f", fg="white")
label_texto_lista.pack()
text_titulos=scrolledtext.ScrolledText(second_frame_lista, height=29, width=60)
text_titulos['font'] = ('Arial', '10')
text_titulos.pack()
boton_editar=Button(lista, text="Editar Texto", bg="#003f6f", fg="white", command=editar_texto)
boton_editar.place(x=580, y=530)
boton_copiar=Button(lista, text="Copiar Texto", bg="#003f6f", fg="white", command=copiar_texto)
boton_copiar.place(x=470, y=530)
boton_eliminar=Button(lista, text="Eliminar Entrada", bg="#003f6f", fg="white", command=eliminar_texto)
boton_eliminar.place(x=75, y=530)
llenar_lista()
root.mainloop()
