class VerificadorEnteroDecimal:

    # Función para verificar que el valor se trate de un número entero válido
    # o si es "0"
    def es_entero(self, token):
        return token.isdigit() and not token.startswith("0") or token == "0"
    
    # Función para verificar que el valor se trate de un número decimal válido
    # Tomando el punto y checar que los números de ambos extremos sean enteros
    def es_decimal(self, token):
        partes = token.split(".")
        return len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit()
    
    # Función para movernos a través de la asignación, con la cual
    # comprobaremos que se trata efectivamente de un valor numérico 
    # válido y no vacío
    def asignacion_entero_o_decimal(self, tokens):
        for index, token in enumerate(tokens):
            if token == "=":
                if index + 1 < len(tokens):
                    siguente = tokens[index + 1]

                    if self.es_entero(siguente) or self.es_decimal(siguente):
                        return True
                    else:
                        return False
    
    # Función para movernos a través de la asignación prefija
    # para comprobar que el valor numérico sea válido y no vacío, además la
    # usaremos para separar las expresiones prefijas de las asignaciones prefijas,
    # pues así evitaremos confusión por los elementos que están después del signo
    # de igualdad
    def notacion_entero_o_decimal(self, tokens):
        for index, token in enumerate(tokens):
            if token == "=":
                if index + 2 < len(tokens):
                    siguente = tokens[index + 2]

                    if self.es_entero(siguente) or self.es_decimal(siguente):
                        return True
                    else:
                        return False