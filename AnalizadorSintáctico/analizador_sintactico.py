

class AnaliadorSintactico:
    def __init__(self, lexico):
        self.lexico = lexico
    
    def imprimir_tokens(self):
        while True:
            token = self.lexico.scanner()
            if token is None:
                break
            print(token)

    
    
