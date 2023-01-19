import customtkinter

from modules import scraper, utils

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


# Move all widgets +1 column and create new frame to be
# placed on column 0 for main navigation to select use-case


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Generative AI Summary")
        self.geometry("1100x800")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # configure main side bar
        # self.main_sidebar_frame = customtkinter.CTkFrame(self, width=40, corner_radius=0)

        # create secondary side bar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="GPTsummary",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, text="Home"
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, text="Summary 1"
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, text="Summary 2"
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter article URL")
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

        self.main_button_1 = customtkinter.CTkButton(
            master=self,
            text="Scrape URL",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.input_text,
        )
        self.main_button_1.grid(
            row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(
            row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=2, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Interpreter")
        self.tabview.add("Visualizer")
        self.tabview.add("Translater")
        self.tabview.tab("Interpreter").grid_columnconfigure(
            0, weight=1
        )  # configure grid of individual tabs
        self.tabview.tab("Visualizer").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(
            self.tabview.tab("Interpreter"),
            dynamic_resizing=False,
            values=["Value 1", "Value 2", "Value Long Long Long"],
        )
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.checkbox_1 = customtkinter.CTkCheckBox(
            self.tabview.tab("Interpreter"), text="Generate Image"
        )
        self.checkbox_1.grid(row=1, column=0, pady=(20, 10), padx=20, sticky="n")

        self.string_input_button = customtkinter.CTkButton(
            self.tabview.tab("Interpreter"),
            text="Get Text",
            command=self.open_input_dialog_event,
        )
        self.string_input_button.grid(row=3, column=0, padx=20, pady=(60, 10))
        self.label_tab_2 = customtkinter.CTkLabel(
            self.tabview.tab("Visualizer"), text="CTkLabel on Visualizer"
        )
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.textbox.insert(
            "0.0",
            "CTkTextbox\n\n"
            + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n"
            * 4,
        )

    def open_input_dialog_event(self):  # sourcery skip: class-extract-method
        dialog = customtkinter.CTkInputDialog(text="Enter URL", title="Scrape")
        global_config = utils.get_config()
        goose_config = global_config["goose"]
        self.textbox.delete(index1="0.0", index2="end")
        url = dialog.get_input()
        scraped_data = scraper.scrape_article(url, config=goose_config)
        self.textbox.insert(index="0.0", text=scraped_data["text"])

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def input_text(self):
        global_config = utils.get_config()
        goose_config = global_config["goose"]
        self.textbox.delete(index1="0.0", index2="end")
        url = self.entry.get()
        scraped_data = scraper.scrape_article(url, config=goose_config)
        self.textbox.insert(index="0.0", text=scraped_data["text"])


if __name__ == "__main__":
    app = App()
    app.mainloop()
