from pila import Pila
from analizador_lexico import AnalizadorLexico
import os

class AnalizadorSemantico:

    def precedencia(self, operador: str) -> int:
        if operador in ('+', '-'):
            return 1
        elif operador in ('*', '/'):
            return 2
        return 0

    def conversionPrefija(self, tokens: list[str]) -> list[str]:
        """Convierte una lista de tokens en notación prefija."""
        pila = Pila()
        resultado = []
        operadores = set(['+', '-', '*', '/'])

        for token in reversed(tokens):
            if token in operadores:
                while (not pila.isEmpty() and pila.peek() in operadores 
                       and self.precedencia(token) <= self.precedencia(pila.peek())):
                    resultado.append(pila.pop())
                pila.push(token)
            else:
                # Si es un operando (número o variable)
                resultado.append(token)
        while not pila.isEmpty():
            resultado.append(pila.pop())
        return resultado[::-1]  # invertir para obtener prefija

    def comprobar_asignacion(self, expresion: str, tabla_simbolos: dict):
        """Verifica la validez de una asignación con comprobación de tipos."""

        if '=' not in expresion:
            return False, [], [], None, None

        var_izq, expr_der = [parte.strip() for parte in expresion.split('=', 1)]

        # Tokens de la línea para reporte
        tokens_linea = expr_der.replace('(', ' ( ').replace(')', ' ) ').replace('=', ' = ').split()
        tokens_linea = [var_izq, '='] + tokens_linea

        # Verificamos que la variable izquierda exista en la tabla
        if var_izq not in tabla_simbolos:
            # Si es declarada, agregarla temporalmente para permitir la comprobación
            tabla_simbolos[var_izq] = {'tipo': 'desconocido', 'valor': None}

        tipo_izq = tabla_simbolos[var_izq]['tipo']

        # Tokenizamos la expresión derecha
        tokens_der = expr_der.replace('(', ' ( ').replace(')', ' ) ').split()
        expr_prefija = self.conversionPrefija(tokens_der)

        # Comprobamos tipos
        tipo_der = self.comprobar_tipos(expr_prefija, tabla_simbolos)

        if tipo_der is None:
            return False, tokens_linea, expr_prefija, tipo_izq, None

        if tipo_izq == tipo_der or (tipo_izq == "float" and tipo_der == "int") or tipo_izq == "desconocido":
            return True, tokens_linea, expr_prefija, tipo_izq, tipo_der
        else:
            return False, tokens_linea, expr_prefija, tipo_izq, tipo_der

    def comprobar_tipos(self, expresion_prefija: list[str], tabla_simbolos: dict) -> str | None:
        """Verifica la expresión prefija y devuelve el tipo resultante si es válido."""
        pila_tipos = []
        operadores = {'+', '-', '*', '/'}

        for token in reversed(expresion_prefija):
            if token in operadores:
                if len(pila_tipos) < 2:
                    return None
                tipo1 = pila_tipos.pop()
                tipo2 = pila_tipos.pop()
                if tipo1 == tipo2:
                    pila_tipos.append(tipo1)
                elif (tipo1, tipo2) in [('int', 'float'), ('float', 'int')]:
                    pila_tipos.append('float')
                else:
                    return None
            else:
                # Operando: variable o número
                if token in tabla_simbolos:
                    tipo_operando = tabla_simbolos[token]['tipo']
                    # Si tipo desconocido, deducir del literal
                    if tipo_operando == 'desconocido':
                        if '.' in token and token.replace('.', '').isdigit():
                            tipo_operando = 'float'
                        elif token.isdigit():
                            tipo_operando = 'int'
                        else:
                            tipo_operando = 'desconocido'
                    pila_tipos.append(tipo_operando)
                elif token.replace('.', '', 1).isdigit():
                    pila_tipos.append('float' if '.' in token else 'int')
                else:
                    return None

        return pila_tipos[0] if len(pila_tipos) == 1 else None


if __name__ == "__main__":
    analizador_lexico = AnalizadorLexico()
    tabla_tokens, tokens_linea, tabla_simbolos, errores = analizador_lexico.distribuir_tokens_en_tablas()

    archivo_expresiones = "AnalizadorSemántico/programa_ejemplo_4.txt"
    ruta_carpeta = "AnalizadorSemántico"
    archivo_salida = "resultado_semantico.txt"
    ruta_completa = os.path.join(ruta_carpeta, archivo_salida)

    analizador_semantico = AnalizadorSemantico()

    with open(archivo_expresiones, "r") as expresiones, open(ruta_completa, "w") as salida:
        salida.write("-----Reporte semántico------\n\n")
        for linea in expresiones:
            linea = linea.strip()
            if not linea or '=' not in linea:
                continue

            linea = linea.replace('–', '-').rstrip(';')

            if linea.startswith(('float ', 'int ')):
                tipo, resto = linea.split(' ', 1)
                variables = resto.split(',')
                for var in variables:
                    asign = var.strip()
                    if '=' not in asign:
                        continue
                    resultado, tokens, expr_prefija, tipo_izq, tipo_der = analizador_semantico.comprobar_asignacion(asign, tabla_simbolos)

                    salida.write(f"Tokens: {tokens}\n")
                    salida.write(f"Prefija derecha: {expr_prefija}\n")
                    if tipo_der is not None and tipo_izq != tipo_der:
                        var_izq = asign.split('=')[0].strip()
                        salida.write(f"Error de tipos: {var_izq} ({tipo_izq}) = expr ({tipo_der})\n")
                    salida.write(f"Resultado de la asignación: {resultado}\n\n")
                    salida.write("-" * 50 + "\n")
            else:
                resultado, tokens, expr_prefija, tipo_izq, tipo_der = analizador_semantico.comprobar_asignacion(linea, tabla_simbolos)
                salida.write(f"Tokens: {tokens}\n")
                salida.write(f"Prefija derecha: {expr_prefija}\n")
                if tipo_der is not None and tipo_izq != tipo_der:
                    var_izq = linea.split('=')[0].strip()
                    salida.write(f"Error de tipos: {var_izq} ({tipo_izq}) = expr ({tipo_der})\n")
                salida.write(f"Resultado de la asignación: {resultado}\n\n")
                salida.write("-" * 50 + "\n")

    print(f"Archivo de resultados generado: {archivo_salida}")



