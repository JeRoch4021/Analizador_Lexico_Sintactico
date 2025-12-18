# Elimina los espacios en blanco de una cadena
class MetodosString:
    def stripCadena(self, cadena: str) -> str:
        caracteres_no_validos = " \n\t\r"
        inicio = 0
        fin = len(cadena) - 1

        while inicio <= fin and cadena[inicio] in caracteres_no_validos:
            inicio += 1

        while fin >= inicio and cadena[fin] in caracteres_no_validos:
            fin -= 1
        
        return cadena[inicio:fin + 1] # Devuelve una subcadena desde el inicio hasta el fin + 1
    
    def splitCadena(self, cadena: str, separador: str) -> list:
        resultado = []
        palabra_actual = ""
        
        for caracter in cadena:
            if caracter == separador:
                resultado.append(palabra_actual)
                palabra_actual = ""
            else:
                palabra_actual += caracter
        
        resultado.append(palabra_actual)  # Agrega la última palabra
        return resultado