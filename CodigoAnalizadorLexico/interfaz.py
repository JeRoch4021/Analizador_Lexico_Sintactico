import tkinter as tk
from tkinter import filedialog, scrolledtext
from analizador import AnalizadorLexico

class InterfazLexica:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")
        self.root.geometry("800x600")
        self.analizador = AnalizadorLexico()
        self._crear_widgets()

    def _crear_widgets(self):
        self.btn_cargar = tk.Button(self.root, text="Cargar archivo", command=self.cargar_archivo)
        self.btn_cargar.pack(pady=10)

        self.texto_salida = scrolledtext.ScrolledText(self.root, width=100, height=30, font=("Courier", 10))
        self.texto_salida.pack(padx=10, pady=10)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if ruta:
            with open(ruta, 'r') as f:
                contenido = f.read()
                self.analizador.analizar_contenido(contenido)
                self.mostrar_resultados()

    def mostrar_resultados(self):
        self.texto_salida.delete(1.0, tk.END)
        reporte = self.analizador.obtener_reporte()

        self.texto_salida.insert(tk.END, "TOKENS VÁLIDOS:\n")
        for token, tipo, linea in reporte['tokens']:
            self.texto_salida.insert(tk.END, f"Línea {linea}: {token} → {tipo}\n")

        self.texto_salida.insert(tk.END, "\nPALABRAS RESERVADAS:\n")
        for palabra in reporte['reservadas']:
            self.texto_salida.insert(tk.END, f"  - {palabra}\n")

        self.texto_salida.insert(tk.END, "\nIDENTIFICADORES:\n")
        for simbolo in reporte['simbolos']:
            self.texto_salida.insert(tk.END, f"  - {simbolo}\n")

        self.texto_salida.insert(tk.END, "\nERRORES LÉXICOS:\n")
        for error, linea in reporte['errores']:
            self.texto_salida.insert(tk.END, f"Línea {linea}: {error}\n")

# Punto de entrada
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLexica(root)
    root.mainloop()