class GeneradorEstructurasG:
    def __init__(self):
        self.gramatica = []
        self.derivaciones = []
        self.noterminales = []
        self.terminales = []

    def agregarGramatica(self, gramatica):
        with open("PythonProjects\AnalizadorLexico\gramatica.txt") as archivo:
            numLinea = 1
            for linea in archivo:
                print("Analizando línea ", str(numLinea), ": ", linea)
                self.gramatica.append((numLinea, self.stripCadena(linea)))
                numLinea += 1


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

if __name__ == "__main__":
    generador = GeneradorEstructurasG()
    print(generador.gramatica)
    print(generador.derivaciones)
    print(generador.noterminales)
    print(generador.terminales)
