class AFN:
    
    
    def __init__(self, alfabeto):
        self.estados = set()
        # Alfabeto permitido (símbolos válidos)
        self.alfabeto = alfabeto
        self.estado_inicial = None
        self.estados_aceptacion = set()
        # Diccionario para almacenar transiciones: {estado: {simbolo: [estados_destino]}}
        self.transiciones = {}
        

    def agregar_estado(self, estado, es_inicial=False, es_aceptacion=False):
        self.estados.add(estado)
        if es_inicial:
            self.estado_inicial = estado
        if es_aceptacion:
            self.estados_aceptacion.add(estado)


    def agregar_transicion(self, desde, simbolo, hacia):
        if desde not in self.transiciones:
            # Inicializa si no existe el estado
            self.transiciones[desde] = {}
        if simbolo not in self.transiciones[desde]:
            # Inicializa la lista de destino
            self.transiciones[desde][simbolo] = []
        # Agrega transición
        self.transiciones[desde][simbolo].append(hacia)


    def procesar(self, cadena):
        estados_actuales = [self.estado_inicial]
        for simbolo in cadena:
            nuevos_estados = []
            for estado in estados_actuales:
                if estado in self.transiciones and simbolo in self.transiciones[estado]:
                    # Acumula estados de destino
                    nuevos_estados += self.transiciones[estado][simbolo]
            # Actualiza los estados actuales
            estados_actuales = nuevos_estados
        # Verifica la aceptación
        return any(estado in self.estados_aceptacion for estado in estados_actuales)
    

def crear_afn_identificador():
    afn = AFN(alfabeto="abcdefghijklmnopqrstuvwxyz")
    afn.agregar_estado('q0', es_inicial=True)
    afn.agregar_estado('q1', es_aceptacion=True)
    for letra in afn.alfabeto:
        afn.agregar_transicion('q0', letra, 'q1')
        afn.agregar_transicion('q1', letra, 'q1')
    return afn


def crear_afn_binario():
    afn = AFN(alfabeto="01B")
    afn.agregar_estado('q0', es_inicial=True)
    afn.agregar_estado('q1')
    afn.agregar_estado('q2', es_aceptacion=True)
    for binario in '01':
        afn.agregar_transicion('q0', binario, 'q0')
    afn.agregar_transicion('q0', 'B', 'q2')
    return afn


def crear_afn_octal():
    afn = AFN(alfabeto="01234567O")
    afn.agregar_estado('q0', es_inicial=True)
    afn.agregar_estado('q1')
    afn.agregar_estado('q2', es_aceptacion=True)
    for octal in '01234567':
        afn.agregar_transicion('q0', octal, 'q0')
    afn.agregar_transicion('q0', 'O', 'q2')
    return afn


def crear_afn_hexadecimal():
    afn = AFN(alfabeto="0123456789ABCDEF")
    afn.agregar_estado('q0', es_inicial=True)
    afn.agregar_estado('q1')
    afn.agregar_estado('q2', es_aceptacion=True)
    for hexadecimal in '0123456789ABCDEF':
        afn.agregar_transicion('q0', hexadecimal, 'q0')
    afn.agregar_transicion('q0', 'X', 'q2')
    return afn


def crear_afn_caracter_simple():
    afn = AFN(alfabeto=";=+-*()/,")
    afn.agregar_estado('q0', es_inicial=True)
    afn.agregar_estado('q1', es_aceptacion=True)
    for caracter_simple in ";=+-*()/,":
        afn.agregar_transicion('q0', caracter_simple, 'q1')
    return afn


palabras_reservadas = {
    'programa', 'binario', 'octal', 'hexadecimal', 'leer', 'escribir', 'finprograma'
}