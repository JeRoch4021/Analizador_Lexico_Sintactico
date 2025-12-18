import os
import pila as Pila
import MetodosString as MS

class Optimizacion:
    def __init__(self, codigo_intermedio="AnalizadorSemántico/codigo_p.txt"):
        self.Pila = Pila.Pila()
        self.MS = MS.MetodosString()

        self.codigo_optimizado = []
        self.valorNoUtilizado(codigo_intermedio)

    # Segundo caso de optimización
    def valorNoUtilizado(self, codigo_intermedio="AnalizadorSemántico/codigo_p.txt"):
        if os.path.exists(codigo_intermedio):
            with open(codigo_intermedio, 'r') as file:
                lineas = file.readlines()
                for linea in lineas:
                    linea = self.MS.stripCadena(linea)
                    if linea.__contains__('assign'):
                        partes = self.MS.splitCadena(linea, ' ')
                        self.Pila.push(partes) # Push de la línea assign dividida en partes
                    elif linea.__contains__('read'):
                        partes = self.MS.splitCadena(linea, ' ')
                        self.Pila.push(partes) # Push de la línea read dividida en partes
                    else:
                        self.codigo_optimizado.append(linea) # Otras líneas se agregan directamente
    
    def contieneTemporal(self, linea: list) -> bool:
        for elemento in linea:
            if elemento.startswith('Temp'):
                return True
        return False
    
    def esVariable(self) -> bool:
        linea = self.Pila.peek()

        if linea[len(linea) - 1]:
            return True
        return False
    


                            