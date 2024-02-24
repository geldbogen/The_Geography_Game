import tkinter as tk
import random
from tkinter import colorchooser
import ttkbootstrap as ttk
from player import Player
from global_definitions import all_categories
from setup_game import setup_the_game


class IntroWindow:

    def __init__(self):

        self.i = 0
        self.root = ttk.Window()
        self.start_country = ttk.StringVar()
        self.winning_condition = ttk.StringVar()
        self.wormhole_option = ttk.StringVar()
        self.list_of_players :list[Player] = list()
        pred_choose_var = ttk.StringVar(self.root)
        pred_choose_var.set("Random")
        self.end_attribute_var = ttk.StringVar()
        self.end_attribute_var.set("Random")

        self.showinglabel = ttk.Label(
            self.root,
            text=
            "Welcome to the Geography Game,\n please choose your names and colors")
        self.showinglabel.grid(row=0, column=0)

        #middle side
        self.nameentry = ttk.Entry(self.root)
        self.nameentry.grid(row=1, column=0)

        choosecolorbutton = ttk.Button(self.root,
                                      text="Choose your color",
                                      command=self.choose_color)
        choosecolorbutton.grid(row=2, column=0)

        gogobutton = ttk.Button(self.root, text="Let's go", command=self.go)
        gogobutton.grid(row=9, column=0)

        self.currentplayerslistbox = tk.Listbox(self.root, height=4)
        self.currentplayerslistbox.grid(row=4, column=0)

        self.label2 = ttk.Label(self.root,
                               text="How many rounds do you want to play")
        self.label2.grid(row=5, column=0)

        self.label3 = ttk.Label(self.root,
                               text="Current participating players:")
        self.label3.grid(row=3, column=0)

        self.numberofroundsentry = ttk.Entry(self.root)
        self.numberofroundsentry.grid(
            row=6,
            column=0,
        )

        # right side
        self.label4 = ttk.Label(self.root, text="Some (advanced) options")
        self.label4.grid(row=0, column=1)

        self.label5 = ttk.Label(self.root, text="Starting countries")
        self.label5.grid(row=1, column=1)

        self.startcountryoptions1 = ttk.Radiobutton(self.root,
                                                   text="Random",
                                                   variable=self.start_country,
                                                   value="random")
        self.startcountryoptions1.grid(row=2, column=1)

        self.startcountryoptions2 = ttk.Radiobutton(self.root,
                                                   text="Choose",
                                                   variable=self.start_country,
                                                   value="choose")
        self.startcountryoptions2.grid(row=3, column=1)

        self.start_country.set("random")

        self.winconditionframe = ttk.Frame(self.root)

        self.label6 = ttk.Label(self.winconditionframe,
                               text="Winning condition")
        self.label6.grid(row=0, column=0)

        self.winningconditionoption1 = ttk.Radiobutton(
            self.winconditionframe,
            text="Number of countries",
            variable=self.winning_condition,
            value="number of countries")
        self.winningconditionoption1.grid(row=1, column=0, sticky="w", padx=60)

        self.winningconditionoption2 = ttk.Radiobutton(
            self.winconditionframe,
            text="Hold 2 countries to win",
            variable=self.winning_condition,
            value="claim 2 countries")
        self.winningconditionoption2.grid(row=2, column=0, sticky="w", padx=60)

        self.winningconditionoption3 = ttk.Radiobutton(
            self.winconditionframe,
            text="Claim at first the golden countries",
            variable=self.winning_condition,
            value="get gold")
        self.winningconditionoption3.grid(row=3, column=0, sticky="w", padx=60)

        self.winningconditionoption4 = ttk.Radiobutton(
            self.winconditionframe,
            text="Claim countries according to a predeterminded attribute",
            variable=self.winning_condition,
            value="attribute",
            command=self.show_option_for_pred_attribute)
        self.winningconditionoption4.grid(row=4, column=0, sticky="w", padx=60)

        self.winningconditionoption5 = ttk.Radiobutton(
            self.winconditionframe,
            text="Secret targets",
            variable=self.winning_condition,
            value="secret targets")
        self.winningconditionoption5.grid(row=7, column=0, sticky="w", padx=60)

        self.winningconditionoption6 = ttk.Radiobutton(
            self.winconditionframe,
            text="Secret attribute",
            variable=self.winning_condition,
            value="secret attribute")
        self.winningconditionoption6.grid(row=8, column=0, sticky="w", padx=60)

        self.winning_condition.set("number of countries")

        self.winconditionframe.grid(row=4, column=1, padx=60)

        #far right side
        self.africavar = ttk.IntVar()
        self.north_americavar = ttk.IntVar()
        self.middle_americavar = ttk.IntVar()
        self.south_americavar = ttk.IntVar()
        self.asiavar = ttk.IntVar()
        self.europevar = ttk.IntVar()
        self.oceaniavar = ttk.IntVar()

        self.farrightframe = ttk.Frame(self.root)

        self.label7 = ttk.Label(self.farrightframe,
                               text="Which continents would you like to play?")
        self.label7.grid(
            row=0,
            column=0,
        )

        self.africa_check = ttk.Checkbutton(self.farrightframe,
                                           text="Africa",
                                           variable=self.africavar)
        self.africa_check.grid(row=1, column=0, sticky="W")
        self.africa_check.invoke()

        self.north_america_check = ttk.Checkbutton(
            self.farrightframe,
            text="North America",
            variable=self.north_americavar)
        self.north_america_check.grid(row=2, column=0, sticky="W")
        self.north_america_check.invoke()

        self.middle_america_check = ttk.Checkbutton(
            self.farrightframe,
            text="Middle America",
            variable=self.middle_americavar)
        self.middle_america_check.grid(row=3, column=0, sticky="W")
        self.middle_america_check.invoke()

        self.south_america_check = ttk.Checkbutton(
            self.farrightframe,
            text="South America",
            variable=self.south_americavar)
        self.south_america_check.grid(row=4, column=0, sticky="W")
        self.south_america_check.invoke()

        self.asia_check = ttk.Checkbutton(self.farrightframe,
                                         text="Asia",
                                         variable=self.asiavar)
        self.asia_check.grid(row=5, column=0, sticky="W")
        self.asia_check.invoke()

        self.europe_check = ttk.Checkbutton(self.farrightframe,
                                           text="Europe",
                                           variable=self.europevar)
        self.europe_check.grid(row=6, column=0, sticky="W")
        self.europe_check.invoke()

        self.oceania_check = ttk.Checkbutton(self.farrightframe,
                                            text="Oceania",
                                            variable=self.oceaniavar)
        self.oceania_check.grid(row=7, column=0, sticky="W")
        self.oceania_check.invoke()
        self.farrightframe.grid(row=0, column=2, rowspan=8)

        self.wormhole_optionsframe = ttk.Frame(self.root)

        self.wormhole_optionslabel = ttk.Label(self.wormhole_optionsframe,
                                              text="Wormhole options")
        self.no_wormholes = ttk.Radiobutton(self.wormhole_optionsframe,
                                           text="No wormholes at all",
                                           variable=self.wormhole_option,
                                           value="no wormholes at all")
        self.fixed_wormholes = ttk.Radiobutton(self.wormhole_optionsframe,
                                              text="Fixed starting wormholes",
                                              variable=self.wormhole_option,
                                              value="fixed starting wormholes")
        self.every_round_changing_wormholes = ttk.Radiobutton(
            self.wormhole_optionsframe,
            text="Every round changing wormholes",
            variable=self.wormhole_option,
            value="every round changing wormholes")
        self.from_your_side_changing_wormholes = ttk.Radiobutton(
            self.wormhole_optionsframe,
            variable=self.wormhole_option,
            text="Every round changing wormholes from your countries",
            value="every round changing wormholes from your countries")

        self.wormhole_option.set("no wormholes at all")

        self.wormhole_optionslabel.grid(row=0, column=0)
        self.no_wormholes.grid(row=1, column=0, sticky="w")
        self.fixed_wormholes.grid(row=2, column=0, sticky="w")
        self.every_round_changing_wormholes.grid(row=3, column=0, sticky="w")
        self.from_your_side_changing_wormholes.grid(row=4,
                                                    column=0,
                                                    sticky="w")

        self.wormhole_optionsframe.grid(row=0, column=3, rowspan=5)

        self.peacemode_var = ttk.IntVar()
        self.peacemode_check = ttk.Checkbutton(self.root,
                                              text="Peace Mode",
                                              variable=self.peacemode_var)
        self.peacemode_check.grid(row=5, column=3)

        #variable for setting whether the final attribute will be reversed, if we play the random attribute mode
        self.reverse_yes_or_no_var = ttk.IntVar()
        self.reverse_yes_or_no_var.set(0)

        self.root.mainloop()

    def choose_color(self):
        if self.nameentry.get() == "":
            return None
        playercolor = colorchooser.askcolor(title="choose your color")
        name = self.nameentry.get()
        self.nameentry.delete(0, "end")
        self.list_of_players.append(Player(color=playercolor[0], name=name))
        self.currentplayerslistbox.insert(self.i, name)
        self.i = self.i + 1

    def show_option_for_pred_attribute(self):

        def roll_attribute():
            rng = random.randrange(1, len(self.displayed_list))
            print(rng)
            self.choose_pred_attribute.current(rng)
            if random.random() <= 0.5:
                self.reverse_yes_or_no.invoke()
            else:
                self.reverse_yes_or_no.invoke()
                

        pred_choose_var = ttk.StringVar(self.winconditionframe)
        pred_choose_var.set("Random")
        self.displayed_list = [c.name for c in all_categories]
        self.displayed_list.sort()
        self.displayed_list = ["Surprise Me!"] + self.displayed_list
        self.displayed_list = [m.rstrip(".csv") for m in self.displayed_list]
        self.end_attribute_var = ttk.StringVar()
        self.choose_pred_attribute = ttk.Combobox(
            self.winconditionframe,
            values=self.displayed_list,
            width=100,
            state="readonly",
            textvariable=self.end_attribute_var)
        self.choose_pred_attribute.current(0)
        self.choose_pred_attribute.grid(
            row=5,
            column=0,
        )

        self.reverse_yes_or_no = ttk.Checkbutton(
            self.winconditionframe,
            text="Reverse?",
            variable=self.reverse_yes_or_no_var)
        self.reverse_yes_or_no.grid(row=6, column=0, padx=60)

        self.roll_button = ttk.Button(self.winconditionframe,
                                     text="Randomize!",
                                     command=roll_attribute)
        self.roll_button.grid(row=5, column=1, sticky="w")

    def go(self):

        self.active_continent_list : list[str] = []
        if self.africavar.get() == 1:
            self.active_continent_list.append("Africa")
        if self.asiavar.get() == 1:
            self.active_continent_list.append("Asia")
        if self.europevar.get() == 1:
            self.active_continent_list.append("Europe")
        if self.north_americavar.get() == 1:
            self.active_continent_list.append("North America")
        if self.middle_americavar.get() == 1:
            self.active_continent_list.append("Middle America")
        if self.south_americavar.get() == 1:
            self.active_continent_list.append("South America")
        if self.oceaniavar.get() == 1:
            self.active_continent_list.append("Oceania")

        self.number_of_rounds : int = int(self.numberofroundsentry.get())

        if not self.number_of_rounds:
            self.number_of_rounds  == -1

        self.root.destroy()

        setup_the_game(continent_list=self.active_continent_list,
                       list_of_players=self.list_of_players,
                       number_of_rounds=self.number_of_rounds,
                       number_of_rerolls=self.number_of_rounds // 3,
                       starting_countries_preferences=self.start_country.get(),
                       winning_condition=self.winning_condition.get(),
                       end_attribute_path=self.end_attribute_var.get() +
                       ".csv",
                       peacemode=self.peacemode_var.get() == 1,
                       wormhole_mode=self.wormhole_option.get(),
                       reversed_end_attribute=self.reverse_yes_or_no_var.get(),
                       start_the_game=True)
