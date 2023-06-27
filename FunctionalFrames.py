from tkinter import ttk, Tk, font as tk
import customtkinter as ctk
import os
import sys


# import PlanIt
import UtilFrames as myFrame


# **************** functional elements ******************
class Locations(ctk.CTkFrame):
    def __init__(self, parent, command=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.command = command

        self.e1_text = ctk.StringVar()
        self.e2_text = ctk.StringVar()
        self.entries = []

        self.grid_columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=0)
        self.rowconfigure((1, 2), weight=0)
        self.rowconfigure((3), weight=1)

        title_label = ctk.CTkLabel(
            self,
            text="Where To?",
            font=ctk.CTkFont("Ink Journal", 35, "normal"),
        ).grid(row=0, column=0, columnspan=2, pady=(15, 45), padx=15)

        start_label = ctk.CTkLabel(
            self, text="Starting from:", font=ctk.CTkFont("Roboto", 16, "normal")
        ).grid(row=1, column=0, pady=15, padx=5)

        self.start_entery = ctk.CTkEntry(
            self,
            width=160,
            height=30,
            corner_radius=5,
            placeholder_text="ex: Chicago, IL ",
        )
        self.start_entery.grid(row=1, column=1, pady=15, padx=(5, 15))
        self.entries.append(self.start_entery.get())

        destin_label = ctk.CTkLabel(
            self, text="Going To:", font=ctk.CTkFont("Roboto", 16, "normal")
        ).grid(row=2, column=0, pady=15, padx=(15, 5))

        self.destin_entery = ctk.CTkEntry(
            self,
            width=160,
            height=30,
            corner_radius=5,
            placeholder_text="ex: Los Angeles, CA",
        )
        self.destin_entery.grid(row=2, column=1, pady=15, padx=(5, 15))
        self.entries.append(self.destin_entery.get())

    def get_locations(self):
        self.entries[0] = self.start_entery.get()
        self.entries[1] = self.destin_entery.get()

        return self.entries


class Filters(ctk.CTkFrame):
    def __init__(self, parent, item={}, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.rowconfigure((0, 2, 5), weight=0)
        self.rowconfigure((1, 3, 4, 6), weight=1)

        self.total_t = ctk.IntVar()
        self.total_t.set(1)
        self.checkbox_list = list(item.keys())

        title_label = ctk.CTkLabel(
            self, text="Flight Filters", font=ctk.CTkFont("Ink Journal", 35, "normal")
        ).grid(row=0, column=0, columnspan=3, pady=25, padx=25)
        self.radio_var = ctk.IntVar(value=0)

        # Type of airline tickets
        Flighttype_label = ctk.CTkLabel(
            self, text="Flight type", font=ctk.CTkFont("Roboto", 16, "bold")
        )
        Flighttype_label.grid(row=1, column=0, pady=(10, 5), columnspan=3)

        self.flight_type_radioButton = myFrame.RadiobuttonFrame(
            master=self,
            width=500,
            command=self.radiobutton_frame_event,
            item_list=[f"One-way", "Roundtrip"],
        )
        self.flight_type_radioButton.grid(
            row=2, column=0, columnspan=3, padx=15, pady=(0, 10)
        )

        # Number of Travelers to be accounted for
        Travelers_label = ctk.CTkLabel(
            self,
            text="How many will be flying?",
            font=ctk.CTkFont("Roboto", 16, "bold"),
        )
        Travelers_label.grid(row=3, column=0, pady=(15, 5), columnspan=3)

        self.mButton1 = ctk.CTkButton(
            self,
            height=40,
            text="-",
            font=ctk.CTkFont("Impact", 20, "normal"),
            command=lambda: self.get_checked_item("-"),
        ).grid(row=4, column=0, pady=(0, 10), padx=(15, 25))

        self.total_label = ctk.CTkLabel(
            self,
            textvariable=self.total_t,
            font=ctk.CTkFont("Helevita", 24, "bold"),
        ).grid(
            row=4,
            column=1,
            columnspan=1,
            pady=(0, 10),
        )

        self.mButton2 = ctk.CTkButton(
            self,
            height=40,
            text="+",
            font=ctk.CTkFont("Impact", 20, "normal"),
            command=lambda: self.get_checked_item("+"),
        ).grid(row=4, column=2, pady=(0, 10), padx=(25, 15))

        # create scrollable checkbox frame
        Airlines_label = ctk.CTkLabel(
            self,
            text="Prefered Airlines",
            font=ctk.CTkFont("Roboto", 16, "bold"),
        )
        Airlines_label.grid(row=5, column=0, pady=(15, 5), columnspan=3)

        self.airlines_checkbox_frame = myFrame.ScrollableCheckBoxFrame(
            master=self,
            width=200,
            height=50,
            command=self.checkbox_frame_event,
            item_list=self.checkbox_list,
        )
        self.airlines_checkbox_frame.grid(
            row=6, column=0, columnspan=3, padx=15, pady=(5, 15)
        )

    def checkbox_frame_event(self):
        print(
            f"checkbox frame modified: {self.airlines_checkbox_frame.get_checked_items()}"
        )

    def radiobutton_frame_event(self):
        print(
            f"radiobutton frame modified: {self.flight_type_radioButton.get_checked_item()}"
        )

    def get_checked_item(self, key):
        if key == "+":
            self.total_t.set(self.total_t.get() + 1)
            print(f"Travelers modified: {self.total_t.get()}")
        elif key == "-":
            if self.total_t.get() == 1:
                print(f"Travelers cant be less than one: {self.total_t.get()}")
            else:
                self.total_t.set(self.total_t.get() - 1)
                print(f"Travelers modified: {self.total_t.get()}")
        else:
            print(f"Travelers : {self.total_t.get()}")
        return self.total_t

    def get_items(self):
        radio_var = self.flight_type_radioButton.get_checked_item()
        airlines_var = self.airlines_checkbox_frame.get_checked_items()
        total_travelers = self.total_t.get()
        return [radio_var, total_travelers, airlines_var]


class Dates(ctk.CTkFrame):
    def __init__(self, parent, command=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.command = command

        self.grid_columnconfigure((0), weight=1)
        self.rowconfigure((0), weight=0)
        self.rowconfigure((1, 2), weight=0)
        self.rowconfigure((3), weight=1)

        self.e1_text = ctk.StringVar()
        self.e2_text = ctk.StringVar()
        self.entries = []

        title_label = ctk.CTkLabel(
            self, text="Dates", font=ctk.CTkFont("Ink Journal", 30, "normal")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=15, padx=15)

        self.leave_label = ctk.CTkLabel(
            self, text="Departing:", font=ctk.CTkFont("Helevita", 16, "normal")
        )
        self.leave_label.grid(row=1, column=0, pady=15, padx=5)

        self.Leaving_entery = ctk.CTkEntry(
            self,
            width=160,
            height=30,
            corner_radius=5,
            placeholder_text="Jun 20, 2024",
        )
        self.Leaving_entery.grid(row=1, column=1, pady=15, padx=(5, 15))
        self.entries.append(self.Leaving_entery.get())

        self.return_label = ctk.CTkLabel(
            self,
            text="Returning:",
            font=ctk.CTkFont(family="Helevita", size=16, weight="normal"),
        ).grid(row=2, column=0, pady=15, padx=(15, 5))

        self.Returning_entery = ctk.CTkEntry(
            self,
            width=160,
            height=30,
            corner_radius=5,
            placeholder_text="Jul 4, 2024",
        )
        self.Returning_entery.grid(row=2, column=1, pady=15, padx=(5, 15))
        self.entries.append(self.Leaving_entery.get())
        self.mButton2 = ctk.CTkButton(
            self,
            height=50,
            text="Confirm",
            font=ctk.CTkFont("Ink Journal", 24, "normal"),
            command=lambda: self.get_Duration(),
        )
        self.mButton2.grid(
            row=4,
            column=0,
            columnspan=3,
            pady=15,
        )

    def get_Duration(self):
        self.entries[0] = self.Leaving_entery.get()
        self.entries[1] = self.Returning_entery.get()

        if self.command is not None:
            self.mButton2.configure(command=self.command)
            return self.entries
        return [checkbox for checkbox in self.entries]
