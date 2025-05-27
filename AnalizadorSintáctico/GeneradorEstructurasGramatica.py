import os

class GeneradorEstructurasGramatica:
    def __init__(self):
        self.gramatica = []
        self.derivaciones = []
        self.noterminales = []
        self.terminales = []
        self.matrizPredictiva = [[1, 0,0, 0,0,0,0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 2,0, 0,0,2,0, 0,2, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
                                 [0, 3,4, 0,0,3,0, 0,3, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0],
                                 [0, 6,0, 0,0,7,0, 0,8, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
                                 [0, 9,0, 0,0,0,0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0,0,11,0,0,0,11,0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0,12,0, 0,0,0,0, 0,0, 0,12,12,12, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0,0,14,0,0,0,14,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0,15,0, 0,0,0,0, 0,0, 0,16,17,18, 0, 0, 0,13,13,13,13],
                                 [0, 0,0, 0,0,0,0, 0,0, 0, 0, 0, 0,19,20,21, 0, 0, 0, 0],
                                 [0, 0,0, 0,0,0,0, 0,0, 0, 0, 0, 0, 0, 0, 0,22,23,25,24]]

    # Método para leer la gramática desde un archivo y almacenarla
    def agregarGramatica(self, nombre_archivo: str):
        if not os.path.exists(nombre_archivo):
            print("El archivo no existe")
            return
        
        # Busca el primer punto '.' para empezar a leer la producción
        print("\nAbriendo gramatica.txt")
        with open(nombre_archivo, 'r') as archivo:
            numero_linea = 1
            print()
            for linea in archivo:
                inicio = 0
                print("Analizando línea ", str(numero_linea), ": ", linea)
                while inicio < len(linea):
                    if linea[inicio] == ".":
                        break
                    inicio += 1
                # Almacena la línea con número de línea y la parte de la producción
                self.gramatica.append((numero_linea, linea[inicio+2:len(linea)]))
                numero_linea += 1

    # Extrae las derivaciones del lado derecho de cada producción
    def agregarDerivacion(self):
        for i in range(len(self.gramatica)):
            self.derivaciones.append(self.stripCadena(self.leerDerivacion(self.gramatica[i][1])))

    # Extrae los no terminales del lado izquierdo de cada producción
    def agregarNoTerminales(self):
        for i in range(len(self.gramatica)):
            ladoIzquierdo = self.stripCadena(self.leerNoTerminales(self.gramatica[i][1]))
            if ladoIzquierdo not in self.noterminales:
                self.noterminales.append(ladoIzquierdo)

    # Extrae los terminales desde las derivaciones
    def agregarTerminales(self):
        for i in range(len(self.derivaciones)):
            self.leerTerminales(self.derivaciones[i])

    # Extrae el lado izquierdo (no terminal) de una producción
    def leerNoTerminales(self, linea):
        inicio = 0
        fin = len(linea) - 1
        while inicio <= fin :
            if linea[inicio] == '<':
                break
            inicio += 1
        while fin >= inicio :
            if linea[fin] == '>' and linea[fin-1] == '-':
                fin -= 1
                break
            fin -= 1
            
        return linea[inicio:fin]

    # Extrae el lado derecho (derivación) de una producción
    def leerDerivacion(self, linea):
        inicio = 0
        fin = len(linea) - 1
        while inicio <= fin :
            if linea[inicio] == "-" and linea[inicio+1] == ">":
                break
            inicio += 1

        return linea[inicio+2:fin+1]
    
    # Identifica y almacena los símbolos terminales en una derivación
    def leerTerminales(self, linea):
        inicio = 0
        fin = len(linea)
        simbolo = "" 

        # Desmenusa los caracteres de los simbolos para encontrar diferencias entre los terminales y no terminales
        while inicio < fin:
            caracter = linea[inicio]
            # Si el simbolo empieza con un caracter "<"", entonces es un no terminal
            if caracter == "<":
                # Si el no terminal tiene caracteres antes del "<" y no son vacios, entonces separalos
                # Si sale fuera del rango de la cadena, ignoralo
                if inicio > 0 and linea[inicio -1] != " ":
                    caracter = linea[inicio-1]
                    if caracter not in self.terminales:
                        self.terminales.append(caracter)
                # Ignorar el resto del no terminal
                while inicio < fin and linea[inicio] != ">":
                    inicio += 1
                # Si el no terminal tiene caracteres después del ">" y no son vacios, entonces separalos
                # Si sale fuera del rango de la cadena, ignoralo
                if inicio + 1 < fin and linea[inicio + 1] != " ":
                    inicio += 1
                    caracter = linea[inicio]
                    if caracter not in self.terminales:
                        self.terminales.append(caracter)
                    # Reseteamos el simbolo para evitar que se junten los caracteres
                    simbolo = ""
            # Si el simbolo tiene un espacio vacio, entonces agrega directamente el terminal al arreglo
            elif caracter == " ":
                # Si es un simbolo valido
                if simbolo:
                    # Si el simblo no se encuentra en el arreglo de terminales y no es "ε", entonces agregalo
                    if simbolo not in self.terminales and simbolo != "ε":
                        self.terminales.append(simbolo)
                    simbolo = ""
            else:
                # Aquí iremos agregando los caracteres separados al simbolo final
                simbolo += caracter
            inicio += 1
        # Si es un simbolo valido
        if simbolo:
            # Si el simblo no se encuentra en el arreglo de terminales y no es "ε", entonces agregalo
            if simbolo not in self.terminales and simbolo != "ε":
                self.terminales.append(simbolo)

    # Elimina los espacios en blanco de una cadena
    def stripCadena(self, cadena: str) -> str:
        caracteres_no_validos = " \n\t\r"
        inicio = 0
        fin = len(cadena) - 1

        while inicio <= fin and cadena[inicio] in caracteres_no_validos:
            inicio += 1

        while fin >= inicio and cadena[fin] in caracteres_no_validos:
            fin -= 1
        
        return cadena[inicio:fin + 1] # Devuelve una subcadena desde el inicio hasta el fin + 1
    
    def printGramatica(self):
        print("Gramática: ")
        for i in range(len(self.gramatica)):
            print(self.gramatica[i][0], ": ", self.gramatica[i][1])

    def printDerivacion(self):
        print("Derivaciones: ")
        for i in range(len(self.derivaciones)):
            print(self.derivaciones[i])
    
    def printNoTerminales(self):
        print("No terminales: ")
        for i in range(len(self.noterminales)):
            print(self.noterminales[i])

    def printTerminales(self):
        print("Terminales: ")
        for i in range(len(self.terminales)):
            print(self.terminales[i])
    
    def printMatrizPredictiva(self):
        for fila in self.matrizPredictiva:
            print(fila)

    def getGramatica(self):
        return self.gramatica

    def getDerivaciones(self):
        return self.derivaciones
    
    def getNoTerminales(self):
        return self.noterminales
    
    def getTerminales(self):
        return self.terminales
        
    def getMatrizPredictiva(self):
        return self.matrizPredictiva
    
    def crearEstructuras(self):
        self.agregarGramatica("AnalizadorSintáctico/gramatica.txt")
        self.agregarDerivacion()
        self.agregarNoTerminales()
        self.agregarTerminales() 
