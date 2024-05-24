import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import scrolledtext as tkScrolledText
import os
from PIL import Image, ImageTk
from hypertext.parser import run_tests as run_html_tests
from cplusplus.parser import run_tests as run_cpp_tests
from javascript.parser import run_tests as run_js_tests
from pascal.parser import run_tests as run_pascal_tests
from python.main import run_tests as run_python_tests
from sql.parser import run_tests as run_sql_tests

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Final")
        self.configure(bg='#202020')  # Un fondo oscuro que combina con el tema de Valorant

        # Carga y muestra el logo de Valorant
        self.load_logo()

        self.title_label = tk.Label(self, text="Proyecto Final", font=("Helvetica", 16, "bold"), bg='#202020', fg='white')
        self.title_label.pack(pady=(10, 10))

        self.instructions_label = tk.Label(self, text="Seleccione un archivo para analizar:", font=("Helvetica", 10), bg='#202020', fg='white')
        self.instructions_label.pack(pady=(0, 20))

        self.boton_analizar = ttk.Button(self, text="Seleccionar Archivo", command=self.seleccionar_archivo_y_analizar, style='TButton')
        self.boton_analizar.pack(pady=(0, 20), ipadx=10, ipady=5)

        self.minsize(500, 300)
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

    def load_logo(self):
        # Ajusta la ruta según la ubicación de tu archivo
        logo_path = os.path.join(os.path.dirname(__file__), 'icono.png')
        img = Image.open(logo_path)
        img = img.resize((100, 100), Image.LANCZOS)  # Redimensionar la imagen para ajustarla
        photo = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self, image=photo, bg='#202020')
        self.logo_label.image = photo  # Mantener una referencia
        self.logo_label.pack(pady=(20, 10))

    def seleccionar_archivo_y_analizar(self):
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
        if extension == '.cpp':
            resultado = run_cpp_tests(content)
            return 'C++: ' + resultado
        elif extension in ['.html', '.htm']:
            resultado = run_html_tests(content)
            return 'HTML: ' + resultado
        elif extension == '.js':
            resultado = run_js_tests(content)
            return 'JavaScript: ' + resultado
        elif extension == '.pas':
            resultado = run_pascal_tests(content)
            return 'Pascal: ' + resultado
        elif extension == '.py':
            resultado = run_python_tests(content)
            return 'Python: ' + resultado
        elif extension == '.sql':
            resultado = run_sql_tests(content)
            return 'SQL: ' + resultado
        else:
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
