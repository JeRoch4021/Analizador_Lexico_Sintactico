from verificar_int_or_float import VerificadorEnteroDecimal
from conversion_prefija import ConversionPrefija

class CodigoIntermedio:
    
    # Función para generar un archivo de texto con la conversión 
    # del programa a notación prefija
    def generar_notacion_prefija(self, lineas_programa: list[str], tabla_simbolos: dict):
        # Extraemos la función que convierte las expresiones infijas a prefijas
        extraer_metodo = ConversionPrefija()
        # Extraemos la función que nos ayudará a comprobar que del otro lado
        # de la igualdad exista un valor asignado que sea válido
        verificar = VerificadorEnteroDecimal()
        # Lista para almacenar las instrucciones creadas
        codigo_intermedio = []

        palabras_reservadas = {
            "programa", "escribir", "leer", "mostrar", "finprograma"
        }

        # Recorrer cada línea del programa y eliminar los espacios en blanco 
        # e ignorar lineas vacias
        for linea in lineas_programa:
            linea = linea.strip()
            if not linea:
                continue
            
            # Quitar los signos de puntuación "," y ";"
            tokens = linea.replace(",", "").replace(";", "").split()

            # Si la línea es una declaración que empieza con
            # las palabras "int" o "float", comprobaremos su
            # tipo en la tabla de símbolos, es decir, si existe
            # la declaración en la tabla de símbolos
            if tokens[0] in ("int", "float"):
                tipo_variable = tokens[0]

                for token in tokens[1:]:
                    # Eliminamos los caracteres no deseados "," o ";"
                    variable = token.strip(",;")
                    if variable in tabla_simbolos:
                        codigo_intermedio.append(f"{tipo_variable} {variable}")
                # Evita seguir procesando la línea    
                continue
            
            # Si la línea empieza con una palabra reservada,
            # la agregamos a la lista, sin embargo, cada 
            # palabra tiene un registro diferente en la lista
            elif tokens[0].lower() in palabras_reservadas:
                instruccion = tokens[0].lower()

                if instruccion == "programa":
                    codigo_intermedio.append(f"{"programa"}")
                
                if instruccion == "escribir":
                    variable = tokens[1].strip(";")
                    codigo_intermedio.append(f"escribir {variable}")

                if instruccion == "leer":
                    variable = tokens[1].strip(";")
                    codigo_intermedio.append(f"leer {variable}")
                
                if instruccion == "mostrar":
                    variable = tokens[1].strip(";")
                    codigo_intermedio.append(f"mostrar {variable}")

                if instruccion == "finprograma":
                    codigo_intermedio.append(f"{"finprograma"}")

            # tokens = [a, =, 0, b, =, 0, c, =, 0,]
            # Si la línea contiene más de una asignación, 
            # comprobaremos que las asignaciones contengan
            # valores numéricos válidos y no vacíos
            elif tokens.count("=") > 1 and (verificar.asignacion_entero_o_decimal(tokens)):#"0" in tokens or "0.0" in tokens):
                filas = []
                index = 0
                
                # Separamos cada asignación en líneas individuales
                while index < len(tokens):
                    filas.append(tokens[index])
                    
                    # Al momento de encontrar un signo de igualdad "="
                    if tokens[index] == "=":
                        if index + 1 < len(tokens):
                            # Tomamos el valor de la asignación
                            filas.append(tokens[index + 1])

                        # Extraemos los tokens que queremos
                        variable = filas[0]
                        valor = filas[2]
                        # Unimos todo en una sola instrucción de tipo texto
                        union_valor_variable = " ".join(("=", variable, valor))
                        codigo_intermedio.append(union_valor_variable)
                        
                        # Ahora avanzamos con la siguiente asignación dentro 
                        # de la misma línea
                        filas = []
                        index += 2
                        continue

                    index += 1

            # Si se trata de una expresión con una sola asignación única
            elif tokens.count("=") == 1:
                posicion = tokens.index("=")
                variable_izquierda = tokens[posicion-1] if posicion > 0 else None
                expr = tokens[posicion+1:]
                # Obtenemos la expresión infija para luego transformarla
                # a notación prefija
                prefija = extraer_metodo.generar_conversion_prefija(expr)
                prefija_string = " ".join(prefija)
                # Unimos todo en una sola instrucción de tipo texto
                unir_expresion_prefija = " ".join(("=", variable_izquierda, prefija_string))
                codigo_intermedio.append(unir_expresion_prefija)

        return codigo_intermedio
    
    # Función para generar el código P a partir de la notación prefija
    def generar_codigo_p(self, codigo_intermedio: list[str], tabla_simbolos: dict):
        # Extraemos la función que nos ayudará a comprobar que del otro lado
        # de la igualdad exista un valor asignado que sea válido
        verificar = VerificadorEnteroDecimal()
        # Creamos la lista del código p
        codigo_p = []

        palabras_reservadas = {
            "programa", "escribir", "leer", "mostrar", "finprograma"
        }

        # Creamos la lista "pila" para describir como 
        # calcular las expresiones prefijas de acuerdo
        # a su orden
        pila = []
        operadores = {'+', '-', '*', '/'}

        # Recorrer cada línea del programa y eliminar los espacios en blanco 
        # e ignorar lineas vacias
        for linea in codigo_intermedio:
            linea = linea.strip()
            if not linea:
                continue
            
            # Dividir los elementos de la línea por medio de separadores ","
            tokens = linea.split()

            # Si la línea es una declaración que empieza con
            # las palabras "int" o "float", comprobaremos su
            # tipo en la tabla de símbolos, es decir, si existe
            # la declaración en la tabla de símbolos
            if tokens[0] in ("int", "float"):

                for token in tokens[1:]:
                    # Eliminamos los espacios en blanco
                    variable = token.strip()
                    if variable in tabla_simbolos:
                        codigo_p.append(f"loadi {variable}")
                # Evita seguir procesando la línea
                continue
            
            # Si la línea empieza con una palabra reservada,
            # la agregamos a la lista, sin embargo, cada 
            # palabra tiene un registro diferente en la lista
            elif tokens[0].lower() in palabras_reservadas:
                instruccion = tokens[0].lower()

                if instruccion == "programa":
                    continue
                
                if instruccion == "escribir":
                    variable = tokens[1].strip()
                    codigo_p.append(f"write {variable}")

                if instruccion == "leer":
                    variable = tokens[1].strip()
                    codigo_p.append(f"read {variable}")
                
                if instruccion == "mostrar":
                    variable = tokens[1].strip()
                    codigo_p.append(f"show {variable}")

                if instruccion == "finprograma":
                    continue

            # tokens = [=, a, 0]
            # Ahora solo leemos las asignaciones por líneas separadas
            # y comprobamos que el valor numérico sea válido y no vacíos
            elif "=" in tokens and (verificar.notacion_entero_o_decimal(tokens)):
                variable = tokens[1]
                valor = tokens[2]
                # Nos aseguramos de que la instrucción que carguen el valor
                # numérico de la asignación, no se vuelvan a repetir
                if (f"loadc {valor}") not in codigo_p:
                    codigo_p.append(f"loadc {valor}")
                # Unimos todo en una sola instrucción de tipo texto 
                union_valor_variable = " ".join(("assign", variable, valor))
                codigo_p.append(union_valor_variable)

            # Si la asignación contiene la expresión prefija,
            # describiremos la instrucciones para calcularla 
            # de forma ordenada
            elif "=" in tokens:
                variable = tokens[1]
                expresion = tokens[2:]
                contador_temporal = 1

                # Reconstrucción de la expresión de manera inversa
                for token in reversed(expresion):
                    # A través de una pila almacenamos los operandos
                    if token not in operadores:
                        pila.append(token)
                    # Si se trata de un operador
                    else:
                        # Sacamos de la pila los 2 operandos que se
                        # encuentren en el tope
                        operando_izquierdo = pila.pop()
                        operando_derecho = pila.pop()
                        # Registramos el temporal que los reemplazó
                        temp = f"Temp{contador_temporal}"
                        contador_temporal += 1

                        # Si el operando izquierdo es un numero, los volteamos para
                        # guardar el resultado en la variable temporal
                        if operando_izquierdo.replace('.', '', 1).isdigit() and token in ['+', '*']:
                            operando_izquierdo, operando_derecho = operando_derecho, operando_izquierdo
                        
                        # Generamos las instrucciones correspondientes
                        if token == '+':
                            codigo_p.append(f"sum {operando_izquierdo} {operando_derecho}")
                        elif token == '-':
                            codigo_p.append(f"rest {operando_izquierdo} {operando_derecho}")
                        elif token == '*':
                            codigo_p.append(f"mult {operando_izquierdo} {operando_derecho}")
                        elif token == '/':
                            codigo_p.append(f"div {operando_izquierdo} {operando_derecho}")

                        # Guardamos el resultado parcial de la operación
                        codigo_p.append(f"assign {temp} {operando_izquierdo}")
                        pila.append(temp)

                # Agregamos la asignación final
                codigo_p.append(f"assign {variable} {pila.pop()}")

        return codigo_p