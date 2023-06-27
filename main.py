import customtkinter as ctk


ctk.set_default_color_theme("green")
# import PlanIt
import FunctionalFrames as myFrame


# init App
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Plant IT")
        self.geometry(f"{1035}x{700}")
        self.grid_rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1, uniform="a")

        self.infoDict = {}
        # SouthWest DOES NOT show up on expedia
        self.checkbox = {
            "American": "AA",
            "Delta": "DL",
            "United": "US",
            "Spirit": "NK",
            "Alaska": "AS",
            "JetBlue": "B6",
        }

        label = ctk.CTkLabel(
            self,
            text="Welcome To PlantIt!",
            font=ctk.CTkFont(family="Ink Journal", size=45, weight="bold"),
            width=140,
            padx=5,
        )
        label.grid(row=0, column=0, columnspan=3, padx=15, pady=15, sticky="nsew")

        # widgets
        self.locations = myFrame.Locations(self)
        self.locations.grid(row=1, column=0, padx=15, pady=15, sticky="ns")

        self.filter = myFrame.Filters(self, item=self.checkbox)
        self.filter.grid(row=1, column=1, padx=15, pady=15, sticky="ns")

        self.dates = myFrame.Dates(self, command=self.checkinput)
        self.dates.grid(row=1, column=2, padx=15, pady=15, sticky="ns")

        self.dates.get_Duration()
        self.filter.get_items()
        self.locations.get_locations()

        # def calls

    def checkevent(self):
        print(f"checkbox frame modified: {self.filter.get_checked_item()}")

    def checkinput(self):
        self.dates_list = self.dates.get_Duration()
        self.locations_list = self.locations.get_locations()
        self.filters_list = self.filter.get_items()
        if (
            self.dates_list.__contains__("")
            or self.locations_list.__contains__("")
            or self.filters_list.__contains__("")
        ):
            print("Bad input")
            return

        print(f"locations data frame: {self.locations_list}")
        print(f"filters data frame: {self.filter.get_items()}")
        print(f"dates data frame: {self.dates_list}")
        lists = []
        for i in self.filters_list[2]:
            lists.append(self.checkbox[i])

        self.infoDict = {
            "Departure": self.locations_list[0],
            "Arrival": self.locations_list[1],
            "Leave_Date": self.dates_list[0],
            "Return_Date": self.dates_list[1],
            "Trip_type": self.filters_list[0],
            "Travelers": self.filters_list[1],
            "Airlines": lists,
        }

        print(self.infoDict)
        if self.infoDict.__contains__(None):
            print("Bad input")


if __name__ == "__main__":
    app = App()
    app.mainloop()
