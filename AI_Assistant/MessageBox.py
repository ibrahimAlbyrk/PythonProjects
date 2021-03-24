from tkinter import *
from playsound import playsound


class MessageBox:
    root = None
    textBox = None
    button = None
    entry = None
    text = ""

    def __init__(self):
        self.root = Tk()
        self.root.title("Assistant Quinn")
        self.root.iconbitmap("Images/assistantIcon.ico")

    def ShowInputBox(self):
        self.entry = Entry(self.root, width=25)
        self.entry.pack(side="right")
        self.button = Button(self.root, text="gönder", command=self.InputButtonCommand, width=12)
        self.button.pack(side="left")

        self.center_window()
        self.root.attributes("-topmost", True)
        self.root.mainloop()
        return self.text

    def ShowTextBox(self, text):
        self.textBox = Text(self.root)
        self.textBox.insert(INSERT, text)
        self.textBox.pack()
        self.center_window(300, 300)
        self.root.attributes("-topmost", True)
        self.root.mainloop()

    def ShowAlarmBox(self, text):
        playsound("Audios/reminder.mp3")
        textbox = Text(self.root, width=20, height=1)
        textbox.insert(INSERT, text)
        textbox.pack()
        Button(self.root, text="tamam", command=self.ButtonCommand, width=12).pack()
        self.center_window(250, 50)
        self.root.attributes("-topmost", True)
        self.root.mainloop()

    def center_window(self, width=250, height=30):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def InputButtonCommand(self):
        self.text = self.entry.get()
        self.root.destroy()

    def ButtonCommand(self):
        self.root.destroy()
