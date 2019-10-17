import os
import platform
import tkinter as tk


def config_grids(widget, rows=[1], columns=[1]):
    [widget.rowconfigure(i, weight=weight) for i, weight in enumerate(rows)]
    [widget.columnconfigure(i, weight=weight) for i, weight in enumerate(columns)]


class Menubar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(label='Restart', command=self.master.restart)
        self.file_menu.add_command(label='Quit', command=self.master.quit)

        self.add_cascade(label='File', menu=self.file_menu)


class ContextMenu(tk.Menu):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master


class ScrollbarListFrame(tk.Frame):
    def __init__(self, master, *args, list_style={}, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        config_grids(self, columns=[1, 0])

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.listbox = tk.Listbox(
            self, yscrollcommand=self.scrollbar.set, **list_style
        )
        self.listbox.grid(row=0, column=0, sticky='nsew')

        self.scrollbar.config(command=self.listbox.yview)

        self.context_functions = [
            {
                'label': 'Test',
                'state': 'normal',
                'command': self.print_item
            }
        ]

        self.listbox.click_index = -1

        self.populate()


    def clear(self):
        self.listbox.delete(0, tk.END)


    def populate(self):
        for i in range(100):
            self.listbox.insert(tk.END, f'Item {i}')


    def print_item(self):
        print(self.listbox.get(self.listbox.click_index))


class MainWindow(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        self.master.geometry('540x540')
        self.master.title('Main Window')

        self.pack(fill=tk.BOTH, expand=True)

        config_grids(self, rows=[1, 0])

        self.restart_flag = False

        self.listframe = ScrollbarListFrame(
            self, bg='#0c0c0c', list_style={
                                    'font': 'Consolas 12',
                                    'bg': '#0c0c0c',
                                    'fg': '#dcdcdc'
                                }
        )
        self.listframe.grid(row=0, column=0, sticky='nsew')

        self.button = tk.Button(self, text='Test', command=lambda: None)
        self.button.grid(row=1, column=0, sticky='nsew')
        self.button.context_functions = [{
            'label': 'Func',
            'state': 'normal',
            'command': lambda: None
        }]

        self.menu_bar = Menubar(self)
        self.master.config(menu=self.menu_bar)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.master.bind('<Button-3>', self.show_context_menu)


    def show_context_menu(self, event):
        self.context_menu = tk.Menu(self, tearoff=0)
        widget = event.widget
        while True:
            if hasattr(widget, 'context_functions') and widget.context_functions:
                [self.context_menu.add_command(**func) for func in widget.context_functions]
                try:
                    event.widget.selection_clear(0, tk.END)
                    event.widget.click_index = self.listframe.listbox.nearest(event.y_root - event.widget.winfo_rooty())
                    event.widget.selection_set(event.widget.click_index)
                except TypeError:
                    pass # Selection only applies to listboxes
                self.context_menu.post(event.x_root, event.y_root)
                break
            if str(widget) == '.':
                break
            else:
                widget = widget.master


    def quit(self):
        self.cont = False
        self.master.destroy()


    def restart(self):
        self.quit()
        self.restart_flag = True


def main():
    root = tk.Tk()
    window = MainWindow(root)
    root.mainloop()

    if window.restart_flag:
        system = platform.system()
        if system == 'Windows':
            os.system(__file__)
        if system == 'Linux':
            os.system('python3 ' + __file__)


if __name__ == '__main__':
    main()
