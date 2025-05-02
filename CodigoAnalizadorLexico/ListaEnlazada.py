# Programa para crear una lista doblemente enlazada

class ListaEnlazada:
    def __init__(self):
        self.inicio = None
        self.fin = None
        self.tamanio = 0

    def getInicio(self):
        if self.inicio is not None:
            return self.inicio
    
    def getFin(self):
        if self.fin is not None:
            return self.fin
    
    def size(self):
        return self.tamanio

    def agregar(self, dato):
        nuevo_nodo = self.Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo_nodo
            self.fin = nuevo_nodo
        else:
            nuevo_nodo.der = self.inicio
            self.inicio.izq = nuevo_nodo
            self.inicio = nuevo_nodo
        self.tamanio += 1

    def eliminar(self):
        borrado = self.Nodo(None)
        if self.inicio is not None:
            if self.size() == 1:
                borrado = self.inicio
                self.inicio = None
                self.fin = None
                tamanio = 0
            else:
                borrado = self.inicio
                self.inicio = self.inicio.der
                self.inicio.izq = None
                tamanio -= 1
        return borrado

    def eliminarUltimo(self):
        borrado = self.Nodo(None)
        if self.fin is not None:
            if self.size() == 1:
                borrado = self.fin
                self.inicio = None
                self.fin = None
                tamanio = 0
            else:
                borrado = self.fin
                self.fin = self.fin.izq
                self.fin.der = borrado.izq = None
                tamanio -= 1
        return borrado

    def imprimir(self):
        salida = "Lista(" + self.size() + "): {"
        cursor = self.inicio
        while cursor is not None:
            salida += str(cursor.dato) + ", "
            cursor = cursor.der
        return salida + "\b}"

    class Nodo:
        # Atributos de la clase Nodo
        der = None # Siguiente nodo
        izq = None # Nodo anterior

         # Constructor de la clase Nodo
        def __init__(self, dato):
            self.dato = dato
            

        def __str__(self):
            return str(self.dato)
