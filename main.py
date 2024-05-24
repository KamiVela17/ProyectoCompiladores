import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import scrolledtext as tkScrolledText
import os

# Importaciones de los módulos de prueba
from hypertext.parser import run_tests as run_html_tests
from cplusplus.parser import run_tests as run_cpp_tests
from javascript.parser import run_tests as run_js_tests
from pascal.parser import run_tests as run_pascal_tests
from python.parser import run_tests as run_python_tests
from sql.parser import run_tests as run_sql_tests

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Detector de Lenguajes de Programación")
        self.configure(bg='#333333')

        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Courier New', 12), padding=10)
        self.style.configure('TLabel', font=('Courier New', 14), background='#333333', foreground='white')

        self.title_label = ttk.Label(self, text="Seleccione un archivo para determinar su lenguaje de programación")
        self.title_label.pack(pady=(20, 10), padx=20)

        self.boton_analizar = ttk.Button(self, text="Seleccionar Archivo", command=self.detectar_lenguaje)
        self.boton_analizar.pack(pady=(10, 20), padx=20)

        self.minsize(600, 200)
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

    def detectar_lenguaje(self):
        filepath = tkFileDialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Todos los archivos", "*.*"),),
            parent=self
        )
        if filepath:
            extension = os.path.splitext(filepath)[1].lower()
            with open(filepath, 'r', encoding='utf-8') as file:
                file_content = file.read()
            resultado = self.identificar_lenguaje(extension, file_content)
            self.mostrar_resultados(resultado)

    def identificar_lenguaje(self, extension, content):
        match extension:
            case '.cpp':
                resultado = run_cpp_tests(content)
                return 'C++: ' + resultado
            case '.html' | '.htm':
                resultado = run_html_tests(content)
                return 'HTML: ' + resultado
            case '.js':
                resultado = run_js_tests(content)
                return 'JavaScript: ' + resultado
            case '.pas':
                resultado = run_pascal_tests(content)
                return 'Pascal: ' + resultado
            case '.py':
                resultado = run_python_tests(content)
                return 'Python: ' + resultado
            case '.sql':
                resultado = run_sql_tests(content)
                return 'SQL: ' + resultado
            case _:
                return 'Desconocido'

    def mostrar_resultados(self, resultado):
        result_window = tk.Toplevel(self)
        result_window.title("Resultados de Análisis")
        result_window.configure(bg='black')
        result_window.geometry("700x400")

        text_area = tkScrolledText.ScrolledText(result_window, wrap=tk.WORD, font=('Courier New', 12), background='black', foreground='green')
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, resultado)
        text_area.config(state='disabled')

if __name__ == '__main__':
    app = Application()
    app.mainloop()
