from tkinter import *
from tkinter import filedialog as fd

# import tkinter as tk
import customtkinter
import re

from program import *

from scraper import scrape_prices_from_pages

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry("1200x800")

        def error_handler(num):
            if num == 0: # not entered num of pages to pull 
                self.textbox_dict.insert(
                    END, "||=== ENTER NUMBER OF PAGES TO PULL! ===||\n", "warning"
                )
                self.textbox_dict.configure(state="disabled")
            
            elif num == 1: # not pulled data yet
                self.textbox_dict.insert(
                    END,
                    "|===| PULL PRICES BEFORE SEARCHING FOR PLAYERS! |===|\n",
                    "warning",
                )
                self.textbox_dict.configure(state="disabled")

            elif num == 2: # no matches
                self.textbox_dict.insert(
                    END, "|===| NO MATCHES! |===|\n", "warning"
                )
                self.textbox_dict.insert(
                    END, "Try other name or try pulling more prices...\n", "warning"
                )
                self.textbox_dict.configure(state="disabled")

            elif num == 3: # not enough characters
                self.textbox_dict.insert(
                    END, "|===| ENTER AT LEAST 3 LETTERS! |===|\n", "warning"
                )
                self.textbox_dict.configure(state="disabled")
            
            elif num == 4: # no. pages is not a int
                self.textbox_dict.insert(
                    END, "|===| NO. PAGES MUST BE A NUMBER! |===|\n", "warning"
                )
                self.textbox_dict.configure(state="disabled")

            elif num == 5: # no detections on img
                self.textbox_dict.insert(
                    END, "|===| NO DETECTIONS ON IMAGE! |===|\n", "warning"
                )
                self.textbox_dict.configure(state="disabled")

        def display_scraped_data():

            self.textbox_dict.configure(state="normal")
            self.textbox_dict.delete(1.0, END)

            num_of_pages = self.entry_pages.get()
            if not num_of_pages:
                error_handler(0)
                return 0
            
            try:
                num_of_pages = int(num_of_pages)
            except ValueError:
                error_handler(4)
                return 0

            global dictionary
            dictionary = {}
            global links

            dictionary_links_values, links_list = scrape_prices_from_pages(
                num_of_pages, sort_var.get()
            )

            for key in dictionary_links_values:
                name = re.findall("[a-zA-Z-]{3,}", key)
                insert_dict_string = name[2] + ": " + dictionary_links_values[key]
                # textbox_dict.insert("0.0", (key, " : ", dictionary_links_values[key], "\n"))
                self.textbox_dict.insert(END, f"{insert_dict_string}\n")

            self.textbox_dict.configure(state="disabled")

            dictionary = dictionary_links_values
            links = links_list

        def find_player():
            self.textbox_dict.configure(state="normal")
            self.textbox_dict.delete(1.0, END)

            try:
                dictionary
            except NameError:
                error_handler(1)
                return 0

            name = self.entry_name.get()
            name = name.lower()
            val_name = re.match("[a-zA-Z-]{3,}", name)
            if val_name is not None:

                matching_values = [
                    value for key, value in dictionary.items() if name in key.lower()
                ]
                # print(matching_values)
                link = list(filter(lambda x: name in x, links))
                # print(link)
                if len(link) == 0:
                    error_handler(2)
                else:
                    for i in range(len(link)):

                        li = re.findall("[a-zA-Z-]{3,}", link[i])
                        # print(li[2], matching_values[i])
                        insert_dict_string = li[2] + ": " + matching_values[i]
                        self.textbox_dict.insert(END, f"{insert_dict_string}\n")

            else:
                error_handler(3)

            self.textbox_dict.configure(state="disabled")

        def detect_img():

            self.textbox_dict.configure(state="normal")
            self.textbox_dict.delete(1.0, END)

            filetypes = ((".png", "*.png"), (".img", "*.img"), ("All files", "*.*"))

            try:
                dictionary
            except NameError:
                error_handler(1)
                return 0

            filename = fd.askopenfilename(
                title="Open a file", initialdir="/", filetypes=filetypes
            )

            print(filename)

            final_links, final_prices = main(dictionary, links, img_path=filename)
            print(final_links, final_prices)

            if len(final_links) == 0:
                error_handler(5)
                return 0

            for i in range(len(final_links)):
                name = re.findall("[a-zA-Z-]{3,}", final_links[i])
                self.textbox_dict.insert(
                    END,
                    f"{name[2].upper()}: {final_prices[i]}", "result",
                )
                self.textbox_dict.insert(
                    END,
                    f" :: link: www.futwiz.com{final_links[i]}\n",
                )

            self.textbox_dict.configure(state="disabled")

        def detect_cam():

            self.textbox_dict.configure(state="normal")
            self.textbox_dict.delete(1.0, END)

            try:
                dictionary
            except NameError:
                error_handler(1)
                return 0

            final_links, final_prices = main(dictionary, links, vid_path=0)

            if len(final_links) == 0:
                error_handler(5)
                return 0

            for i in range(len(final_links)):
                name = re.findall("[a-zA-Z-]{3,}", final_links[i])
                self.textbox_dict.insert(
                    END,
                    f"{name[2].upper()}: {final_prices[i]}", "result",
                )
                self.textbox_dict.insert(
                    END,
                    f" :: link: www.futwiz.com{final_links[i]}\n",
                )
                
            self.textbox_dict.configure(state="disabled")

        self.frame = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame.pack(pady=20, padx=50, fill="both", expand=True)

        self.title("FIFA 23 PRICE DETECTION")
        self.minsize(800, 500)

        # self.frame.grid_rowconfigure(0, weight=1)
        # self.frame.grid_columnconfigure(0, weight=1, uniform="fred")
        self.frame.grid_columnconfigure((0, 0), weight=1, uniform="fred")
        self.frame.grid_columnconfigure((1, 0), weight=1, uniform="fred")
        self.frame.grid_columnconfigure((2, 0), weight=1, uniform="fred")
        self.frame.grid_columnconfigure((3, 0), weight=1, uniform="fred")

        self.label_scrape = customtkinter.CTkLabel(
            master=self.frame, text="Scrape prices", font=("Roboto", 24)
        )
        self.label_scrape.grid(pady=6, padx=10, column=0, row=0)

        self.entry_pages = customtkinter.CTkEntry(
            master=self.frame, placeholder_text="no. pages", fg_color='silver', placeholder_text_color='#40403f', text_color='black'
        )
        self.entry_pages.grid(pady=6, padx=10, column=0, row=1)

        self.button_scrape = customtkinter.CTkButton(
            master=self.frame,
            text="GET PRICES",
            command=display_scraped_data,
            hover_color="#3377FF",
        )
        self.button_scrape.grid(pady=6, padx=10, column=0, row=2)

        sort_var = IntVar(self.master, 1)
        self.radiobutton_overall = customtkinter.CTkRadioButton(
            master=self.frame,
            text="overall",
            variable=sort_var,
            value=1,
            hover_color="#3377FF",
            radiobutton_height=15,
            radiobutton_width=15,
        )
        self.radiobutton_price = customtkinter.CTkRadioButton(
            master=self.frame,
            text="price",
            variable=sort_var,
            value=2,
            hover_color="#3377FF",
            radiobutton_height=15,
            radiobutton_width=15,
        )
        self.radiobutton_overall.grid(column=0, row=3, pady=3, padx=10)
        self.radiobutton_price.grid(column=0, row=4, pady=3, padx=10)

        self.label_find = customtkinter.CTkLabel(
            master=self.frame, text="Find player", font=("Roboto", 24)
        )
        self.label_find.grid(pady=6, padx=10, column=1, row=0)

        self.entry_name = customtkinter.CTkEntry(
            master=self.frame, placeholder_text="name", fg_color='silver', placeholder_text_color='#40403f', text_color='black'
        )
        self.entry_name.grid(pady=6, padx=10, column=1, row=1)

        self.button_find = customtkinter.CTkButton(
            master=self.frame, text="FIND", command=find_player, hover_color="#3377FF"
        )
        self.button_find.grid(pady=6, padx=10, column=1, row=2)

        self.label_detect_img = customtkinter.CTkLabel(
            master=self.frame, text="Detect from image", font=("Roboto", 24)
        )
        self.label_detect_img.grid(pady=6, padx=10, column=2, row=0)

        self.entry_detect_img = customtkinter.CTkEntry(
            master=self.frame, placeholder_text="path",
        )
        self.entry_detect_img.configure(state="disabled")
        self.entry_detect_img.grid(pady=6, padx=10, column=2, row=1)

        self.button_detect_img = customtkinter.CTkButton(
            master=self.frame, text="BROWSE", command=detect_img, hover_color="#3377FF"
        )
        self.button_detect_img.grid(pady=6, padx=10, column=2, row=2)

        self.label_detect_cam = customtkinter.CTkLabel(
            master=self.frame, text="Detect from camera", font=("Roboto", 24)
        )
        self.label_detect_cam.grid(pady=6, padx=10, column=3, row=0)

        self.entry_detect_cam = customtkinter.CTkEntry(
            master=self.frame, placeholder_text="camera no.",
        )
        self.entry_detect_cam.configure(state="disabled")
        self.entry_detect_cam.grid(pady=6, padx=10, column=3, row=1)

        self.button_detect_cam = customtkinter.CTkButton(
            master=self.frame, text="DETECT", command=detect_cam, hover_color="#3377FF"
        )
        self.button_detect_cam.grid(pady=6, padx=10, column=3, row=2)  

        self.frame_textbox_dict = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame_textbox_dict.pack(pady=20, padx=50, fill="both", expand=True)

        self.scrollbar_textbox_dict = customtkinter.CTkScrollbar(
            master=self.frame_textbox_dict, button_hover_color="#3377FF"
        )
        self.scrollbar_textbox_dict.pack(side=RIGHT, fill=Y, pady=10, padx=10)

        self.textbox_dict = Text(
            master=self.frame_textbox_dict,
            width=500,
            height=350,
            bd=0,
            bg="silver",
            fg="black",
            font="Calibri",
            yscrollcommand=self.scrollbar_textbox_dict.set,
        )
        self.textbox_dict.configure(state="disabled")
        self.textbox_dict.tag_config("warning", foreground="red")
        self.textbox_dict.tag_config("result", foreground="green")
        # textbox_dict.grid(row=0, column=0)
        self.textbox_dict.pack(pady=12, padx=10)

        self.scrollbar_textbox_dict.configure(command=self.textbox_dict.yview)


app = App()
app.mainloop()
