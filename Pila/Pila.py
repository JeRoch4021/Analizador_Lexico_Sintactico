from Pila.Nodo import Nodo

class Pila:
    def __init__(self):
        self.inicio = None
        self.fin = None
        self.tamanio = 0
    
    def isEmpty(self):
        return self.tamanio == 0
    
    def push(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo_nodo
            self.fin = nuevo_nodo
        else:
            self.fin.siguiente = nuevo_nodo
            self.fin = self.fin.siguiente
        self.tamanio += 1
    
    def pop(self):
        borrado = Nodo(None)
        if self.inicio is not None:
            if self.tamanio == 1:
                borrado = self.inicio
                self.inicio = self.fin = None
                self.tamanio = 0
            elif self.tamanio == 2:
                borrado = self.fin
                self.fin = self.inicio
                self.inicio.siguiente = None
                self.tamanio = 1
            else:
                cursor = self.inicio
                while cursor.siguiente is not self.fin:
                    cursor = cursor.siguiente
                borrado = self.fin
                self.fin = cursor
                cursor.siguiente = None
                self.tamanio -= 1
        return borrado
    
    def peek(self):
        if self.inicio is not None:
            return self.fin.valor
        return None
    
    def __str__(self):
        cadena = "Pila(" + str(self.tamanio) + "): { "
        cursor = self.inicio
        while cursor is not None:
            if cursor is self.fin:
                cadena += cursor.__str__() + " }"
                break
            cadena += cursor.__str__() + ", "
            cursor = cursor.siguiente
        return str(cadena)
