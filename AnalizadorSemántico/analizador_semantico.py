from analizador_lexico import AnalizadorLexico
from conversion_prefija import ConversionPrefija
from codigo_intermedio import CodigoIntermedio
import os

class AnalizadorSemantico:
    
    # Verifica la validez de una asignación y tipos
    def comprobar_asignacion(self, expresion: str, tabla_simbolos: dict):
        extraer_funcion = ConversionPrefija()
        """Verifica la validez de una asignación con comprobación de tipos."""

        if '=' not in expresion:
            return False, [], [], None, None

        # Separar variable izquierda y expresión derecha
        var_izq, expr_der = [parte.strip() for parte in expresion.split('=', 1)]

        # Tokens de la línea para reporte
        tokens_linea = expr_der.replace('(', ' ( ').replace(')', ' ) ').replace('=', ' = ').split()
        tokens_linea = [var_izq, '='] + tokens_linea # Agregar variable y '=' al inicio

        # Verificamos que la variable izquierda exista en la tabla
        if var_izq not in tabla_simbolos:
            # Si es declarada, agregarla temporalmente para permitir la comprobación
            tabla_simbolos[var_izq] = {'tipo': 'desconocido', 'valor': None}

        tipo_izq = tabla_simbolos[var_izq]['tipo']

        # Tokenizar expresión derecha y convertir a prefija
        tokens_der = expr_der.replace('(', ' ( ').replace(')', ' ) ').split()
        expr_prefija = extraer_funcion.generar_conversion_prefija(tokens_der)

        # Comprobar tipo de expresión derecha
        tipo_der = self.comprobar_tipos(expr_prefija, tabla_simbolos)

        if tipo_der is None:
            return False, tokens_linea, expr_prefija, tipo_izq, None
        
        # Si la variable era desconocida, asignamos automáticamente el tipo
        if tipo_izq == "desconocido":
            tipo_izq = tipo_der
            tabla_simbolos[var_izq]['tipo'] = tipo_der

        # Compatibilidad de tipos: exacta, float/int permitido o desconocido asignable
        if tipo_izq == tipo_der or tipo_izq == "desconocido":
            return True, tokens_linea, expr_prefija, tipo_izq, tipo_der
        else:
            return False, tokens_linea, expr_prefija, tipo_izq, tipo_der

    # Comprueba tipos en expresión prefija
    def comprobar_tipos(self, expresion_prefija: list[str], tabla_simbolos: dict) -> str | None:
        """Verifica la expresión prefija y devuelve el tipo resultante si es válido."""
        pila_tipos = []
        operadores = {'+', '-', '*', '/'}

        for token in reversed(expresion_prefija):
            if token in operadores:
                # Se necesitan dos operandos para el operador
                if len(pila_tipos) < 2:
                    return None
                tipo1 = pila_tipos.pop()
                tipo2 = pila_tipos.pop()
                # Regla de combinación de tipos
                if tipo1 == tipo2:
                    pila_tipos.append(tipo1)
                elif (tipo1, tipo2) in [('int', 'float'), ('float', 'int')]:
                    pila_tipos.append('float')
                else:
                    return None # Tipos incompatibles
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
    # Crea una instancia del analizador léxico
    analizador_lexico = AnalizadorLexico()
    # Crea una instancia del código intermedio (funciones)
    codigo_intermedio = CodigoIntermedio()
    # Crea una instancia del analizador semántico
    analizador_semantico = AnalizadorSemantico()
    # Llamada a la función distribuir_tokens_en_tablas del analizador_lexico
    # para obtener los datos de algunas de las tabla de información
    tabla_tokens, tokens_linea, tabla_simbolos, errores = analizador_lexico.distribuir_tokens_en_tablas()

    ruta_carpeta = "AnalizadorSemántico"
    archivo_programa = os.path.join(ruta_carpeta, "programa_ejemplo_No7.txt")
    archivo_resultados_semanticos = os.path.join(ruta_carpeta, "resultado_semantico.txt")
    archivo_notacion = os.path.join(ruta_carpeta, "notacion_prefija.txt")
    archivo_codigo_p = os.path.join(ruta_carpeta, "codigo_p.txt")

    # Instrucción para leer el programa fuente
    with open(archivo_programa, "r") as f:
        lineas_programa = f.readlines()

    # Extracción de la función para recibir el archivo del programa fuente
    # escrito de forma prefija 
    notacion_prefija = codigo_intermedio.generar_notacion_prefija(lineas_programa, tabla_simbolos)

    # Creación del archivo con la notación prefija
    with open(archivo_notacion, "w") as out_prefija:
        out_prefija.write("----- NOTACIÓN PREFIJA -----\n\n")
        # Escribir cada instrucción generada
        for item in notacion_prefija:
            # Escribir la instrucción en forma de tupla
            if isinstance(item, tuple):
                var, expr = item
                out_prefija.write(f"= {var} {expr}\n")
            else:
                # Escribir solo la instrucción (en caso de que todo esté unido)
                out_prefija.write(f"{item}\n")

    print(f"Archivo generado: {archivo_notacion}")

    # Extracción de la función para recibir el archivo escrito de forma
    # prefija y obtener el archivo del código p
    codigo_p = codigo_intermedio.generar_codigo_p(notacion_prefija, tabla_simbolos)

    # Creación del archivo código p
    with open(archivo_codigo_p, "w") as out_cp:
        out_cp.write("----- CÓDIGO P -----\n\n")
        # Escribir cada instrucción generada
        for item in codigo_p:
            # Escribir la instrucción en forma de tupla
            if isinstance(item, tuple):
                var, expr = item
                out_cp.write(f"= {var} {expr}\n")
            else:
                # Escribir solo la instrucción (en caso de que todo esté unido)
                out_cp.write(f"{item}\n")

    print(f"Archivo generado: {archivo_codigo_p}")

    with open(archivo_programa, "r") as expresiones, open(archivo_resultados_semanticos, "w") as salida:
        salida.write("-----REPORTE SEMÁNTICO-----\n\n")
        for linea in expresiones:
            linea = linea.strip()
            if not linea or '=' not in linea:
                continue

            # Reemplazar guiones largos por normales y eliminar punto y coma
            linea = linea.replace('–', '-').rstrip(';')

            # Separar múltiples variables si hay declaración con tipo
            if linea.startswith(('float ', 'int ')):
                tipo, resto = linea.split(' ', 1)
                variables = resto.split(',')
                for var in variables:
                    asign = var.strip()
                    if '=' not in asign:
                        continue
                    # Comprobar asignación y tipos
                    resultado, tokens, expr_prefija, tipo_izq, tipo_der = analizador_semantico.comprobar_asignacion(asign, tabla_simbolos)

                    # Guardar reporte en archivo
                    salida.write(f"Tokens: {tokens}\n")
                    salida.write(f"Prefija derecha: {expr_prefija}\n")
                    if tipo_der is not None and tipo_izq != tipo_der:
                        var_izq = asign.split('=')[0].strip()
                        salida.write(f"Error de tipos: {var_izq} ({tipo_izq}) = expr ({tipo_der})\n")
                    salida.write(f"Resultado de la asignación: {resultado}\n\n")
                    salida.write("-" * 50 + "\n")
            else:
                # Caso sin declaración explícita de tipo
                resultado, tokens, expr_prefija, tipo_izq, tipo_der = analizador_semantico.comprobar_asignacion(linea, tabla_simbolos)
                salida.write(f"Tokens: {tokens}\n")
                salida.write(f"Prefija derecha: {expr_prefija}\n")
                if tipo_der is not None and tipo_izq != tipo_der:
                    var_izq = linea.split('=')[0].strip()
                    salida.write(f"Error de tipos: {var_izq} ({tipo_izq}) = expr ({tipo_der})\n")
                salida.write(f"Resultado de la asignación: {resultado}\n\n")
                salida.write("-" * 50 + "\n")

    print(f"Archivo de resultados generado: {archivo_resultados_semanticos}")