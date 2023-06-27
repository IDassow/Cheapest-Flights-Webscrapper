from tkinter import ttk
import customtkinter as ctk
import os


# **************** utilities ******************
class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [
            checkbox.cget("text")
            for checkbox in self.checkbox_list
            if checkbox.get() == 1
        ]


class RadiobuttonFrame(ctk.CTkFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = ctk.CTkRadioButton(
            self, text=item, value=item, variable=self.radiobutton_variable
        )
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=0, column=len(self.radiobutton_list), padx=(0, 10), pady=5)
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.button_list = []
        self.total = 1
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        button = ctk.CTkButton(self, text=item, width=100, height=30)
        if self.command is not None:
            button.configure(command=self.command)
        button.grid(row=0, column=len(self.button_list), padx=(0, 10), pady=5)
        self.button_list.append(button)

    def remove_item(self, item):
        for button in self.button_list:
            if item == button.cget("text"):
                button.destroy()
                self.radiobutton_list.remove(button)
                return

    def get_checked_item(self):
        return [
            checkbox.cget("text")
            for checkbox in self.button_list
            if checkbox.get() == 1
        ]
