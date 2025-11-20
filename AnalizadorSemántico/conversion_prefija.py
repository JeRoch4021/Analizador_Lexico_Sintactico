from pila import Pila

class ConversionPrefija:

    # Función que devuelve la precedencia de los operadores
    def precedencia(self, operador: str) -> int:
        if operador in ('+', '-'):
            return 1 # Suma y resta tienen precedencia 1
        elif operador in ('*', '/'):
            return 2 # Multiplicación y división tienen precedencia 2
        return 0 # Otros símbolos (o no operadores) tienen precedencia 0

    # Convierte una lista de tokens a notación prefija
    def generar_conversion_prefija(self, tokens: list[str]) -> list[str]:
        """Convierte una lista de tokens en notación prefija."""
        pila = Pila() # Pila para operadores
        resultado = [] # Lista de resultado prefija
        operadores = set(['+', '-', '*', '/']) # Conjunto de operadores válidos

        # Se recorre la lista de tokens de derecha a izquierda
        for token in reversed(tokens):
            if token == ')':
                pila.push(token)  # Guardamos el paréntesis derecho
            elif token == '(':
                # Sacar operadores hasta encontrar un paréntesis derecho
                while not pila.isEmpty() and pila.peek() != ')':
                    resultado.append(pila.pop())
                if not pila.isEmpty():
                    pila.pop()  # Quitar el paréntesis derecho
            elif token in operadores:
                # Sacar operadores de mayor o igual precedencia antes de agregar
                while (not pila.isEmpty() and pila.peek() in operadores 
                       and self.precedencia(token) < self.precedencia(pila.peek())):
                    resultado.append(pila.pop())
                pila.push(token) # Agregar operador actual a la pila
            else:
                # Si es un operando (número o variable)
                resultado.append(token)
        # Vaciar cualquier operador restante en la pila
        while not pila.isEmpty():
            resultado.append(pila.pop())
        return resultado[::-1]  # Invertir la lista para obtener notación prefija correcta