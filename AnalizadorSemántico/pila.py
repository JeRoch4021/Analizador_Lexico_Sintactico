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
        nuevo_nodo = self.Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo_nodo
            self.fin = nuevo_nodo
        else:
            nuevo_nodo.der = self.inicio
            self.inicio.izq = nuevo_nodo
            self.inicio = nuevo_nodo
        self.tamanio += 1

    def popDat(self):
        dato = None
        if self.inicio is not None:
            if self.tamanio == 1:
                dato = self.inicio.dato
                self.inicio = None
                self.fin = None
            else:
                dato = self.inicio.dato
                self.inicio = self.inicio.der
                self.inicio.izq = None
            self.tamanio -= 1
        return dato
    
    # 🔹 Métodos necesarios para conversionPrefija
    def pop(self):
        return self.popDat()
    
    def peek(self):
        return self.inicio.dato if self.inicio is not None else None
    
    def isEmpty(self):
        return self.tamanio == 0
