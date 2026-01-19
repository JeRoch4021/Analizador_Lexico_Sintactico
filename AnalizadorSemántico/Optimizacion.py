import os
import MetodosString as MS

class Optimizacion:

    def __init__(self):
        # Variable para almacenar lineas del archivo original
        self.codigo_p = []
        # Variable para almacenar el resultado final
        self.codigo_optimizado = []
        # Diccionario para rastrear el valor que tiene asignado cada variable 
        self.valores_asignados = {}
        # Diccionario para rastrear el valor modificado de cada variable
        self.valores_modificados = {}
        # Llamada a los metodos inventados strip y split
        self.MS = MS.MetodosString()

    def es_un_valor_numerico(self, valor: str) -> bool:
        """Verifica si un valor es una constante numérica"""
        try:
            float(valor)
            return True
        except ValueError:
            return False
        
    def limpiar_valor(self, valor_texto):
        """Limpiar los valores numéricos escritos como texto"""
        try:
            numero = float(valor_texto)

            if numero.is_integer():
                return int(numero)
            return numero
        except ValueError:
            return valor_texto
        
    def algoritmos_optimizacion(self, ruta_codigo_p: str):
        # Abrimos el archivo para leerlo
        try:
            with open(ruta_codigo_p, 'r', ) as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{ruta_codigo_p}'")
            return []
        
        # Tomamos solo las instrucciones que nos interesan
        for linea in lineas:
            linea_limpia = self.MS.stripCadena(linea)
            if linea_limpia and not linea_limpia.startswith("-----"):
                self.codigo_p.append(linea_limpia)
        
        # Separamos cada uno de los elementos que componen la instrucción 
        # para reribirlos como una lista de elementos
        for indice, linea in enumerate(self.codigo_p):
            elementos = self.MS.splitCadena(linea, " ")
            instruccion = elementos[0]

            print(f"Linea {indice}: {elementos}")
            
            if not elementos:
                continue

            if instruccion == "assign":

                if len(elementos) < 3:
                    continue
                
                operando_izquierdo = elementos[1]
                operando_derecho = elementos[2]

                # Si asignamos una variable a un temporal
                if operando_izquierdo in self.valores_asignados and operando_derecho.startswith("Temp"):
                    print(f"[ASSIGN {operando_derecho}] {operando_izquierdo} = {operando_derecho}")
                    self.valores_modificados[operando_izquierdo] = operando_derecho
                    continue

                # Si es una asignación normal
                elif not operando_izquierdo.startswith("Temp"):
                    print(f"[ASSIGN {operando_derecho}] {operando_izquierdo} = {operando_derecho}")
                    self.valores_asignados[operando_izquierdo] = self.limpiar_valor(operando_derecho)
                    continue   

        for linea in self.codigo_p:
            elementos = self.MS.splitCadena(linea, " ")
            
            # Si una de las variables esta modificada su instrucción
            # read debe de ser cancelada
            if elementos[0] == "read" and elementos[1] in self.valores_modificados:
                print(f"[READ OPTIMIZADO] Eliminando linea: {linea}")
                continue

            # Si una instricción es multiplicada por 1 o por 0, la linea
            # "mult" debe de ser cancelada
            elif elementos[0] == "mult":
                operando_izquierdo, operando_derecho = elementos[1], elementos[2]

                obtener_valor_1 = self.valores_asignados.get(operando_izquierdo) if not self.es_un_valor_numerico(operando_izquierdo) else operando_izquierdo
                obtener_valor_2 = self.valores_asignados.get(operando_derecho) if not self.es_un_valor_numerico(operando_derecho) else operando_derecho

                if obtener_valor_1 == 1 or obtener_valor_2 == 1:
                    print(f"[MULT OPTIMIZADO] Eliminando linea: {linea}")
                    continue
                if obtener_valor_1 == 0 or obtener_valor_2 == 0:
                    print(f"[MULT OPTIMIZADO] Eliminando linea: {linea}")
                    continue
            
            # Si una instrucción es sumada con 0, la linea con "sum" debe de
            # ser cancelada
            elif elementos[0] == "sum":
                operando_izquierdo, operando_derecho = elementos[1], elementos[2]
                
                obtener_valor_1 = self.valores_asignados.get(operando_izquierdo) if not self.es_un_valor_numerico(operando_izquierdo) else operando_izquierdo
                obtener_valor_2 = self.valores_asignados.get(operando_derecho) if not self.es_un_valor_numerico(operando_derecho) else operando_derecho

                if obtener_valor_1 == 0 or obtener_valor_2 == 0:
                    print(f"[SUM OPTIMIZADO] Eliminando linea: {linea}")
                    continue
                else:
                    self.codigo_optimizado.append(linea)
            
            # Si una instrucción es dividida con 0, la línea con "div" debe de
            # ser cancelada
            elif elementos[0] == "div":
                operando_izquierdo, operando_derecho = elementos[1], elementos[2]
                
                obtener_valor_1 = self.valores_asignados.get(operando_izquierdo) if not self.es_un_valor_numerico(operando_izquierdo) else operando_izquierdo
                obtener_valor_2 = self.valores_asignados.get(operando_derecho) if not self.es_un_valor_numerico(operando_derecho) else operando_derecho

                if obtener_valor_1 == 0 or obtener_valor_2 == 0:
                    print(f"[DIV OPTIMIZADO] Eliminando linea: {linea}")
                    continue

            else:
                self.codigo_optimizado.append(linea)

        return self.codigo_optimizado
    
    # Generamos el archivo según los datos que guardamos en la pila de 
    # recompilación e imprimimos una notificación de que ya esta listo
    def guardar_codigo_optimizado(self, codigo_optimizado: list[str], archivo_salida: str):
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("----- CÓDIGO P OPTIMIZADO -----\n\n")
                for linea in codigo_optimizado:
                    f.write(linea + '\n')
            print(f"\nCódigo optimizado guardado en '{archivo_salida}'")

if __name__ == "__main__":
    # Aquí solamente definimos las rutas, creamos instancias de la clase
    # ejecutamos el proceso.
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_codigo_p = os.path.join(directorio_actual, "codigo_p.txt")

    optimizacion = Optimizacion()
    codigo_optimizado = optimizacion.algoritmos_optimizacion(archivo_codigo_p)

    ruta_salida = os.path.join(directorio_actual, "codigo_p_optimizado.txt")
    optimizacion.guardar_codigo_optimizado(codigo_optimizado, ruta_salida)