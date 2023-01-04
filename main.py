from tkinter import *
from tkinter.ttk import *
import pandas as pd
import sqlite3
from PIL import Image, ImageTk
# Tkinter creación
root = Tk()
root.call("source", "azure.tcl")
root.call("set_theme", "light")
# Creación del título
root.title("Fisio Sistema")
ico = Image.open('icon.jpg')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
menubar = Menu(root)
file = Menu(menubar, tearoff=0)
# Funcionalidades del sistema
# 1. Creación del paciente


def ventanaCreacionPacienteFuncion():
    ventanaCreacionPaciente = Toplevel(root)
    ventanaCreacionPaciente.title("Creación paciente")
    ventanaCreacionPaciente.wm_iconphoto(False, photo)
    # Nombre Cedula Telefono
    # Sesiones requeridas / Sesiones llevadas
    Label(ventanaCreacionPaciente, text="Nombre completo").grid(row=0)
    Label(ventanaCreacionPaciente, text="Documento").grid(row=1)
    Label(ventanaCreacionPaciente, text="Teléfono").grid(row=2)
    Label(ventanaCreacionPaciente, text="Sesiones requeridas").grid(row=3)
    Label(ventanaCreacionPaciente, text="Patología").grid(row=4)
    nombreCompleto = Entry(ventanaCreacionPaciente)
    nombreCompleto.grid(row=0, column=1)
    documento = Entry(ventanaCreacionPaciente)
    documento.grid(row=1, column=1)
    telefono = Entry(ventanaCreacionPaciente)
    telefono.grid(row=2, column=1)
    sesionesR = Entry(ventanaCreacionPaciente)
    sesionesR.grid(row=3, column=1)
    patologia = Entry(ventanaCreacionPaciente)
    patologia.grid(row=4, column=1)

    def insertarDatos():
        import string
        from tkinter import messagebox
        nombre = nombreCompleto.get()
        doc = documento.get()
        tel = telefono.get()
        sesR = sesionesR.get()
        pat = patologia.get()
        # Se insertan los datos al db
        if nombre != "" and doc != "" and tel != "" and sesR != "" and pat != "":
            # En caso de que el tipo de datos sea incorrecto
            try:
                doc = int(doc)
                tel = int(tel)
                sesR = int(sesR)
                pat = string.capwords(pat)
                conn = sqlite3.connect('doctora.db')
                cursor = conn.cursor()
                insert = (nombre, doc, tel, sesR, 0, pat)
                cursor.execute(
                    'insert into pacientes values (?,?,?,?,?,?)', insert)
                cursor.close()
                conn.commit()
                conn.close()
                messagebox.showinfo(message="Se creó el siguiente paciente:\nNombre: {}\nDocumento: {}\nTeléfono: {}\nSesiones requeridas: {}\nPatología: {}".format(
                    nombre, doc, tel, sesR, pat), title="Creación de paciente")
            except:
                messagebox.showinfo(
                    message="Error, tipo de dato incorrecto", title="Error")
        else:
            # Alerta avisando el error
            messagebox.showinfo(message="Error, faltan datos", title="Error")

    Button(ventanaCreacionPaciente, text="Salir", command=ventanaCreacionPaciente.destroy).grid(
        row=5, column=0, sticky=W, pady=4)
    Button(ventanaCreacionPaciente, text="Crear", command=insertarDatos).grid(
        row=5, column=1, sticky=W, pady=4)


file.add_command(label="Crear paciente",
                 command=ventanaCreacionPacienteFuncion)

# 2. Eliminar paciente


def ventanaEliminacionPacienteFuncion():
    from tkinter import messagebox
    ventanaEliminacionPaciente = Toplevel(root)
    ventanaEliminacionPaciente.title("Eliminación paciente")
    ventanaEliminacionPaciente.wm_iconphoto(False, photo)
    Label(ventanaEliminacionPaciente, text="Documento").grid(row=0)
    documento = Entry(ventanaEliminacionPaciente)
    documento.grid(row=0, column=1)

    def eliminarDatos():
        # En caso de que el tipo de dato sea incorrecto
        try:
            doc = documento.get()
            doc = int(doc)
            conn = sqlite3.connect('doctora.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT count(*) FROM pacientes WHERE cedula = ?", (doc,))
            # Ver si existe siquiera ese documento
            db_result = cursor.fetchone()[0]
            # Si no existe
            if db_result == 0:
                messagebox.showinfo(
                    message="No existe paciente con esa cedula", title="Error")
            else:
                # En caso de que exista
                cursor.execute(
                    "SELECT * FROM pacientes WHERE cedula = ?", (doc,))
                nombre = cursor.fetchone()[0]
                cursor.execute(
                    "DELETE FROM pacientes WHERE cedula = ?", (doc,))
                cursor.execute("DELETE FROM fechas WHERE cedula = ?", (doc,))
                cursor.close()
                conn.commit()
                conn.close()
                messagebox.showinfo(
                    message="Vas a eliminar al paciente "+nombre, title="Eliminar")
        except:
            messagebox.showinfo(
                message="Error, tipo de dato incorrecto", title="Error")
    Button(ventanaEliminacionPaciente, text="Salir",
           command=ventanaEliminacionPaciente.destroy).grid(row=1, column=0, sticky=W, pady=4)
    Button(ventanaEliminacionPaciente, text="Eliminar",
           command=eliminarDatos).grid(row=1, column=1, sticky=W, pady=4)


file.add_command(label="Eliminar paciente",
                 command=ventanaEliminacionPacienteFuncion)

# 3. Editar pacientes


def ventanaEditarPacienteFuncion():
    from tkinter import messagebox
    import string
    ventanaEditarPaciente = Toplevel(root)
    ventanaEditarPaciente.title("Edición paciente")
    ventanaEditarPaciente.wm_iconphoto(False, photo)
    Label(ventanaEditarPaciente, text="Documento").grid(row=0)
    documento = Entry(ventanaEditarPaciente)
    documento.grid(row=0, column=1)
    Label(ventanaEditarPaciente, text="Selecciona el campo a editar").grid(row=1)
    # Campo desplegable
    value_inside = StringVar(ventanaEditarPaciente)
    value_inside.set("Elige una opción")
    options_list = ["Elige una opción", "nombre", "cedula",
                    "telefono", "sesiones requeridas", "sesiones llevadas", "patologia"]
    opciones = OptionMenu(ventanaEditarPaciente, value_inside, *options_list)
    opciones.grid(row=1, column=1)
    Label(ventanaEditarPaciente, text="Valor").grid(row=2)
    valor = Entry(ventanaEditarPaciente)
    valor.grid(row=2, column=1)

    def editarDatos():
        try:
            doc = documento.get()
            doc = int(doc)
            conn = sqlite3.connect('doctora.db')
            cursor = conn.cursor()
            valorCambiar = value_inside.get()
            # Esto se hace para cambiar el atributo, los atributos se llaman sesionesR o sesionesL
            if value_inside.get() == "sesiones requeridas":
                valorCambiar = "sesionesR"
            elif value_inside.get() == "sesiones llevadas":
                valorCambiar = "sesionesL"

            # Revisar si existe o no
            cursor.execute(
                "SELECT count(*) FROM pacientes WHERE cedula = ?", (doc,))
            # Ver si existe siquiera ese documento
            db_result = cursor.fetchone()[0]
            # Si no existe
            if db_result == 0:
                messagebox.showinfo(
                    message="No existe paciente con esa cedula", title="Error")
            else:
                valorIntroducir = valor.get()
                if valorCambiar == "nombre":
                    valorIntroducir = "'"+valorIntroducir+"'"
                elif valorCambiar == "patologia":
                    valorIntroducir = "'"+string.capwords(valorIntroducir)+"'"
                else:
                    valorIntroducir = int(valorIntroducir)
                query = "UPDATE pacientes SET {} = {} WHERE cedula = {}".format(
                    valorCambiar, valorIntroducir, doc)
                cursor.execute(query)
                conn.commit()
                # En caso de que exista
                cursor.execute(
                    "SELECT * FROM pacientes WHERE cedula = ?", (doc,))
                listaQuery = cursor.fetchone()
                nombre = listaQuery[0]
                telefono = listaQuery[2]
                sesionesR = listaQuery[3]
                sesionesL = listaQuery[4]
                cursor.close()
                conn.close()
                messagebox.showinfo(message="Paciente actualizado con estas características:\nNombre: {}\nDocumento: {}\nTeléfono: {}\nSesiones realizadas: {}\nSesiones llevadas: {}".format(
                    nombre, doc, telefono, sesionesR, sesionesL), title="Actualizar")
        except:
            messagebox.showinfo(
                message="Error, tipo de dato incorrecto", title="Error")
    Button(ventanaEditarPaciente, text="Salir", command=ventanaEditarPaciente.destroy).grid(
        row=3, column=0, sticky=W, pady=4)
    Button(ventanaEditarPaciente, text="Editar", command=editarDatos).grid(
        row=3, column=1, sticky=W, pady=4)


file.add_command(label="Editar paciente", command=ventanaEditarPacienteFuncion)


def ventanaConsultarPacienteFuncion():
    from tkinter import messagebox
    ventanaConsultarPaciente = Toplevel(root)
    ventanaConsultarPaciente.title("Edición paciente")
    ventanaConsultarPaciente.wm_iconphoto(False, photo)
    Label(ventanaConsultarPaciente,
          text="Selecciona el campo a editar").grid(row=0)
    # Campo desplegable
    value_inside = StringVar(ventanaConsultarPaciente)
    value_inside.set("Elige una opción")
    options_list = ["Elige una opción", "nombre", "cedula", "telefono"]
    opciones = OptionMenu(ventanaConsultarPaciente,
                          value_inside, *options_list)
    opciones.grid(row=0, column=1)
    Label(ventanaConsultarPaciente, text="Valor").grid(row=1)
    valor = Entry(ventanaConsultarPaciente)
    valor.grid(row=1, column=1)

    def consultarDatos():
        try:
            conn = sqlite3.connect('doctora.db')
            cursor = conn.cursor()
            valorSeleccionado = value_inside.get()
            valorIntroducir = valor.get()
            if valorSeleccionado == "cedula" or valorSeleccionado == "telefono":
                valorIntroducir = int(valorIntroducir)
            else:
                valorIntroducir = "'"+valorIntroducir+"'"
            # Revisar si existe o no
            cursor.execute(
                "SELECT count(*) FROM pacientes WHERE {} = {}".format(valorSeleccionado, valorIntroducir))
            # Ver si existe siquiera ese documento
            db_result = cursor.fetchone()[0]
            # Si no existe
            if db_result == 0:
                messagebox.showinfo(message="No existe paciente con ese dato ({})".format(
                    valorSeleccionado), title="Error")
            else:
                cursor.execute(
                    "SELECT * FROM pacientes  WHERE {} = {}".format(valorIntroducir, valorIntroducir))
                listaQuery = cursor.fetchone()
                nombre = listaQuery[0]
                cedula = listaQuery[1]
                telefono = listaQuery[2]
                sesionesR = listaQuery[3]
                sesionesL = listaQuery[4]
                cursor.close()
                conn.close()
                messagebox.showinfo(message="Paciente actualizado con estas características:\nNombre: {}\nDocumento: {}\nTeléfono: {}\nSesiones realizadas: {}\nSesiones llevadas: {}".format(
                    nombre, cedula, telefono, sesionesR, sesionesL), title="Actualizar")
        except:
            messagebox.showinfo(
                message="Error, tipo de dato incorrecto", title="Error")
    Button(ventanaConsultarPaciente, text="Salir",
           command=ventanaConsultarPaciente.destroy).grid(row=2, column=0, sticky=W, pady=4)
    Button(ventanaConsultarPaciente, text="Consultar",
           command=consultarDatos).grid(row=2, column=1, sticky=W, pady=4)


file.add_command(label="Consultar paciente",
                 command=ventanaConsultarPacienteFuncion)


def ventanaAnadirSesionFuncion():
    from tkcalendar import DateEntry
    from tkinter import messagebox
    ventanaAnadirSesion = Toplevel(root)
    ventanaAnadirSesion.title("Añadir sesión")
    ventanaAnadirSesion.wm_iconphoto(False, photo)
    Label(ventanaAnadirSesion, text="Documento").grid(row=0)
    documento = Entry(ventanaAnadirSesion)
    documento.grid(row=0, column=1)
    Label(ventanaAnadirSesion, text="Fecha").grid(row=1)
    sel = StringVar()  # declaring string variable
    cal = DateEntry(ventanaAnadirSesion, selectmode='day',
                    textvariable=sel, locale='es_Mx')
    # Dato curioso: Nuestro date es dia/mes/año, sqlite necesita: año/mes/dia, toca introducirlo de esa forma.
    # Ejemplo: 12/01/23 -> 2023-01-23
    cal.grid(row=1, column=1)

    def cambiarFecha(fechaAntigua):
        fechaAntigua = fechaAntigua.split("/")
        return "20"+fechaAntigua[2]+"-"+fechaAntigua[1]+"-"+fechaAntigua[0]

    def cambiarSesion():
        try:
            conn = sqlite3.connect('doctora.db')
            cursor = conn.cursor()
            doc = int(documento.get())
            date = cambiarFecha(sel.get())
            # Revisar si existe o no
            cursor.execute(
                "SELECT count(*) FROM pacientes WHERE cedula = {}".format(doc))
            # Ver si existe siquiera ese documento
            db_result = cursor.fetchone()[0]
            # Si no existe
            if db_result == 0:
                messagebox.showinfo(
                    message="No existe paciente con ese documento", title="Error")
            else:
                insert = (doc, date)
                cursor.execute('insert into fechas values (?,?)', insert)
                conn.commit()
                cursor.execute(
                    'SELECT COUNT(*) FROM fechas WHERE cedula = {}'.format(doc))
                count = cursor.fetchone()[0]
                query = "UPDATE pacientes SET sesionesL = {} WHERE cedula = {}".format(
                    count, doc)
                cursor.execute(query)
                conn.commit()
                cursor.execute(
                    "SELECT * FROM pacientes  WHERE cedula = {}".format(doc))
                listaQuery = cursor.fetchone()
                nombre = listaQuery[0]
                cedula = listaQuery[1]
                sesionesL = listaQuery[4]
                cursor.close()
                conn.close()
                messagebox.showinfo(message="{} con documento {} lleva {} sesiones".format(
                    nombre, cedula, sesionesL), title="Sesiones")
        except:
            messagebox.showinfo(
                message="Error, tipo de dato incorrecto", title="Error")
    Button(ventanaAnadirSesion, text="Salir", command=ventanaAnadirSesion.destroy).grid(
        row=2, column=0, sticky=W, pady=4)
    Button(ventanaAnadirSesion, text="Añadir", command=cambiarSesion).grid(
        row=2, column=1, sticky=W, pady=4)


file.add_command(label="Añadir sesion", command=ventanaAnadirSesionFuncion)


def eliminarSesionFuncion():
    from tkcalendar import DateEntry
    from tkinter import messagebox
    ventanaEliminarSesion = Toplevel(root)
    ventanaEliminarSesion.title("Eliminar sesión")
    ventanaEliminarSesion.wm_iconphoto(False, photo)
    Label(ventanaEliminarSesion, text="Documento").grid(row=0)
    documento = Entry(ventanaEliminarSesion)
    documento.grid(row=0, column=1)
    Label(ventanaEliminarSesion, text="Fecha").grid(row=1)
    sel = StringVar()  # declaring string variable
    cal = DateEntry(ventanaEliminarSesion, selectmode='day',
                    textvariable=sel, locale='es_Mx')
    # Dato curioso: Nuestro date es dia/mes/año, sqlite necesita: año/mes/dia, toca introducirlo de esa forma.
    # Ejemplo: 12/01/23 -> 2023-01-23
    cal.grid(row=1, column=1)

    def cambiarFecha(fechaAntigua):
        fechaAntigua = fechaAntigua.split("/")
        return "20"+fechaAntigua[2]+"-"+fechaAntigua[1]+"-"+fechaAntigua[0]

    def eliminarSesion():
        try:
            conn = sqlite3.connect('doctora.db')
            cursor = conn.cursor()
            doc = int(documento.get())
            date = cambiarFecha(sel.get())
            # Revisar si existe o no
            cursor.execute(
                "SELECT count(*) FROM pacientes WHERE cedula = {}".format(doc))
            # Ver si existe siquiera ese documento
            db_result = cursor.fetchone()[0]
            # Si no existe
            if db_result == 0:
                messagebox.showinfo(
                    message="No existe paciente con ese documento", title="Error")
            else:
                insert = (doc, date)
                cursor.execute(
                    'DELETE FROM fechas WHERE cedula = {} AND fecha = {} '.format(doc, "'"+date+"'"))
                conn.commit()
                cursor.execute(
                    'SELECT COUNT(*) FROM fechas WHERE cedula = {}'.format(doc))
                count = cursor.fetchone()[0]
                query = "UPDATE pacientes SET sesionesL = {} WHERE cedula = {}".format(
                    count, doc)
                cursor.execute(query)
                conn.commit()
                cursor.execute(
                    "SELECT * FROM pacientes  WHERE cedula = {}".format(doc))
                listaQuery = cursor.fetchone()
                nombre = listaQuery[0]
                cedula = listaQuery[1]
                sesionesL = listaQuery[4]
                cursor.close()
                conn.close()
                messagebox.showinfo(message="{} con documento {} lleva {} sesiones".format(
                    nombre, cedula, sesionesL), title="Sesiones")
        except:
            messagebox.showinfo(
                message="Error, tipo de dato incorrecto", title="Error")
    Button(ventanaEliminarSesion, text="Salir", command=ventanaEliminarSesion.destroy).grid(
        row=2, column=0, sticky=W, pady=4)
    Button(ventanaEliminarSesion, text="Eliminar", command=eliminarSesion).grid(
        row=2, column=1, sticky=W, pady=4)


file.add_command(label="Eliminar sesion", command=eliminarSesionFuncion)


def consultarSesionFuncion():
    from tkinter import messagebox
    ventanaConsultarSesion = Toplevel(root)
    ventanaConsultarSesion.title("Consultar número de sesiones")
    ventanaConsultarSesion.wm_iconphoto(False, photo)
    Label(ventanaConsultarSesion, text="Documento").grid(row=0)
    documento = Entry(ventanaConsultarSesion)
    documento.grid(row=0, column=1)

    def consultarSesion():
        try:
            conn = sqlite3.connect('doctora.db')
            cursor = conn.cursor()
            doc = int(documento.get())
            # Revisar si existe o no
            cursor.execute(
                "SELECT count(*) FROM pacientes WHERE cedula = {}".format(doc))
            # Ver si existe siquiera ese documento
            db_result = cursor.fetchone()[0]
            # Si no existe
            if db_result == 0:
                messagebox.showinfo(
                    message="No existe paciente con ese documento", title="Error")
            else:
                cursor.execute(
                    "SELECT * FROM pacientes  WHERE cedula = {}".format(doc))
                listaQuery = cursor.fetchone()
                nombre = listaQuery[0]
                cedula = listaQuery[1]
                sesionesL = listaQuery[-1]
                cursor.close()
                # Ahora para mostrar todas las sesiones (fechas)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT fecha FROM fechas WHERE cedula = {}".format(doc))
                records = cursor.fetchall()
                mensaje = ""
                for i in range(len(records)):
                    mensaje = mensaje + str(i) + ": " + records[i][0] + "\n"
                conn.close()

                messagebox.showinfo(message="{} con documento {} lleva {} sesiones\n".format(
                    nombre, cedula, sesionesL)+mensaje, title="Sesiones")
        except:
            messagebox.showinfo(
                message="Error, tipo de dato incorrecto", title="Error")
    Button(ventanaConsultarSesion, text="Salir", command=ventanaConsultarSesion.destroy).grid(
        row=1, column=0, sticky=W, pady=4)
    Button(ventanaConsultarSesion, text="Consultar número de sesiones",
           command=consultarSesion).grid(row=1, column=1, sticky=W, pady=4)


file.add_command(label="Consultar sesiones", command=consultarSesionFuncion)


def crearInformeFuncion():
    from tkinter import messagebox
    import pandas as pd
    import os
    ventanaInforme = Toplevel(root)
    ventanaInforme.title("Informe")
    ventanaInforme.wm_iconphoto(False, photo)
    Label(ventanaInforme, text="Selecciona año").grid(row=0)
    ano = Entry(ventanaInforme)
    ano.grid(row=0, column=1)
    # Función crear informe

    def crearInforme():
        # Primer paso: Filtrar por año y mes
        conn = sqlite3.connect('doctora.db')
        cursor = conn.cursor()
        fechaAno = ano.get()
        Meses = ["01", "02", "03", "04", "05", "06",
                 "07", "08", "09", "10", "11", "12"]
        # Recorrer los meses
        # KPIS:
        # 1. Número de sesiones
        # 2. Cuantos terminaron
        # 3. Cuantos iniciaron
        kpi = {mes: [] for mes in Meses}
        for mes in Meses:
            # 1. Número de sesiones
            query = "SELECT COUNT(*) FROM fechas WHERE strftime('%m', fecha) = {} AND strftime('%Y', fecha) = {}".format(
                "'"+mes+"'", "'"+fechaAno+"'")
            cursor.execute(query)
            listaQuery = cursor.fetchone()
            kpi[mes].append(listaQuery[0])
            # 2. Cuantos terminaron
            query = "SELECT COUNT(*) FROM pacientes INNER JOIN (SELECT cedula,max(fecha) FROM fechas GROUP BY cedula HAVING strftime('%m', fecha) = {} AND strftime('%Y', fecha) = {}) as 'a' ON pacientes.cedula = a.cedula WHERE pacientes.sesionesR = pacientes.sesionesL".format("'"+mes+"'", "'"+fechaAno+"'")
            cursor.execute(query)
            listaQuery = cursor.fetchone()
            kpi[mes].append(listaQuery[0])
            # 3. Cuantos iniciaron
            query = "SELECT COUNT(*) FROM pacientes INNER JOIN (SELECT cedula,min(fecha) FROM fechas GROUP BY cedula HAVING strftime('%m', fecha) = {} AND strftime('%Y', fecha) = {}) as 'a' ON pacientes.cedula = a.cedula".format("'"+mes+"'", "'"+fechaAno+"'")
            cursor.execute(query)
            listaQuery = cursor.fetchone()
            kpi[mes].append(listaQuery[0])
        # Segunda parte: Tabla según la enfermedad y mes
        # Busqueda de todas las enfermedades
        # Group by patologia por los que inician en ese mes
        query = """SELECT patologia,STRFTIME("%m", "min(fecha)"),COUNT(patologia) FROM pacientes INNER JOIN (SELECT cedula,min(fecha) FROM fechas GROUP BY cedula) as 'a' ON pacientes.cedula = a.cedula GROUP BY STRFTIME("%m-%Y", "min(fecha)"),patologia HAVING STRFTIME("%Y", "min(fecha)") = {}""".format("'"+fechaAno+"'")
        # Columnas: patología | Fecha
        patologiaMes = pd.read_sql(query, conn)
        patologiaMes.rename(
            columns={'STRFTIME("%m", "min(fecha)")': 'Fecha'}, inplace=True)
        patologiaMes.rename(
            columns={'COUNT(patologia)': 'Repeticiones'}, inplace=True)
        # Pasar a mes
        print(patologiaMes.dtypes)
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        numero = ["01", "02", "03", "04", "05",
                  "06", "07", "08", "09", "10", "11", "12"]
        diccionarioMes = {numero[i]: meses[i] for i in range(12)}
        patologiaMes["fecha"] = [diccionarioMes[x]
                                 for x in patologiaMes["Fecha"]]
        patologiaMes.drop(["Fecha"], axis=1, inplace=True)
        patologiaMes.rename(
            columns={'fecha': 'Fecha'}, inplace=True)
        # De kpi diccionario a pandas
        kpiDiccionario = {'Meses': meses, 'Numero de sesiones': [
            kpi[mes][0] for mes in kpi], 'Pacientes finalizados': [kpi[mes][1] for mes in kpi], 'Pacientes iniciados': [kpi[mes][2] for mes in kpi]}
        kpiTabla = pd.DataFrame(kpiDiccionario)
        # A csv (patologiaMes)
        patologiaMes.to_csv("archivosExcel/patologias.csv", index=False)
        # A csv (kpiDiccionario)
        kpiTabla.to_csv("archivosExcel/informeTotal.csv", index=False)
        # Merge csv
    Button(ventanaInforme, text="Salir", command=ventanaInforme.destroy).grid(
        row=1, column=0, sticky=W, pady=4)
    Button(ventanaInforme, text="Crear", command=crearInforme).grid(
        row=1, column=1, sticky=W, pady=4)


file.add_command(label="Crear informe", command=crearInformeFuncion)
file.add_command(label="Salir", command=root.quit)
# Se añade el menú
menubar.add_cascade(label="Paciente", menu=file)
root.config(menu=menubar)
# Loop del menú
root.mainloop()
