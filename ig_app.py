import tkinter
from tkinter import filedialog, ttk, messagebox
from xml.etree.ElementTree import tostring

from numpy import empty

def buscador_archivo():
    global text
    try:
        archivo = filedialog.askopenfilename(
            title="Selección de archivo form", initialdir="./", filetypes=(("form files", "*.form"), ("all files", "*.*")))
        with open(archivo, encoding='utf-8') as cargado:
            artemp = cargado.read().strip()
    except:
        messagebox.showerror(message="Seleccione un archivo", title="Alerta")
        return
    
    scroll = tkinter.Scrollbar(frameIm)
    text = tkinter.Text(frameIm, height = 29,width =113)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text.pack(side=tkinter.LEFT, fill=tkinter.Y)
    text.config(yscrollcommand=scroll.set)
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
                    errortemp = "Error ' "+formulario+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
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
                    errortemp = "Error ' "+conF+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    error.append(errortemp)
                if letra == "[":
                    tokentemp = "Token apertura documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    tokn.append(tokentemp)
                    form = True
                elif letra == "<":
                    errortemp = "Error ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                    error.append(errortemp)  
        elif form is True:
            if letra == "<":
                tokentemp = "Token apertura formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                tokn.append(tokentemp)
                nform = True
            else:
                if nform is True:                    
                    if letra != ":" and letra != "[" and letra != "\"" and letra != "," and letra != "'":                                         
                        temp += letra.lower()
                        if temp == "tipo":
                            tipoval = True
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)                 
                        elif temp == "fondo":
                            fondoval = True  
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)   
                        elif temp == "nombre":
                            nombreval = True  
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)    
                        elif temp == "valor":
                            valorval = True  
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)                         
                        elif temp == "valores":
                            valoresval = True  
                            tokentemp = "Token palabra reservada ' "+temp+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)    
                            if valorval is True:
                                valorval = False     
                    else:     
                        tokentemp = "Token de asignacion' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)     
                        temp = ""               
                        nform = False      
               #Validación de tipo
                elif tipoval is True:
                    if letra == "\"":
                        if valista is True:
                            valista = False
                            tokentemp = "Token cadena ' "+tipo+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
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
                            tokentemp = "Token cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
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
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
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
                            tokentemp = "Token cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
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
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
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
                            tokentemp = "Token cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
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
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
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
                            tokentemp = "Token cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            tokn.append(tokentemp)
                        elif  letra == "]":
                            nform = False
                            errortemp = "Error cierre de documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)
                #Validación de valores
                elif valoresval is True:
                    if letra == "[":
                        valista = True
                        tokentemp = "Token apertura de lista ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
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
                                tokentemp = "Token cierre de lista ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
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
                            tokentemp = "Token cierre de formulario ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
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
                        nform = True
                        tokentemp = "Token separador ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)
                    elif letra == "]":
                        tokentemp = "Token cierre de documento ' "+letra+" ' encontrado en Lin. "+str(fila)+", col. "+str(columna)
                        tokn.append(tokentemp)    
    generar_form()

    
        
import webbrowser

def rep_token():
    try:
        analizar()
    except Exception as e:
        messagebox.showerror(message="Error, no se a cargado o analizado ningúna información", title="Alerta")
    
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

def rep_error():
    try:
        analizar()
    except Exception as e:
        messagebox.showerror(message="Error, no se a cargado o analizado ningúna información", title="Alerta")
    
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
                <input type="text" name={} size="40" placeholder={}><br><br>
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
                    <input type="radio" name="radio" value="valores">
                    <label for="inf">{}</label>            
                    """.format(r)
                                    
                html_r3 = """            
                </div>
                </form>
                """
                html_radio = html_r1 + html_r2 + html_r3
            elif tipo == "grupo-option":
                optionval = True
                vlores = formslist[a]['valores'].replace("'","").split(",")

                html_o1 = """
                <form>
                <label for="lista">{}</label>&nbsp;&nbsp;
                <select name="lista" id="lista">
                """.format(formslist[a]['nombre'])

                html_o2 = ""
                for i in range(len(vlores)):                
                    r = vlores[i]
                    
                    html_o2 += """      
                    <option value={}>{}</option>          
                    """.format(r,r)
                                    
                html_o3 = """            
                    </select>
                </form>
                """
                html_option = html_o1 + html_o2 + html_o3
            elif tipo == "boton":
                botonval = True
                vlores = formslist[a]['valores'].lower()

                if vlores == "entrada":
                    print(vlores)
                elif vlores == "formulario":
                    print(vlores)

                html_boton = """
                <button type="button">{}</button>
                """.format(formslist[a]['nombre'])

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
        print("Manual Técnico")

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
