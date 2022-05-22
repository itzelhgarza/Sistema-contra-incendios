'''
Melissa Arreola Pasos         00000216552
Itzel Haydeé Garza González   00000216628
Clase main para instanciar el main_Frame.py principal.
'''
from main_Frame import Main_Frame
from tkinter import Tk

def main():
    root = Tk()
    root.wm_title('Sistema contra incendios')
    root.iconbitmap('')
    app = Main_Frame(root)
    app.configure(bg='green3')
    app.mainloop()

if __name__ == "__main__":
    main()
