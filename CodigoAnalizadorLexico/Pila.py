class Pila:
    def __init__(self):
        self.inicio = None
        self.fin = None
        self.tamanio = 0

    def size(self):
        return self.tamanio
    
    def push(self, dato):
        nuevo_nodo = self.Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo_nodo
            self.fin = nuevo_nodo
        else:
            nuevo_nodo.der = self.inicio
            self.inicio.izq = nuevo_nodo
            self.inicio = nuevo_nodo
        self.tamanio += 1

    def pop(self):
        borrado = self.Nodo(None)
        if self.inicio is not None:
            if self.size() == 1:
                borrado = self.inicio
                self.inicio = None
                self.fin = None
                self.tamanio = 0
            else:
                borrado = self.inicio
                self.inicio.izq = None
                self.inicio = self.inicio.der
                self.tamanio -= 1
        return borrado
    
    def popDat(self):
        dato = None
        if self.inicio is not None:
            if self.size() == 1:
                dato = self.inicio.dato
                self.inicio = None
                self.fin = None
            else:
                dato = self.inicio.dato
                self.inicio = self.inicio.der
                self.inicio.izq = None
            self.tamanio -= 1
        return dato
    
    def peek(self):
        if self.inicio is not None:
            return self.inicio.dato
        return None
    
    def imprimir(self):
        salida = "Lista(" + str(self.size()) + "): {"
        cursor = self.inicio
        while cursor is not None:
            salida += str(cursor.dato) + ", "
            cursor = cursor.der
        return salida + "\b}"

    class Nodo:
        def __init__(self, dato):
            self.dato = dato
            self.der = None
            self.izq = None

        def __str__(self):
            return str(self.dato)
