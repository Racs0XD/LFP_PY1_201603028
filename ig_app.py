import tkinter
from tkinter import filedialog, ttk, messagebox
from turtle import update
from xml.etree.ElementTree import tostring

from numpy import empty

def buscador_archivo():
    cargado = False
    global artemp
    try:
        archivo = filedialog.askopenfilename(
            title="Selección de archivo form", initialdir="./", filetypes=(("form files", "*.form"), ("all files", "*.*")))
        with open(archivo, encoding='utf-8') as cargado:
            artemp = cargado.read().strip()
    except:
        messagebox.showerror(message="Seleccione un archivo", title="Alerta")
        return
    
    if cargado is False:
        carga(artemp)
    else:
        recarga(artemp)
    
def carga(artemp):    
    text.insert(tkinter.END, artemp)

def recarga(artemp):
    text.delete("1.0","end")
    text.insert(tkinter.END, artemp)


def analizar():
    try:        
        data = text.get(1.0, "end-1c")
    except Exception as e:
        messagebox.showerror(message="Error, no se a cargado archivo para analizar", title="Alerta")    
    
    #listas de almacenamiento
    global formslist, tokn, error
    tokn = []
    error = []
    lista_valores = {}
    formslist = []
    columna = 1
    fila = 1
    temp = ""
    formulario = ""
    conF = ""
    tipo = ""
    valor = ""
    fondo = ""
    nombre = ""
    valores = ""
    tm = ""
    formval = True
    conFval = True
    tipoval = False
    valorval = False
    fondoval = False
    nombreval = False
    valoresval = False
    valista = False
    nform = False
    form = False
    reservada = True
    #Inicio del autómata
    for letra in data:
             
        if letra == "\n":
            fila += 1
            columna = 1
        else:
            columna += 1        
     
        if letra == "\n":
            ""
        elif letra == " " and valista is False:
            ""
        elif formval is True:                 
            if letra != "~":                
                formulario += letra        
            else:
                formval = False 
                tmp = formulario.lower()            
                if tmp == "formulario" or tmp == "formulário":
                    tokentemp = "Token palabra reservada ' "+formulario+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    tokn.append(tokentemp)
                else:
                    errortemp = "Error ' "+formulario+" ' se esperaria ' formulario ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    error.append(errortemp)
                if letra == "~":                
                    conF += letra                    
        elif conFval is True:
            if letra != "[" and letra != "<":
                conF += letra   
            else:
                conFval = False
                if conF == "~>>":
                    tokentemp = "Token asignacion ' "+conF+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    tokn.append(tokentemp)
                else:
                    errortemp = "Error ' "+conF+" ' se esperaria ' ~>> ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    error.append(errortemp)
                if letra == "[":
                    tokentemp = "Token contenedor apertura documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    tokn.append(tokentemp)
                    form = True
                elif letra == "<":
                    errortemp = "Error ' "+letra+" ' se esperaria ' [ ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    error.append(errortemp)  
        elif form is True:

            if letra == "<":
                tokentemp = "Token contenedor apertura formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                tokn.append(tokentemp)
                nform = True
            else:
                if nform is True:                    
                    if letra != ":" and letra != "[" and letra != "\"" and letra != "," and letra != "'":                                         
                        temp += letra.lower()
                        if temp == "tipo" or temp == "típo":
                            tipoval = True
                            reservada = True
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)                 
                        elif temp == "fondo" or temp == "fóndo":
                            fondoval = True 
                            reservada = True 
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)   
                        elif temp == "nombre" or temp == "nómbre":
                            nombreval = True  
                            reservada = True
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)    
                        elif temp == "valor" or temp == "valór":
                            valorval = True  
                            reservada = True
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)   
                        elif valorval is True:
                            reservada = False
                            valorval = False                                              
                        elif temp == "valores" or temp == "valóres":
                            valoresval = True  
                            reservada = True
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)    
                                 
                            
                    else:     
                        if letra == ":":
                            if temp == "":
                                errortemp = "Error ' "+letra+" ' se esperaria ' tipo, valor, fondo, nombre o valores ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                                error.append(errortemp) 
                            elif  temp != "tipo" and temp != "típo" and temp != "fondo" and temp != "fóndo" and temp != "nombre" and temp != "nómbre" and temp != "valor" and temp != "valór" and temp != "valores" and temp != "valóres":
                               errortemp = "Error ' "+ temp +" ' se esperaria palabra reservada ' tipo, valor, fondo, nombre o valores ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                               error.append(errortemp) 
                               temp = "" 
                               reservada = False
                               nform = False                            
                            else:
                                tokentemp = "Token de asignacion' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                                tokn.append(tokentemp)     
                                temp = ""               
                                nform = False 
                        elif letra == "[" or letra == "\"" or letra == "," or letra != "'":
                                errortemp = "Error ' "+ letra +" ' se esperaria ' : ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                                error.append(errortemp)  
                                nform = False
                                temp = "" 
                             
               #Validación de tipo
                elif tipoval is True:
                    if letra == "\"":
                        if valista is True:
                            valista = False
                            if tipo.lower() == "etiqueta" or tipo.lower() == "etiquéta" or tipo.lower() == "texto" or tipo.lower() == "téxto" or tipo.lower() == "grupo-radio" or tipo.lower() == "radio" or tipo.lower() == "grúpo-radio" or tipo.lower() == "grupo-rádio" or tipo.lower() == "grúpo-rádio" or tipo.lower() == "grupo-option" or tipo.lower() == "grúpo-option" or tipo.lower() == "botón" or tipo.lower() == "boton":
                                tokentemp = "Token palabra reservada tipo ' "+tipo+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                                tokn.append(tokentemp)
                            else:
                                errortemp = "Error palabra reservada tipo ' "+tipo+" ' no existente, se esperaria etiqueta, texto, grupo-radio, grupo-option, boton, Lin. "+str(fila)+", col. "+str(columna)
                                error.append(errortemp) 
                            tm = "" 
                        elif not tipo and tm == "cc":
                            errortemp = "Error cadena vacia, se esperaria informacion, Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)  
                            tm = ""                                                                                
                        tokentemp = "Token contenedor cadena ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
                        tm  += "c"
                    elif letra != ">" and letra != "," and letra != "]":
                        tipo += letra
                        valista = True
                    else:                                               
                        tipoval = False
                        nform = True                        
                        if letra == ",":
                            tokentemp = "Token separador ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)                             
                        elif letra == ">":
                            nform = False
                            tokentemp = "Token contenedor cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                        elif  letra == "]":
                            nform = False
                            errortemp = "Error cierre de documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)
                        
                #Validación de valor
                elif valorval is True:
                    if letra == "\"":
                        if valista is True:
                            valista = False
                            tokentemp = "Token cadena ' "+valor+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                            tm = "" 
                        elif not valor and tm == "cc":
                            errortemp = "Error cadena vacia, se esperaria informacion, Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)  
                            tm = ""                                                    
                        tokentemp = "Token contenedor cadena ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
                        tm  += "c"
                    elif letra != ">" and letra != "," and letra != "]":
                        valor += letra
                        valista = True
                    else:                        
                        valista = False
                        valorval = False              
                        nform = True   
                        if letra == ",":
                            tokentemp = "Token separador ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp) 
                        elif letra == ">":
                            nform = False  
                            tokentemp = "Token contenedor cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                        elif  letra == "]":
                            nform = False
                            errortemp = "Error cierre de documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)
                #Validación de fondo
                elif fondoval is True:
                    if letra == "\"":
                        if valista is True:
                            valista = False
                            tokentemp = "Token cadena ' "+fondo+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                            tm = "" 
                        elif not fondo and tm == "cc":
                            errortemp = "Error cadena vacia, se esperaria informacion, Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)  
                            tm = ""                                                    
                        tokentemp = "Token contenedor cadena' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
                        tm  += "c"
                    elif letra != ">" and letra != "," and letra != "]":
                        fondo += letra  
                        valista = True
                    else:
                        valista = False
                        fondoval = False 
                        nform = True
                        if letra == ",":
                            tokentemp = "Token separador ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp) 
                        elif letra == ">":
                            nform = False
                            tokentemp = "Token contenedor cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                        elif  letra == "]":
                            nform = False
                            errortemp = "Error cierre de documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)
                #Validación de nombre
                elif nombreval is True:
                    if letra == "\"":
                        if valista is True:
                            valista = False
                            tokentemp = "Token cadena ' "+nombre+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                            tm = "" 
                        elif not nombre and tm == "cc":
                            errortemp = "Error cadena vacia, se esperaria informacion, Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)  
                            tm = ""                                                    
                        tokentemp = "Token contenedor cadena ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
                        tm  += "c"                    
                    elif letra != ">" and letra != "," and letra != "]":
                        nombre += letra
                        valista = True
                    else:
                        valista = False
                        nombreval = False  
                        nform = True
                        if letra == ",":
                            tokentemp = "Token separador ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp) 
                        elif letra == ">":
                            nform = False
                            tokentemp = "Token contenedor cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                        elif  letra == "]":
                            nform = False
                            errortemp = "Error cierre de documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)
                #Validación de valores
                elif valoresval is True:
                    if letra == "[":
                        valista = True
                        tokentemp = "Token contenedor apertura de lista ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
                    elif valista is False and letra == "'":
                        valista = True
                        errortemp = "Error contenedor en lista ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        error.append(errortemp)
                    elif valista is True:
                        if letra != ">"  and letra != "]":
                            valores += letra
                            valista = True
                        else:
                            valista = False
                            lista_valores = valores                            
                            if letra == "]":
                                valista = False
                                tokentemp = "Token cadena ' "+lista_valores+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna-1)
                                tokn.append(tokentemp)
                                tokentemp = "Token contenedor cierre de lista ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                                tokn.append(tokentemp)
                            elif letra == ">":
                                valista = False
                                errortemp = "Error cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                                error.append(errortemp)
                    elif letra != ">" and letra != "," and letra != "\"" and letra != "]":
                        valores += letra 
                    else:
                        lista_valores = valores
                        valores = ""
                        valoresval = False 
                        nform = True
                        if letra == ",":
                            tokentemp = "Token cadena ' "+lista_valores+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna-1)
                            tokn.append(tokentemp)
                            tokentemp = "Token separador ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)                             
                        elif letra == ">":
                            nform = False
                            tokentemp = "Token cadena ' "+lista_valores+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna-1)
                            tokn.append(tokentemp)
                            tokentemp = "Token contenedor cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                        elif  letra == "]":
                            nform = False
                            errortemp = "Error cierre de documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)
                elif nform is False:  
                    #agregar validación para apendisar valores a lista   
                    if tipo == "etiqueta":
                        pv = {
                            "tipo":tipo.replace(" ",""),
                            "valor":valor
                        }
                        formslist.append(pv)
                    elif tipo == "texto":
                        pv = {
                            "tipo":tipo,
                            "valor":valor,
                            "fondo":fondo
                        }
                        formslist.append(pv)
                    elif tipo == "grupo-radio":
                        pv = {
                            "tipo":tipo,
                            "nombre":nombre,
                            "valores":lista_valores
                        }
                        formslist.append(pv)
                    elif tipo == "grupo-option":
                        pv = {
                            "tipo":tipo,
                            "nombre":nombre,
                            "valores":lista_valores
                        }
                        formslist.append(pv)
                    elif tipo == "boton":
                        pv = {
                            "tipo":tipo,
                            "nombre":nombre,
                            "valores":lista_valores
                        }     
                        formslist.append(pv)        
                    tipo = ""
                    valor = ""
                    fondo = ""
                    nombre = ""
                    valores = ""
                    if letra == ",":
                        if reservada is False:
                            nform = False
                        else:                        
                            tokentemp = "Token separador ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            nform = True
                            tokn.append(tokentemp)
                    elif letra == "]":
                        tokentemp = "Token contenedor cierre de documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)    
    generar_form()

import webbrowser

def rep_token():
    try:
        if tokn is not empty:

            f = open('Reporte_token.html', 'w')  

            html_cabeza = """
            <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Token</title>
        </head>

        <body>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">



        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand"> &nbsp;&nbsp;&nbsp;Reporte</a>
        </nav>

        """
            html_header = '''
            <center>
            <h3>
            Lista de tokens
            </h3>
            </center>
            <table border="1", style="margin: 0 auto;",class="default">
            <tr>
            <th>Tokens</th>
            </tr>
            '''
            html_mid = ''
            for a in range(len(tokn)):
                n = tokn[a]
                html_mid += '''<tr>
            <td>{}</td>
            </tr>'''.format(n)

            hmtl_end = """</table><br><br>
            """
            html_pie="""


            <br><br><br><br><br><br>
            <footer>
            </footer>

            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
            integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
            crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
            integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
            crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
            integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
            crossorigin="anonymous"></script>
        </body>
        <style>
            table {
            border: #b2b2b2 1px solid;
            border-collapse: separate;

            }
            th {
            border: black 1px solid;
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #357baa;
            color: white;
            }
            td, th {
            border: 1px solid #ddd;
            padding: 8px;
            }

            tr:nth-child(even){background-color: #c0c0c0;}

            tr:hover {background-color: #ddd;}


            </style>

        </body>
            """

            html = html_cabeza  + html_header + html_mid + hmtl_end + html_pie

            f.write(html)     
            f.close()     
            file = webbrowser.open('Reporte_token.html')  
        else:
            messagebox.showerror(message="No tienes ningún token", title="Alerta")
    except Exception as e:
        messagebox.showerror(message="Error, no se a cargado o analizado ningúna información", title="Alerta")
    
    

def rep_error():
    try:
        if len(error) != 0:

            f = open('Reporte_error.html', 'w')  

            html_cabeza = """
            <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Errores</title>
        </head>

        <body>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">



        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand"> &nbsp;&nbsp;&nbsp;Reporte</a>
        </nav>

        """
            html_header = '''
            <center>
            <h3>
            Lista de errores
            </h3>
            </center>
            <table border="1", style="margin: 0 auto;",class="default">
            <tr>
            <th>Errores</th>
            </tr>
            '''
            html_mid = ''
            for a in range(len(error)):
                n = error[a]
                html_mid += '''<tr>
            <td>{}</td>
            </tr>'''.format(n)

            hmtl_end = """</table><br><br>
            """
            html_pie="""


            <br><br><br><br><br><br>
            <footer>
            </footer>

            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
            integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
            crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
            integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
            crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
            integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
            crossorigin="anonymous"></script>
        </body>
        <style>
            table {
            border: #b2b2b2 1px solid;
            border-collapse: separate;

            }
            th {
            border: black 1px solid;
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #357baa;
            color: white;
            }
            td, th {
            border: 1px solid #ddd;
            padding: 8px;
            }

            tr:nth-child(even){background-color: #c0c0c0;}

            tr:hover {background-color: #ddd;}


            </style>

        </body>
            """

            html = html_cabeza  + html_header + html_mid + hmtl_end + html_pie

            f.write(html)     
            f.close()     
            file = webbrowser.open('Reporte_error.html')  
        else:
            messagebox.showerror(message="Felicidades no tienes errores", title="Alerta")
    except Exception as e:
        messagebox.showerror(message="Error, no se a cargado o analizado ningúna información", title="Alerta")
    
    

def generar_form():
    try:
        "analizar()"
    except Exception as e:
        messagebox.showerror(message="Error, no se a cargado o analizado ningúna información", title="Alerta")
    f = open('Formulario.html', 'w')  

    if len(error) == 0:
        etiquetaval = False
        textoval = False
        radioval = False
        optionval = False
        botonval = False

        for a in range(len(formslist)):
            tipo = formslist[a]['tipo']     

            if tipo == "etiqueta":
                etiquetaval = True
                html_etiqueta = """
                <h3>
                {}
                </h3>            
                """.format(formslist[a]['valor'])
            elif tipo == "texto":
                textoval = True
                html_texto = """  
                <input type="text" id="txt" size="40" value={} placeholder={}><br><br>
                """.format(formslist[a]['valor'],"\""+formslist[a]['fondo']+"\"")
            elif tipo == "grupo-radio":
                radioval = True
                vlores = formslist[a]['valores'].replace("'","").split(",")

                html_r1 = """
                <form>
                <label for="radio">{}</label>&nbsp;&nbsp;
                """.format(formslist[a]['nombre'])

                html_r2 = ""
                for i in range(len(vlores)):                
                    r = vlores[i]
                    
                    html_r2 += """       
                    <input type="radio" name="radio" value={}>
                    <label for="inf">{}</label>            
                    """.format(r,r)
                                    
                html_r3 = """     
                </form>
                """
                html_radio = html_r1 + html_r2 + html_r3
            elif tipo == "grupo-option":
                optionval = True
                vlores = formslist[a]['valores'].replace("'","").split(",")

                html_o1 = """
                <form>
                <label for="lista">{}</label>&nbsp;&nbsp;
                <select name="lista" id="list">
                """.format(formslist[a]['nombre'])

                html_o2 = ""
                for i in range(len(vlores)):                
                    r = vlores[i]
                    
                    html_o2 += """      
                    <option value={}>{}</option>          
                    """.format("\""+r+"\"",r)
                                    
                html_o3 = """            
                    </select>
                </form>
                """
                html_option = html_o1 + html_o2 + html_o3
            elif tipo == "boton":
                botonval = True
                vlores = formslist[a]['valores'].lower()

                if vlores == "entrada":
                    html_boton1 = """
                    <input type="submit" onclick="f()" value={}>                         
                    """.format(formslist[a]['nombre']) 
                    html_boton2="""
                    <textarea id="myDIV" rows="20" cols="80" readonly>
                    {}
                    </textarea>
                    
                    """.format(text.get(1.0, "end-1c")) 
                    html_boton3="""  
                    <style>
                      textarea {
                      display: none;                      
                      }                      
                    </style>                
                    <script>                    
                    
                    function f() {
                    var y = document.getElementById("myDIV").value;
                    var x = document.getElementById("myDIV");
                    alert(y);
                      
                      if (x.style.display === "none") {
                        x.style.display = "block";
                      } else {
                        x.style.display = "none";
                      }
                    }
                    </script>
                    """
                    html_boton = html_boton1 + html_boton2 + html_boton3
                elif vlores == "info":
                    html_boton1 = """
                    <input type="submit" onclick="f()" value={}><br>                         
                    """.format(formslist[a]['nombre']) 
                    html_boton2="""
                    
                    
                    """
                    html_boton3="""               
                    <h4 id="inp"></h4>
                    <h4 id="rad"></h4>
                    <h4 id="lis"></h4> <br>
                    <script>
                    function f() {
                    var x = document.getElementById("txt").value;
                    document.getElementById("inp").innerHTML = x;

                    var y = document.querySelector('input[name="radio"]:checked').value;
                    document.getElementById("rad").innerHTML = y;

                    var z = document.getElementById('list');
                    var val = z.options[z.selectedIndex].value;
                    document.getElementById("lis").innerHTML = val;
                    
                    
                    alert(x+"  "+y+"  "+val);
                    }
                    </script>
                    """
                    html_boton = html_boton1 + html_boton2 + html_boton3

                

        html_cabeza = """
            <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte</title>
            </head>

            <body>

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">



            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <a class="navbar-brand"> &nbsp;&nbsp;&nbsp;Reporte</a>
            </nav>
            <div class="wrapper fadeInDown">
            <div id="formContent">
            """
        html_pie="""   
            </div>
            </div>
            <br>
            <footer>
            </footer>

            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
            integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
            crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
            integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
            crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
            integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
            crossorigin="anonymous"></script>
            </body>
            <style>
            table {
            border: #b2b2b2 1px solid;
            border-collapse: separate;
            
            }
            th {
            border: black 1px solid;
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #357baa;
            color: white;
            }
            td, th {
            border: 1px solid #ddd;
            padding: 8px;
            }
            
            tr:nth-child(even){background-color: #c0c0c0;}
            
            tr:hover {background-color: #ddd;}

            
            html {
            background-color: #56baed;
            }

            body {
            font-family: "Poppins", sans-serif;
            height: 100vh;
            }

            a {
            color: #92badd;
            display:inline-block;
            text-decoration: none;
            font-weight: 400;
            }

            h2 {
            text-align: center;
            font-size: 16px;
            font-weight: 600;
            text-transform: uppercase;
            display:inline-block;
            margin: 40px 8px 10px 8px; 
            color: #cccccc;
            }



            /* STRUCTURE */

            .wrapper {
            display: flex;
            align-items: center;
            flex-direction: column; 
            justify-content: BOTTOM;
            width: 100%;
            min-height: 100%;
            padding: 20px;
            }

            #formContent {
            -webkit-border-radius: 10px 10px 10px 10px;
            border-radius: 10px 10px 10px 10px;
            background: #fff;
            padding: 30px;
            width: 150%;
            max-width: 660px;
            position: relative;
            padding: 0px;
            -webkit-box-shadow: 0 30px 60px 0 rgba(0,0,0,0.3);
            box-shadow: 0 30px 60px 0 rgba(0,0,0,0.3);
            text-align: center;
            }

            #formFooter {
            background-color: #f6f6f6;
            border-top: 1px solid #dce8f1;
            padding: 25px;
            text-align: center;
            -webkit-border-radius: 0 0 10px 10px;
            border-radius: 0 0 10px 10px;
            }



            /* TABS */

            h2.inactive {
            color: #cccccc;
            }

            h2.active {
            color: #0d0d0d;
            border-bottom: 2px solid #5fbae9;
            }



            /* FORM TYPOGRAPHY*/

            input[type=button], input[type=submit], input[type=reset]  {
            background-color: #56baed;
            border: none;
            color: white;
            padding: 15px 80px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            text-transform: uppercase;
            font-size: 13px;
            -webkit-box-shadow: 0 10px 30px 0 rgba(95,186,233,0.4);
            box-shadow: 0 10px 30px 0 rgba(95,186,233,0.4);
            -webkit-border-radius: 5px 5px 5px 5px;
            border-radius: 5px 5px 5px 5px;
            margin: 5px 20px 40px 20px;
            -webkit-transition: all 0.3s ease-in-out;
            -moz-transition: all 0.3s ease-in-out;
            -ms-transition: all 0.3s ease-in-out;
            -o-transition: all 0.3s ease-in-out;
            transition: all 0.3s ease-in-out;
            }

            input[type=button]:hover, input[type=submit]:hover, input[type=reset]:hover  {
            background-color: #39ace7;
            }

            input[type=button]:active, input[type=submit]:active, input[type=reset]:active  {
            -moz-transform: scale(0.95);
            -webkit-transform: scale(0.95);
            -o-transform: scale(0.95);
            -ms-transform: scale(0.95);
            transform: scale(0.95);
            }

            input[type=text] {
            background-color: #f6f6f6;
            border: none;
            color: #0d0d0d;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 5px;
            width: 85%;
            border: 2px solid #f6f6f6;
            -webkit-transition: all 0.5s ease-in-out;
            -moz-transition: all 0.5s ease-in-out;
            -ms-transition: all 0.5s ease-in-out;
            -o-transition: all 0.5s ease-in-out;
            transition: all 0.5s ease-in-out;
            -webkit-border-radius: 5px 5px 5px 5px;
            border-radius: 5px 5px 5px 5px;
            }

            input[type=text]:focus {
            background-color: #fff;
            border-bottom: 2px solid #5fbae9;
            }

            input[type=text]:placeholder {
            color: #cccccc;
            }



            /* ANIMATIONS */

            /* Simple CSS3 Fade-in-down Animation */
            .fadeInDown {
            -webkit-animation-name: fadeInDown;
            animation-name: fadeInDown;
            -webkit-animation-duration: 1s;
            animation-duration: 1s;
            -webkit-animation-fill-mode: both;
            animation-fill-mode: both;
            }

            @-webkit-keyframes fadeInDown {
            0% {
                opacity: 0;
                -webkit-transform: translate3d(0, -100%, 0);
                transform: translate3d(0, -100%, 0);
            }
            100% {
                opacity: 1;
                -webkit-transform: none;
                transform: none;
            }
            }

            @keyframes fadeInDown {
            0% {
                opacity: 0;
                -webkit-transform: translate3d(0, -100%, 0);
                transform: translate3d(0, -100%, 0);
            }
            100% {
                opacity: 1;
                -webkit-transform: none;
                transform: none;
            }
            }

            /* Simple CSS3 Fade-in Animation */
            @-webkit-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
            @-moz-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
            @keyframes fadeIn { from { opacity:0; } to { opacity:1; } }

            .fadeIn {
            opacity:0;
            -webkit-animation:fadeIn ease-in 1;
            -moz-animation:fadeIn ease-in 1;
            animation:fadeIn ease-in 1;

            -webkit-animation-fill-mode:forwards;
            -moz-animation-fill-mode:forwards;
            animation-fill-mode:forwards;

            -webkit-animation-duration:1s;
            -moz-animation-duration:1s;
            animation-duration:1s;
            }

            .fadeIn.first {
            -webkit-animation-delay: 0.4s;
            -moz-animation-delay: 0.4s;
            animation-delay: 0.4s;
            }

            .fadeIn.second {
            -webkit-animation-delay: 0.6s;
            -moz-animation-delay: 0.6s;
            animation-delay: 0.6s;
            }

            .fadeIn.third {
            -webkit-animation-delay: 0.8s;
            -moz-animation-delay: 0.8s;
            animation-delay: 0.8s;
            }

            .fadeIn.fourth {
            -webkit-animation-delay: 1s;
            -moz-animation-delay: 1s;
            animation-delay: 1s;
            }

            /* Simple CSS3 Fade-in Animation */
            .underlineHover:after {
            display: block;
            left: 0;
            bottom: -10px;
            width: 0;
            height: 2px;
            background-color: #56baed;
            content: "";
            transition: width 0.2s;
            }

            .underlineHover:hover {
            color: #0d0d0d;
            }

            .underlineHover:hover:after{
            width: 100%;
            }



            /* OTHERS */

            *:focus {
                outline: none;
            } 

            #icon {
            width:60%;
            }
            
            
            </style>

            </body>
            """
        
        if etiquetaval is True:
            html_etiqueta = html_etiqueta
            etiquetaval = False
        else:
            html_etiqueta = ""
        
        if textoval is True:
            html_texto = html_texto
            textoval = False
        else:
            html_texto = ""

        if radioval is True:
            html_radio = html_radio
            radioval = False
        else:
            html_radio = ""

        if optionval is True:
            html_option = html_option
            optionval = False
        else:
            html_option = ""

        if botonval is True:
            html_boton = html_boton
            botonval = False
        else:
            html_boton = ""


        html = html_cabeza  + html_etiqueta + html_texto + html_radio + html_option + html_boton + html_pie        
        f.write(html)     
        f.close()     
        file = webbrowser.open('Formulario.html')  
    else:
        messagebox.showerror(message="El documento contiene errores", title="Alerta")

def manual_tecnico():
    f = open('Tecnico.html', 'w')

    html_cabeza = """
            <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Token</title>
        </head>

        <body>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">



        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand"> &nbsp;&nbsp;&nbsp;Reporte</a>
        </nav>

        """

    html_pie="""


            <br><br><br><br><br><br>
            <footer>
            </footer>

            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
            integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
            crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
            integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
            crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
            integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
            crossorigin="anonymous"></script>
        </body>
        <style>
            table {
            border: #b2b2b2 1px solid;
            border-collapse: separate;

            }
            th {
            border: black 1px solid;
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: #357baa;
            color: white;
            }
            td, th {
            border: 1px solid #ddd;
            padding: 8px;
            }

            tr:nth-child(even){background-color: #c0c0c0;}

            tr:hover {background-color: #ddd;}


            </style>

        </body>
            """

    html_tecnico = """
    <iframe src="Manual_Tecnico.pdf" height="100%" width="100%"></iframe>

    """
    html = html_cabeza  + html_tecnico +  html_pie    

    f.write(html)     
    f.close()     
    file = webbrowser.open('Tecnico.html') 
    

    # -----------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------- Listas --------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------- XML --------------------------------------------------------


ventana = tkinter.Tk()
ventana.title("Formularios dinámicos")
ventana.geometry("1100x700")
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ Frames ---------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
frame = tkinter.Frame(ventana)
# Establece la posición del componente
frame.place(x=35, y=85)
# Color de fondo, background
frame.config(bg="lightgrey")
# Podemos establecer un tamaño
frame.config(width=1000, height=550)
# Establece el ancho del borde
frame.config(bd=10)
# Establece el tipo de relieve para el borde
frame.config(relief="ridge")

frameAr = tkinter.Frame(ventana)
# Establece la posición del componente
frameAr.place(x=35, y=10)
# Color de fondo, background
frameAr.config(bg="lightgrey")
# Podemos establecer un tamaño
frameAr.config(width=400, height=60)
# Establece el ancho del borde
frameAr.config(bd=10)
# Establece el tipo de relieve para el borde
frameAr.config(relief="ridge")

frameBu = tkinter.Frame(ventana)
# Establece la posición del componente
frameBu.place(x=450, y=15)
# Color de fondo, background
frameBu.config(bg="lightgrey")
# Podemos establecer un tamaño
frameBu.config(width=410, height=60)
# Establece el ancho del borde
frameBu.config(bd=10)
# Establece el tipo de relieve para el borde
frameBu.config(relief="ridge")

frameIm = tkinter.Frame(frame)
# Establece la posición del componente
frameIm.place(x=20, y=20)
# Color de fondo, background
frameIm.config(bg="white")
# Podemos establecer un tamaño
frameIm.config(width=940, height=490)
# Establece el ancho del borde
frameIm.config(bd=10)
# Establece el tipo de relieve para el borde
frameIm.config(relief="ridge")

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ Labels ---------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
"""Label1 = tkinter.Label(frameInfo, text="Canción")
    Label1.config(fg="white", bg="grey", font=("broadway 18 bold"))
    Label1.place(x=10,y=40)

    CANCION = "VALOR"

    Label1A = tkinter.Label(frameInfo, text=CANCION)
    Label1A.config(fg="white", bg="grey", font=("broadway 15 "))
    Label1A.place(x=150,y=45)

    Label2 = tkinter.Label(frameInfo, text="Artista")
    Label2.config(fg="white", bg="grey", font=("broadway 18 bold"))
    Label2.place(x=10,y=90)

    ARTISTA = "VALOR2"

    Label2A = tkinter.Label(frameInfo, text=ARTISTA)
    Label2A.config(fg="white", bg="grey", font=("broadway 15"))
    Label2A.place(x=150,y=95)

    Label3 = tkinter.Label(frameInfo, text="Album")
    Label3.config(fg="white", bg="grey", font=("broadway 18 bold"))
    Label3.place(x=10,y=140)

    ALBUM = "VALOR3"

    Label3A = tkinter.Label(frameInfo, text=ALBUM)
    Label3A.config(fg="white", bg="grey", font=("broadway 15"))
    Label3A.place(x=150,y=145)"""

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ Buttons --------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


def hola():
    print("Hola Mundo")

def combobox_estado():
    if comboReportes.get()=="Reporte de tokens":
        rep_token()
    elif comboReportes.get()=="Reporte de errores":
        rep_error()
    elif comboReportes.get()=="Manual de Usuario":
        print("Manual de Usuario")
    elif comboReportes.get()=="Manual Técnico":
        manual_tecnico()

boton1 = tkinter.Button(frameAr, text="Cargar", fg="white", font=(
    "broadway 12 bold"), command=buscador_archivo, borderwidth=0, bg="grey")
boton1.place(x=25, y=5)
boton1.config(width=12, height=1)

boton2 = tkinter.Button(frameAr, text="Analizar", fg="white", font=(
    "broadway 12 bold"), command=analizar, borderwidth=0, bg="grey")
boton2.place(x=205, y=5)
boton2.config(width=12, height=1)

boton3 = tkinter.Button(ventana, text="Generar", fg="black", font=(
    "broadway 12 bold"), command=combobox_estado, borderwidth=0, bg="lightgrey")
boton3.place(x=730, y=10)
boton3.config(width=12, height=1)
boton3.config(bd=10)
# Establece el tipo de relieve para el borde
boton3.config(relief="ridge")

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ Combobox --------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

comboReportes = ttk.Combobox(frameBu,state="readonly", values=[
    "Reporte de tokens", "Reporte de errores", "Manual de Usuario", "Manual Técnico"], font=("broadway 12 bold"))
comboReportes.grid(column=0, row=1)
comboReportes.current(2)
comboReportes.config(width=20, height=10)




# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ TextArea --------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
global text
scroll = tkinter.Scrollbar(frameIm)
text = tkinter.Text(frameIm, height = 29,width =113)
scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
text.pack(side=tkinter.LEFT, fill=tkinter.Y)
text.config(yscrollcommand=scroll.set)

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------- Entry ---------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

ventana.config(cursor="arrow")
ventana.config(bg="grey")
ventana.config(bd=15)
ventana.config(relief="ridge")
ventana.mainloop()
