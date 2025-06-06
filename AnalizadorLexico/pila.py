class Pila:

    def __init__(self):
        self.inicio = None
        self.fin = None
        self.tamanio = 0
    
    class Nodo:

        def __init__(self, dato):
            self.dato = dato
            self.der = None
            self.izq = None


        def __str__(self):
            return str(self.dato)
    
    def push(self, dato):
        # Crea un nuevo nodo con el dato a insertar
        nuevo_nodo = self.Nodo(dato)
        if self.inicio is None:
            # Si la pila está vacía, el nuevo nodo será el inicio y el fin
            self.inicio = nuevo_nodo
            self.fin = nuevo_nodo
        else:
            # Inserta al inicio, ajustando los enlaces entre nodos
            nuevo_nodo.der = self.inicio
            self.inicio.izq = nuevo_nodo
            self.inicio = nuevo_nodo
        self.tamanio += 1
    
    def popDat(self):
        dato = None
        if self.inicio is not None:
            if self.tamanio == 1:
                # Si hay un solo nodo, extrae su dato y limpia la pila
                dato = self.inicio.dato
                self.inicio = None
                self.fin = None
            else:
                # Extrae solo el dato del nodo superior (inicio)
                dato = self.inicio.dato
                self.inicio = self.inicio.der
                self.inicio.izq = None
            self.tamanio -= 1
        # Devuelve solo el dato del nodo, no el nodo completo
        return dato
