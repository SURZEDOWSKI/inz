from tkinter import *
#import tkinter as tk
import customtkinter
import re


from scraper import scrape_prices_from_pages

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):

    def __init__(self) -> None:
        super().__init__()

        self.geometry("1000x700")

        def display_scraped_data():
            
            global dictionary
            global links

            self.textbox_dict.configure(state="normal")
            self.textbox_dict.delete(1.0, END)

            num_of_pages = self.entry_pages.get()
            num_of_pages = int(num_of_pages)
            dictionary_links_values, links_list = scrape_prices_from_pages(num_of_pages)

            for key in dictionary_links_values:
                name = re.findall("[a-zA-Z-]{3,}", key)
                insert_dict_string = name[2] + ": " + dictionary_links_values[key]
                #textbox_dict.insert("0.0", (key, " : ", dictionary_links_values[key], "\n"))
                self.textbox_dict.insert(END, f"{insert_dict_string}\n")

            self.textbox_dict.configure(state="disabled")

            dictionary = dictionary_links_values
            links = links_list

        def find_player():
            self.textbox_dict.configure(state="normal")
            self.textbox_dict.delete(1.0, END)
            
            print()
            name = self.entry_name.get()
            matching_values = [value for key, value in dictionary.items() if name.lower() in key.lower()]
            #print(matching_values)
            link = list(filter(lambda x: name in x, links))
            print(link)
            for i in range(len(link)):
                
                li = re.findall("[a-zA-Z-]{3,}", link[i])
                print(li[2], matching_values[i])
                insert_dict_string = li[2] + ": " + matching_values[i]
                self.textbox_dict.insert(END, f"{insert_dict_string}\n")

            self.textbox_dict.configure(state="disabled")





        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=50, fill="both", expand=True)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure((0, 1), weight=1)

        self.label_scrape = customtkinter.CTkLabel(master=self.frame, text="Scrape prices", font=("Roboto", 24))
        self.label_scrape.grid(pady=12, padx=10, column=0, row=0)

        self.entry_pages = customtkinter.CTkEntry(master=self.frame, placeholder_text="no. pages")
        self.entry_pages.grid(pady=12, padx=10, column=0, row=1)

        self.button_scrape = customtkinter.CTkButton(master=self.frame, text="GET PRICES!", command=display_scraped_data, hover_color='#3377FF')
        self.button_scrape.grid(pady=12, padx=10, column=0, row=2)

        self.label_find = customtkinter.CTkLabel(master=self.frame, text="Find player", font=("Roboto", 24))
        self.label_find.grid(pady=12, padx=10, column=1, row=0)

        self.entry_name = customtkinter.CTkEntry(master=self.frame, placeholder_text="name")
        self.entry_name.grid(pady=12, padx=10, column=1, row=1)

        self.button_find = customtkinter.CTkButton(master=self.frame, text="FIND", command=find_player, hover_color='#3377FF')
        self.button_find.grid(pady=12, padx=10, column=1, row=2)


        self.frame_textbox_dict = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame_textbox_dict.pack(pady=20, padx=50, fill="both", expand=True)

        self.scrollbar_textbox_dict = customtkinter.CTkScrollbar(master=self.frame_textbox_dict, button_hover_color='#3377FF')
        self.scrollbar_textbox_dict.pack(side=RIGHT, fill=Y, pady=10, padx=10)

        self.textbox_dict = Text(master=self.frame_textbox_dict, width=500, height=350, bd=0, bg="#292929", fg="silver", font="Calibri", yscrollcommand=self.scrollbar_textbox_dict.set)
        self.textbox_dict.configure(state="disabled")
        #textbox_dict.grid(row=0, column=0)
        self.textbox_dict.pack(pady=12, padx=10)

        self.scrollbar_textbox_dict.configure(command=self.textbox_dict.yview)


app = App()
app.mainloop()