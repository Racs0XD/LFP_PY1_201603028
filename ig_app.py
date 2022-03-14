import tkinter
from tkinter import filedialog, ttk, messagebox
from xml.etree.ElementTree import tostring

def buscador_archivo():
    global artemp
    artemp = ""
    try:
        archivo = filedialog.askopenfilename(
            title="Selección de archivo form", initialdir="./", filetypes=(("form files", "*.form"), ("all files", "*.*")))
        with open(archivo, encoding='utf-8') as cargado:
            artemp = cargado.read().strip()
    except:
        messagebox.showerror(message="Seleccione un archivo", title="Alerta")
        return
    
    scroll = tkinter.Scrollbar(frameIm)
    text = tkinter.Text(frameIm)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    text.pack(side=tkinter.LEFT, fill=tkinter.Y)
    text.config(yscrollcommand=scroll.set)
    text.insert(tkinter.END, artemp)
    



def analizar():
    data = artemp
    #listas de almacenamiento
    global cadena
    token = []
    error = []
    lista_valores = []
    columna = 1
    fila = 1
    temp = ""
    tem = ""
    #tokens
    #palabra reservada
    reservada = ""
    variable = ""
    asignacion = ""
    contenido = ""
    separador = ""
    #variables
    formulario = ""
    conF = ""
    tipo = ""
    valor = ""
    fondo = ""
    nombre = ""
    valores = ""
    form_vacio = True
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
        elif letra == " ":
            ""
        elif formval is True:                 
            if letra != "~":                
                formulario += letra        
            else:
                formval = False 
                tmp = formulario.lower()            
                if tmp == "formulario" or tmp == "formulário":
                    tokentemp = "Token reservado ' "+formulario+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                    token.append(tokentemp)
                else:
                    errortemp = "Error ' "+formulario+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                    error.append(errortemp)
                if letra == "~":                
                    conF += letra                    
        elif conFval is True:
            if letra != "[" and letra != "<":
                conF += letra   
            else:
                conFval = False
                if conF == "~>>":
                    tokentemp = "Token asignación ' "+conF+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                    token.append(tokentemp)
                else:
                    errortemp = "Error ' "+conF+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                    error.append(errortemp)
                if letra == "[":
                    tokentemp = "Token apertura lista ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                    token.append(tokentemp)
                    form = True
                elif letra == "<":
                    errortemp = "Error ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                    error.append(errortemp)                    
        elif form is True:
            if letra == "<":
                tokentemp = "Token apertura formulario ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                token.append(tokentemp)
                nform = True
            else:
                if nform is True:                    
                    if letra != ":":                        
                        temp += letra
                        if temp == "tipo":
                            tipoval = True
                            tokentemp = "Token variable ' "+temp+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                            token.append(tokentemp)                        
                        elif temp == "fondo":
                            fondoval = True  
                            tokentemp = "Token variable ' "+temp+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                            token.append(tokentemp) 
                        elif temp == "nombre":
                            nombreval = True  
                            tokentemp = "Token variable ' "+temp+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                            token.append(tokentemp) 
                        elif temp == "valores":
                            valoresval = True  
                            tokentemp = "Token variable ' "+temp+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                            token.append(tokentemp)
                        elif temp == "valor":
                            valorval = True  
                            tokentemp = "Token variable ' "+temp+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                            token.append(tokentemp)      
                        elif valorval is True and valoresval is True:
                            valorval = False                   
                    else:         
                        temp = ""               
                        nform = False     
                        tokentemp = "Token asignación ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)  
               #Validación de tipo
                elif tipoval is True:
                    if letra == "\"":
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                    elif letra != ">" and letra != ",":
                        tipo += letra
                    else:
                        tokentemp = "Token separador ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                        tipoval = False
                        nform = True
                #Validación de valor
                elif valorval is True:
                    if letra == "\"":
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                    elif letra != ">" and letra != ",":
                        valor += letra
                    else:
                        tokentemp = "Token separador ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                        valorval = False              
                        nform = True      
                #Validación de tipo
                elif tipoval is True:
                    if letra == "\"":
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                    elif letra != ">" and letra != ",":
                        tipo += letra
                    else:
                        tokentemp = "Token separador ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                        tipoval = False
                        nform = True
                #Validación de fondo
                elif fondoval is True:
                    if letra == "\"":
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                    elif letra != ">" and letra != ",":
                        fondo += letra
                    else:
                        tokentemp = "Token separador ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                        fondoval = False 
                        nform = True
                #Validación de nombre
                elif nombreval is True:
                    if letra == "\"":
                        tokentemp = "Token contenedor ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                    elif letra != ">" and letra != ",":
                        nombre += letra
                    else:
                        tokentemp = "Token separador ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                        nombreval = False  
                        nform = True
                #Validación de valores
                elif valoresval is True:
                    if letra == "[":
                        tokentemp = "Token contenedor de Lista ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                        valista = True
                    elif letra == "]":
                        tokentemp = "Token de cierre de Lista ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                        valista = False
                    elif valista is True:
                        if letra == "'" and letra ==" ":
                            ""
                        elif letra != ">" and letra != ",":
                            valores += letra
                        else:
                            lista_valores.append(valores)
                            valores = ""
                    elif letra != ">" and letra != ",":
                        if letra == "'":
                            errortemp = "Error ' "+conF+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                            error.append(errortemp)
                        else:
                            valores += letra
                    else:
                        tokentemp = "Token separador ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                        token.append(tokentemp)
                        valoresval = False 
                        nform = True
                elif letra == ">":                    
                    tokentemp = "Token de cierre ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
                    token.append(tokentemp)  
                    #agregar validación para apendisar valores a lista      
                    forms = {
                        tipo
                    } 
                    form = False    
        elif letra == ",":
            tokentemp = "Token separador ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
            token.append(tokentemp)
            form = True
        elif letra == "]":
            print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
            tokentemp = "Token de cierre de archivo ' "+letra+" ' encontrado en Lín. "+str(fila)+", col. "+str(columna)
            token.append(tokentemp)

                    
                            
                    
                
                     
            
        
        #Aplicando match
    for a in token:        
        print(a)
        print("==================================================")
    for b in error:      
        print(b)
        print("==================================================")
        
       

    

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
frameIm.place(x=140, y=65)
# Color de fondo, background
frameIm.config(bg="white")
# Podemos establecer un tamaño
frameIm.config(width=680, height=405)
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

boton6 = tkinter.Button(frameAr, text="Cargar", fg="white", font=(
    "broadway 12 bold"), command=buscador_archivo, borderwidth=0, bg="grey")
boton6.place(x=25, y=5)
boton6.config(width=12, height=1)

boton7 = tkinter.Button(frameAr, text="Analizar", fg="white", font=(
    "broadway 12 bold"), command=analizar, borderwidth=0, bg="grey")
boton7.place(x=205, y=5)
boton7.config(width=12, height=1)

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
