class AFN:

    
    def __init__(self, alfabeto):
        self.estados = set()
        self.alfabeto = alfabeto
        self.estado_inicial = None
        self.estados_aceptacion = set()
        self.transiciones = {}
        

    def agregar_estado(self, estado, estado_inicial=False, estado_final=False):
        self.estados.add(estado)
        if estado_inicial:
            self.estado_inicial = estado
        if estado_final:
            self.estados_aceptacion.add(estado)


    def agregar_transicion(self, desde, simbolo, hacia):
        if desde not in self.transiciones:
            self.transiciones[desde] = {}
        if simbolo not in self.transiciones[desde]:
            self.transiciones[desde][simbolo] = []
        self.transiciones[desde][simbolo].append(hacia)


    def procesar(self, cadena):
        estados_actuales = [self.estado_inicial]
        for simbolo in cadena:
            nuevos_estados = []
            for estado in estados_actuales:
                if estado in self.transiciones and simbolo in self.transiciones[estado]:
                    nuevos_estados += self.transiciones[estado][simbolo]
            estados_actuales = nuevos_estados
        return any(estado in self.estados_aceptacion for estado in estados_actuales)
    

def crear_afn_identificador():
    afn = AFN(alfabeto="abcdefghijklmnopqrstuvwxyz")
    afn.agregar_estado('q0', estado_inicial=True)
    afn.agregar_estado('q1', estado_final=True)
    for letra in afn.alfabeto:
        afn.agregar_transicion('q0', letra, 'q1')
        afn.agregar_transicion('q1', letra, 'q1')
    return afn


def crear_afn_binario():
    afn = AFN(alfabeto="01B")
    afn.agregar_estado('q0', estado_inicial=True)
    afn.agregar_estado('q1')
    afn.agregar_estado('q2', estado_final=True)
    for b in '01':
        afn.agregar_transicion('q0', b, 'q0')
    afn.agregar_transicion('q0', 'B', 'q2')
    return afn


def crear_afn_octal():
    afn = AFN(alfabeto="01234567O")
    afn.agregar_estado('q0', estado_inicial=True)
    afn.agregar_estado('q1')
    afn.agregar_estado('q2', estado_final=True)
    for o in '01234567':
        afn.agregar_transicion('q0', o, 'q0')
    afn.agregar_transicion('q0', 'O', 'q2')
    return afn


def crear_afn_hexadecimal():
    afn = AFN(alfabeto="0123456789ABCDEF")
    afn.agregar_estado('q0', estado_inicial=True)
    afn.agregar_estado('q1')
    afn.agregar_estado('q2', estado_final=True)
    for h in '0123456789ABCDEF':
        afn.agregar_transicion('q0', h, 'q0')
    afn.agregar_transicion('q0', 'X', 'q2')
    return afn


def crear_afn_caracter_simple():
    afn = AFN(alfabeto=";=+-*()/,")
    afn.agregar_estado('q0', estado_inicial=True)
    afn.agregar_estado('q1', estado_final=True)
    for c in ";=+-*()/,":
        afn.agregar_transicion('q0', c, 'q1')
    return afn


palabras_reservadas = {
    'programa', 'binario', 'octal', 'hexadecimal', 'leer', 'escribir', 'finprograma'
}