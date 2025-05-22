import os

class GeneradorEstructurasGramatica:
    def __init__(self):
        self.gramatica = []
        self.derivaciones = []
        self.noterminales = []
        self.terminales = []

    def agregarGramatica(self, nombre_archivo: str):
        if not os.path.exists(nombre_archivo):
            print("El archivo no existe")
            return
        
        with open(nombre_archivo, 'r') as archivo:
            numero_linea = 1
            for linea in archivo:
                inicio = 0
                #print("Analizando línea ", str(numLinea), ": ", linea)
                while inicio < len(linea):
                    if linea[inicio] == ".":
                        break
                    inicio += 1
                self.gramatica.append((numero_linea, linea[inicio+2:len(linea)]))
                numero_linea += 1


    def agregarDerivacion(self):
        for i in range(len(self.gramatica)):
            self.derivaciones.append(self.stripCadena(self.leerDerivacion(self.gramatica[i][1])))

    def agregarNoTerminales(self):
        for i in range(len(self.gramatica)):
            ladoIzquierdo = self.stripCadena(self.leerNoTerminales(self.gramatica[i][1]))
            if ladoIzquierdo not in self.noterminales:
                self.noterminales.append(ladoIzquierdo)

    def agregarTerminales(self):
        for i in range(len(self.derivaciones)):
            self.leerTerminales(self.derivaciones[i])

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

    def leerDerivacion(self, linea):
        inicio = 0
        fin = len(linea) - 1
        while inicio <= fin :
            if linea[inicio] == "-" and linea[inicio+1] == ">":
                break
            inicio += 1

        return linea[inicio+2:fin+1]
    
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
                # Si salir fuera del rango de la cadena
                if inicio > 0 and linea[inicio -1] != " ":
                    caracter = linea[inicio-1]
                    if caracter not in self.terminales:
                        self.terminales.append(caracter)
                # Ignorar el resto del no terminal
                while inicio < fin and linea[inicio] != ">":
                    inicio += 1
                # Si el no terminal tiene caracteres después del ">" y no son vacios, entonces separalos
                # Sin salir fuera del rango de la cadena
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

    def main(self):
        self.agregarGramatica("AnalizadorSintáctico/gramatica.txt")
        print('\n')
        self.printGramatica()
        print('\n')
        self.agregarDerivacion()
        self.printDerivacion()
        print('\n')
        self.agregarNoTerminales()
        self.printNoTerminales()
        print('\n')
        self.agregarTerminales()
        self.printTerminales()
        print('\n')

if __name__ == "__main__":
    generador = GeneradorEstructurasGramatica()
    generador.main()
