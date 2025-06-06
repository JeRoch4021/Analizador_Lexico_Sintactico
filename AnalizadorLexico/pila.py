class Pila:

    def __init__(self):
        self.inicio = None
        self.fin = None
        self.tamanio = 0
    
    
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


    def pop(self):
        # Nodo vacío temporal por si la pila está vacía
        borrado = self.Nodo(None)
        if self.inicio is not None:
            if self.tamanio == 1:
                # Si solo hay un nodo, se elimina y se reinicia la pila
                borrado = self.inicio
                self.inicio = None
                self.fin = None
                self.tamanio = 0
            else:
                # Elimina el nodo del tope (inicio)
                borrado = self.inicio
                self.inicio.izq = None
                self.inicio = self.inicio.der
                self.tamanio -= 1
        # Devuelve el nodo completo eliminado (no solo el dato)
        return borrado
    
    
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
    
    
    def peek(self):
        if self.inicio is not None:
            # Devuelve el dato del nodo en el tope (sin quitarlo)
            return self.inicio.dato
        # Si la pila está vacía
        return None
    
    
    def imprimir(self):
        salida = "Lista(" + str(self.size()) + "): {"
        cursor = self.inicio
        while cursor is not None:
            salida += str(cursor.dato) + ", "
            # Avanza al siguiente nodo
            cursor = cursor.der
        # Devuelve cadena que representa visualmente la pila
        return salida + "\b}"
    

    class Nodo:

        def __init__(self, dato):
            self.dato = dato
            self.der = None
            self.izq = None


        def __str__(self):
            return str(self.dato)
