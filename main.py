from tkinter import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Image Filter')
        self.geometry('{}x{}'.format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.wm_state('zoomed')
        self.create_widgets()

    def create_widgets(self):
        # Label(self, text="").pack()
        
        # self._entry = Entry(self)
        # self._entry.pack()

        # Button(self, text="Botão", command=self.funcao).pack()
        # self.bind('<Return>', lambda e: self.funcao()) # Define uma bind para cionar o botão ao apertar Enter
        pass

if __name__ == '__main__':
    app = App()
    app.mainloop()