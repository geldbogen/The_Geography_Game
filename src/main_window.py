import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.window import Toplevel
from PIL import ImageTk, Image
import sv_ttk
import random
import traceback
import numpy as np
import wikipedia
import webbrowser

from country import Country, get_country_by_position, Unknown_country, Germany, France
from category import Category
from player import Player, call_player_by_name, No_Data_Body, mr_nobody
from image import greencountrydict, green_image
from global_definitions import all_categories, all_countries_in_game, dictionary_attribute_name_to_attribute, gold, realgrey
from backend_game import BackendGame
from endscreen import endscreen


class MainWindow():

    def __init__(self,
                 bild: Image.Image,
                 list_of_players: list[Player],
                 wormhole_mode: str,
                 starting_countries_preferences: str = "random",
                 number_of_rounds: int = 99999999999,
                 winning_condition: str = "number of countries",
                 number_of_wormholes: int = 3,
                 pred_attribute: str = "random",
                 peacemode: bool = False,
                 reversed_end_attribute: int = 0):

        self.backend: BackendGame = BackendGame(list_of_players, wormhole_mode, starting_countries_preferences,
                                                number_of_rounds, winning_condition, number_of_wormholes,
                                                  pred_attribute, peacemode, reversed_end_attribute)
        self.rerolls: int = 3

        self.number_of_targets = 2

        self.pred_attribute_name = pred_attribute

        self.winning_condition = winning_condition

        self.flagframe_dict: dict[str, ttk.Frame] = dict()
        self.number_of_rounds = number_of_rounds
        self.index = 0
        self.goldlist: list[Country] = list()
        self.choosing_index = -1
        self.starting_countries = starting_countries_preferences
        self.reversed_end_attribute = reversed_end_attribute
        self.main = ttk.Window()

        print(self.backend.list_of_players)
        print(len(list_of_players))
        self.backend.active_player = self.backend.list_of_players[
            self.backend.active_player_counter]
        self.number_of_players = len(self.backend.list_of_players)


        self.wormhole_mode: str = wormhole_mode
        self.linelist = list()
        self.pointlist = list()

        self.wormholed_countries: list[list[Country]] = list()

        self.number_of_wormholes = number_of_wormholes

        print(self.winning_condition)

        self.peacemode: bool = peacemode

        self.backend.current_attribute = all_categories[0]

        self.chosen_country_a = None
        self.turn_counter = 0

        self.frame1 = ttk.Frame(self.main, width=300, height=300)
        self.frame1.pack(side="bottom", fill="both", expand=True)

        # frame1=frame2+areyousurebuttons

        self.frame2 = ttk.Frame(self.frame1)
        # frame2= frame3 + flags

        self.frame3 = ttk.Frame(self.frame2)
        self.buttonframe = ttk.Frame(self.frame1)
        self.buttonframe2 = ttk.Frame(self.frame1)
        self.bild = bild
        self.c = ttk.Canvas(self.frame3, bg="white", width=1000, height=600)

        ph = ImageTk.PhotoImage(image=bild, master=self.c)

        self.c.background = ph
        self.image_on_canvas = self.c.create_image(0,
                                                   0,
                                                   image=self.c.background,
                                                   anchor="nw")

        # scrollbar
        my_scrollbar1 = tk.Scrollbar(self.frame3,
                                     orient="vertical",
                                     command=self.c.yview)
        my_scrollbar1.pack(side="right", fill="y")
        my_scrollbar1.config(command=self.c.yview)
        my_scrollbar2 = tk.Scrollbar(self.frame3,
                                     orient="horizontal",
                                     command=self.c.xview)
        my_scrollbar2.pack(side="bottom", fill="x")
        my_scrollbar2.config(command=self.c.xview)
        self.c.config(yscrollcommand=my_scrollbar1.set,
                      xscrollcommand=my_scrollbar2.set)
        self.c.config(scrollregion=self.c.bbox("all"))

        for player in self.backend.list_of_players:
            self.flagframe_dict[player.name] = ttk.Frame(self.frame2)
            self.flagframe_dict[player.name].current_flagdict = dict()

        self.c.bind("<ButtonPress-1>", self.click)

        self.c.bind("<ButtonPress-3>", self.scroll_start)
        self.c.bind("<B3-Motion>", self.scroll_move)

        # unpacking
        self.frame3.pack(side="bottom", expand=True, fill="both")
        self.frame2.pack(side="top", expand=True, fill="both")
        self.frame1.pack(side="top", expand=True, fill="both")
        self.frame4 = ttk.Frame(self.frame3)
        self.frame5 = ttk.Frame(self.frame3)

        self.reroll_button = ttk.Button(
            self.frame5,
            text="rerolls left:\n " +
            str(self.backend.active_player.rerolls_left),
            command=lambda: self.backend.reroll(activating_player=self.backend.active_player,to_update_category_label=self.showing_current_attribute_text_label, to_update_reroll_button=self.reroll_button))

        self.reroll_button.pack(side="left", fill="y")

        self.showing_country_label = ttk.Label(
            self.frame5,
            text="It is the turn of " + self.backend.active_player.name +
            "\n You have not chosen any country yet",
            font="Helvetica 25")
        self.showing_country_label.pack(side="bottom",
                                        expand=True,
                                        fill="both")

        self.turn_counter_label = ttk.Label(self.frame4,
                                           text=str(self.turn_counter),
                                           font="Helvetica 50")
        self.turn_counter_label.pack(side="right")

        self.showing_current_attribute_text_label = ttk.Label(
            self.frame4, text="Welcome!", font="Helvetica 25")
        self.showing_current_attribute_text_label.pack(anchor="nw",
                                                       expand=True,
                                                       fill="both")

        self.frame4.pack(side="top", fill="x")
        self.frame5.pack(side="bottom", fill="x")

        self.c.pack(side="top", fill="both", expand=True)

        self.button_sure = ttk.Button(self.buttonframe,
                                     text="Attack!",
                                     )
        self.button_not_sure = ttk.Button(self.buttonframe,
                                         text="No go back",
                                         )
        self.button_sure.pack(side="left")
        self.button_not_sure.pack(side="right")
        self.button_claim = ttk.Button(self.buttonframe2,
                                      text="Yes Please!",
                                      )

        self.d = ""
        self.random_people_start = random.sample(
            range(0, len(self.backend.list_of_players)), len(self.backend.list_of_players))

        # usher choosing countries procedure if that mode was chosen
        if self.starting_countries == "choose":
            self.choosing_index = 0
            self.backend.active_player = self.backend.list_of_players[self.random_people_start[
                self.choosing_index]]
            self.showing_current_attribute_text_label[
                "text"] = "Choose a starting country of your choice"
            self.showing_country_label[
                "text"] = self.backend.active_player.name + "\n Please choose a starting country"

        # roll starting countries for the players
        # TODO take care of ending attribute
        if self.starting_countries == "random":
            self.choosing_index = len(self.backend.list_of_players)
            self.setupgame()
            while True:
                j = 0
                self.randomstart = random.sample(range(0, len(all_countries_in_game)),
                                                 len(self.backend.list_of_players))
                for rng in self.randomstart:
                    if len(all_countries_in_game[rng].neighboring_countries) < 3:
                        j = 1
                    for rng2 in self.randomstart:
                        if all_countries_in_game[rng2].is_connected_with(
                                all_countries_in_game[rng]):
                            j = 1
                    if self.winning_condition == "attribute":
                        try:
                            all_countries_in_game[rng].dict_of_attributes[
                                self.backend.end_attribute.name].value
                        except:
                            j = 1
                if j == 0:
                    break
            for i in range(len(self.backend.list_of_players)):
                self.claim_country(self.backend.list_of_players[i],
                                   all_countries_in_game[self.randomstart[i]])
                print(all_countries_in_game[self.randomstart[i]].name)

        # roll first attribute
        self.backend.current_attribute = self.backend.active_player.get_good_attribute(
            peacemode=self.peacemode)
        self.backend.current_attribute.replace_A_and_B_in_category_name(
            self.showing_current_attribute_text_label)
        
        self.main.mainloop()

    def start(self):
        self.main.mainloop()

    def update_image(self, new_image):
        new_image = ImageTk.PhotoImage(new_image)
        self.c.background = new_image
        self.c.itemconfig(self.image_on_canvas, image=new_image)

    def click(self, event):

        if self.d == "disabled":
            return None
        if self.choosing_index < len(self.backend.list_of_players):
            clicked_country = get_country_by_position(self.c.canvasx(event.x),
                                                      self.c.canvasy(event.y))
            self.showing_country_label[
                "text"] = self.backend.active_player.name + " do you want to start with \n" + clicked_country.name + " ?"
            self.button_claim["command"] = lambda: self.claim_starting_country(
                self.backend.active_player, clicked_country)
            self.button_claim.pack(side="bottom")
            self.buttonframe2.pack(side="bottom")
            return None
        clicked_country = get_country_by_position(self.c.canvasx(event.x),
                                                  self.c.canvasy(event.y))
        if self.chosen_country_a == None:
            self.showing_country_label[
                "text"] = "It is the turn of " + self.backend.active_player.name + "\n You have chosen " + clicked_country.name + " currently controlled by " + clicked_country.owner_name
            if clicked_country.owner_name == self.backend.active_player.name:
                self.chosen_country_a = clicked_country
                self.backend.current_attribute.replace_A_and_B_in_category_name(
                    self.showing_current_attribute_text_label, self.chosen_country_a)

                self.showing_country_label[
                    "text"] = self.showing_country_label[
                        "text"] + "\n You can attack with this country"
        else:
            if self.peacemode and clicked_country.owner_name != "Nobody" and call_player_by_name(
                    clicked_country.owner_name) != self.backend.active_player:
                self.chosen_country_a = None
                self.showing_country_label[
                    "text"] = "You can not attack anoter player's countries in peace mode! \n Choose another country!"
                # time.sleep(5)
                # self.showingcountrylabel["text"]=""
                return None
            if clicked_country.is_connected_with(self.chosen_country_a):
                if self.backend.active_player != call_player_by_name(
                        clicked_country.owner_name):
                    self.backend.current_attribute.replace_A_and_B_in_category_name(
                        self.showing_current_attribute_text_label, self.chosen_country_a,
                        clicked_country)

                    self.showing_country_label[
                        "text"] = "Does the above sentence looks correct to you?"
                    self.button_sure["command"] = lambda: self.attack(
                        self.chosen_country_a, clicked_country)
                    self.button_not_sure["command"] = self.go_back
                    self.buttonframe.pack(side="bottom")
                    self.d = "disabled"
                else:
                    self.showing_country_label[
                        "text"] = "You already own this country"
            else:
                self.chosen_country_a = None
                self.showing_country_label[
                    "text"] = "These countries do not share a common land border.\n Please choose another pair!"
                self.backend.current_attribute.replace_A_and_B_in_category_name(self.showing_current_attribute_text_label)

    def find_distance(self, country_a: Country, country_b: Country) -> None:
        mydict = dict()
        myset = set(country_a.name)
        q = [[country_a.name, 0]]
        print(q)
        for country in all_countries_in_game:
            mydict[country.name] = country.neighboring_countries
        while country_b.name not in myset:
            temp = q[0]
            q.pop(0)
            for countryname in mydict[temp[0]]:
                if countryname in myset:
                    pass
                else:
                    myset.add(countryname)
                    q.append([countryname, temp[1] + 1])
                    if countryname == country_b.name:
                        return temp[1] + 1
            pass
        return None

    def attack(self, country_a: Country, country_b: Country):

        self.buttonframe.pack_forget()
        self.d = ""
        self.showing_country_label["text"] = ""
        self.chosen_country_a = None
        result = self.backend.active_player.check_if_attack_is_succesful(self.backend.current_attribute,
                                                                         country_a, country_b)
        if result == "no data":
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.backend.current_attribute,
                                    wl="no data")
            self.backend.current_attribute = self.backend.active_player.get_good_attribute()
            self.backend.current_attribute.replace_A_and_B_in_category_name(
                self.showing_current_attribute_text_label,
            )
            return None
        if result == "draw":
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.backend.current_attribute,
                                    wl="draw")
            self.backend.current_attribute = self.backend.active_player.get_good_attribute()
            self.backend.current_attribute.replace_A_and_B_in_category_name(
                self.showing_current_attribute_text_label,
            )
            return None
        if result == "hard defeat":
            self.claim_country(self.backend.active_player, country_b)
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.backend.current_attribute,
                                    wl="hard defeat")
            return None
        if result == "win":
            self.claim_country(self.backend.active_player, country_b)
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.backend.current_attribute,
                                    wl="you win!")

        else:
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.backend.current_attribute,
                                    wl="you loose!")
            if country_b.owner_name != "Nobody":
                self.claim_country(call_player_by_name(country_b.owner_name),
                                   country_a)

    def transition(self, same_player_again: bool = False):

        if not same_player_again:
            if self.backend.check_if_game_should_end():
                self.d = 'disabled'
                to_show_message: str = endscreen(cause='', triggered_player_name=self.backend.active_player.name,
                                                 winning_condition=self.winning_condition,
                                                 list_of_players=self.backend.list_of_players,
                                                 attached_backend=self.backend,
                                                 end_attribute=self.backend.end_attribute,
                                                 reversed_end_attribute=self.reversed_end_attribute,
                                                 winning_country=self.backend.winning_country,
                                                 dict_of_targets=self.backend.dict_of_targets,
                                                 dict_of_target_attribute_name=self.backend.dict_of_target_attribute_name,
                                                 )
                self.showing_country_label[
                    "text"] = to_show_message
                self.showing_current_attribute_text_label[
                    "text"] = to_show_message
                return None
            self.backend.active_player_counter = self.backend.active_player_counter + 1

        self.index = self.backend.active_player_counter % len(
            self.backend.list_of_players)

        if not same_player_again:
            if self.index == 0:
                self.turn_counter += 1

        # update the interface
        self.turn_counter_label["text"] = str(self.turn_counter)
        self.flagframe_dict[self.backend.active_player.name].pack_forget()
        self.backend.active_player = self.backend.list_of_players[self.index]
        self.showing_country_label[
            "text"] = "It is the turn of " + self.backend.active_player.name + "\n You have not chosen any country yet"

        # roll a new attribute
        self.backend.current_attribute = self.backend.active_player.get_good_attribute()
        self.backend.current_attribute.replace_A_and_B_in_category_name(
            self.showing_current_attribute_text_label)
        self.flagframe_dict[self.backend.active_player.name].pack(side="top")
        if self.wormhole_mode == "every round changing wormholes":
            if self.index == 0:
                try:
                    self.destroy_all_wormholes()
                except:
                    traceback.print_exc()
                self.activate_wormholes(3)
        if self.wormhole_mode == "every round changing wormholes from your countries":
            try:
                self.destroy_all_wormholes()
            except:
                traceback.print_exc()
            if len(self.backend.active_player.list_of_possessed_countries) >= 3:
                print("wormholes are getting activated")
                self.activate_wormholes(1, player=self.backend.active_player)
        self.reroll_button["text"] = "rerolls left:\n " + str(
            self.backend.active_player.rerolls_left)

    def go_back(self):
        # self.buttonsure.pack_forget()
        # self.buttonnotsure.pack_forget()
        self.buttonframe.pack_forget()
        self.chosen_country_a = None
        self.showing_country_label["text"] = ""
        self.backend.current_attribute.replace_A_and_B_in_category_name(self.showing_current_attribute_text_label)
        self.d = ""

    def claim_country(self, player: Player, country: Country):

        # backend
        old_player: Player = call_player_by_name(country.owner_name)
        self.backend.claim_country_backend(old_player, player, country)

        # frontend
        inv_map = {v: k for k, v in greencountrydict.items()}
        color = inv_map[country.name]
        np_image = np.array(green_image)
        green = np.array(color, dtype=np.uint8)
        greens = list(zip(*np.where(np.all((np_image == green), axis=-1))))

        for tuplen in greens:
            self.bild.putpixel((tuplen[1], tuplen[0]), player.color)

        # this is for the flagframe
        if player.name != "Nobody":
            if self.winning_condition != "get gold" or country in self.goldlist:
                frame = self.flagframe_dict[player.name]
                myimage = country.get_resized_flag(50)
                new_label = ttk.Label(frame, image=myimage)
                new_label.grid(row=0,
                               column=len(player.list_of_possessed_countries) +
                               1)
                new_label.bind("<Button-1>",
                               lambda x: self.popup_country_stats(country))
                player.labeldict[country] = new_label
                frame.current_flagdict[country] = myimage

        self.update_image(self.bild)

    def claim_starting_country(self, player: Player, country: Country):
        self.buttonframe2.pack_forget()
        self.claim_country(player, country)
        self.choosing_index = self.choosing_index + 1
        if self.choosing_index == len(self.backend.list_of_players):
            self.backend.active_player = self.backend.list_of_players[self.index]
            self.showing_country_label[
                "text"] = "It is the turn of " + self.backend.active_player.name + "\n You have not chosen any country yet"
            self.backend.current_attribute.replace_A_and_B_in_category_name(
                self.showing_current_attribute_text_label,
            )
            self.setupgame()
        else:
            self.backend.active_player = self.backend.list_of_players[self.random_people_start[
                self.choosing_index]]
            self.showing_current_attribute_text_label[
                "text"] = "Choose a starting country of your choice"
            self.showing_country_label[
                "text"] = self.backend.active_player.name + " Please choose a starting country"

    def callback(self, url):
        webbrowser.open_new(url)

    def popup_country_stats(self, country: Country):

        def _on_mousewheel(event):
            canvas21.yview_scroll(int(-1 * (float(event.delta) / 120)),
                                  "units")

        win2 = Toplevel()

        frame21 = ttk.Frame(win2)
        frame21.pack(fill="both", expand=True)
        canvas21 = ttk.Canvas(frame21)
        canvas21.pack(side="left", expand=True, fill="both")

        my_scrollbar12 = ttk.Scrollbar(frame21,
                                      orient="vertical",
                                      command=canvas21.yview)
        my_scrollbar12.pack(side="right", fill="y")
        my_scrollbar12.config(command=canvas21.yview)

        frame22 = ttk.Frame(canvas21)
        canvas21.create_window((0, 0), window=frame22, anchor="nw")
        win2.geometry("1650x825")
        frame22.bind(
            "<Configure>",
            lambda e: canvas21.configure(scrollregion=canvas21.bbox("all")))
        canvas21.bind_all("<MouseWheel>", _on_mousewheel)

        img = country.get_resized_flag(800)
        self.img221 = img
        panel = ttk.Label(frame22, image=img)
        panel.grid(column=0, row=0, columnspan=4, sticky="N")
        namelabel = ttk.Label(frame22, text=country.name, font="Helvetica 100")
        namelabel.grid(row=1, column=0, columnspan=4)

        mylist = list(country.dict_of_attributes.keys())
        mylist.sort(key=lambda x: x.lower())
        for index, item in enumerate(mylist):
            mylabel = ttk.Label(frame22,
                               text=item.replace(".csv", ""),
                               font="Helvetica 15")
            mylabel.grid(row=index + 2, column=0, pady=10)
            mylabel2 = ttk.Label(frame22,
                                text=country.dict_of_attributes[item].value,
                                font="Helvetica 15")
            try:
                mylabel3 = ttk.Label(frame22,
                                    text=country.dict_of_attributes[item].additional_information_name,
                                    font="Helvetica 15")
            except IndexError:
                mylabel3 = ttk.Label(frame22, text="--", font="Helvetica 15")
            mylabel2.grid(row=index + 2, column=1, pady=10)
            mylabel3.grid(row=index + 2, column=2, pady=10)
            mylabel4 = ttk.Label(frame22,
                                text=str(country.dict_of_attributes[item].rank) +
                                "/" +
                                str(
                                    country.dict_of_attributes[item].how_many_ranked),
                                font="Helvetica 15")
            mylabel4.grid(row=index + 2, column=3, pady=10)
        ddlist = [[propertyname, value.rank / value.how_many_ranked]
                  for propertyname, value in country.dict_of_attributes.items()]
        ddlist.sort(key=lambda x: x[1])
        print(ddlist)
        goodlist = ddlist[:5]
        ddlist = [[pname, value] for [pname, value] in ddlist
                  if country.dict_of_attributes[pname].value not in
                  [-1, -1.0, -9999.0, -9999]]
        badlist = ddlist[-5:]
        badlist.reverse()
        good_label = ttk.Label(frame22,
                              text=country.name + " is good in:",
                              font="Helvetica 15")
        bad_label = ttk.Label(frame22,
                             text=country.name + " is bad in:",
                             font="Helvetica 15")

        good_label.grid(row=len(mylist) + 3, column=0, columnspan=4, pady=20)
        for index, ditem in enumerate(goodlist):
            item = ditem[0]
            item = str(item)
            mylabel = ttk.Label(frame22,
                               text=str(item.replace(".csv", "")),
                               font="Helvetica 15")
            mylabel.grid(row=len(mylist) + index + 4, column=0, pady=10)
            mylabel2 = ttk.Label(frame22,
                                text=country.dict_of_attributes[item].value,
                                font="Helvetica 15")
            try:
                mylabel3 = ttk.Label(frame22,
                                    text=country.dict_of_attributes[item].additional_information_name,
                                    font="Helvetica 15")
            except IndexError:
                mylabel3 = ttk.Label(frame22, text="--", font="Helvetica 15")
            mylabel2.grid(row=index + 4 + len(mylist), column=1, pady=10)
            mylabel3.grid(row=index + 4 + len(mylist), column=2, pady=10)
            mylabel4 = ttk.Label(frame22,
                                text=str(country.dict_of_attributes[item].rank) +
                                "/" +
                                str(
                                    country.dict_of_attributes[item].how_many_ranked),
                                font="Helvetica 15")
            mylabel4.grid(row=index + 4 + len(mylist), column=3, pady=10)

        bad_label.grid(row=len(mylist) + 9, column=0, columnspan=4, pady=20)
        for index, ditem in enumerate(badlist):
            item = ditem[0]
            item = str(item)
            mylabel = ttk.Label(frame22,
                               text=item.replace(".csv", ""),
                               font="Helvetica 15")
            mylabel.grid(row=len(mylist) + index + 10, column=0, pady=10)
            mylabel2 = ttk.Label(frame22,
                                text=country.dict_of_attributes[item].value,
                                font="Helvetica 15")
            try:
                mylabel3 = ttk.Label(frame22,
                                    text=country.dict_of_attributes[item].additional_information_name,
                                    font="Helvetica 15")
            except IndexError:
                mylabel3 = ttk.Label(frame22, text="--", font="Helvetica 15")
            mylabel2.grid(row=index + 10 + len(mylist), column=1, pady=10)
            mylabel3.grid(row=index + 10 + len(mylist), column=2, pady=10)
            mylabel4 = ttk.Label(frame22,
                                text=str(country.dict_of_attributes[item].rank) +
                                "/" +
                                str(
                                    country.dict_of_attributes[item].how_many_ranked),
                                font="Helvetica 15")
            mylabel4.grid(row=index + 10 + len(mylist), column=3, pady=10)
        

    def activate_wormholes(self, numberofwormholes: int, player: Player | None = None) -> None:
        self.colorarray = [
            "cyan", "dark slate grey", "dark green", "dark violet",
            "dark goldenrod", "medium violet red", "brown2",
            "medium spring green", "grey2"
        ]

        def makeline_not_hidden(line):
            self.c.itemconfig(line, state=ttk.NORMAL)

        def makeline_hidden(line):
            self.c.itemconfig(line, state=ttk.HIDDEN)

        def create_good_line(country1: Country, country2: Country):
            ml = self.c.create_line(country1.wormhole_coordinates[0],
                                    country1.wormhole_coordinates[1],
                                    country2.wormhole_coordinates[0],
                                    country2.wormhole_coordinates[1],
                                    width=5,
                                    fill="black",
                                    dash=[5, 2],
                                    state=ttk.HIDDEN)
            self.linelist.append(ml)
            color = self.colorarray[random.randrange(0, len(self.colorarray))]
            self.colorarray.remove(color)
            startpoint = self.c.create_rectangle(
                country1.wormhole_coordinates[0] + 15,
                country1.wormhole_coordinates[1] + 15,
                country1.wormhole_coordinates[0] - 15,
                country1.wormhole_coordinates[1] - 15,
                fill="gray",
                # stipple="@my_stripple.xbm",
                outline=color,
                width=5)
            endpoint = self.c.create_rectangle(
                country2.wormhole_coordinates[0] + 15,
                country2.wormhole_coordinates[1] + 15,
                country2.wormhole_coordinates[0] - 15,
                country2.wormhole_coordinates[1] - 15,
                fill="gray",
                # stipple="@my_stripple.xbm",
                outline=color,
                width=5)
            self.pointlist.append(startpoint)
            self.pointlist.append(endpoint)
            self.c.tag_bind(startpoint, "<Enter>",
                            lambda x: makeline_not_hidden(ml))
            self.c.tag_bind(endpoint, "<Enter>",
                            lambda x: makeline_not_hidden(ml))
            self.c.tag_bind(startpoint, "<Leave>",
                            lambda x: makeline_hidden(ml))
            self.c.tag_bind(endpoint, "<Leave>", lambda x: makeline_hidden(ml))

        self.linelist = list()
        self.pointlist = list()
        country1 = Germany
        country2 = France
        if player != None:
            while (
                    country2.name in country1.neighboring_countries
                    or country1.name in country2.neighboring_countries
                    or country1.continent_name == country2.continent_name
                    or country2 in player.list_of_possessed_countries
                    or country1 == Unknown_country
                    or country2 == Unknown_country or
                (self.peacemode and
                 (country1.owner_name != "Nobody" and country2.owner_name != "Nobody"))):
                country1 = player.list_of_possessed_countries[random.randrange(
                    1, len(player.list_of_possessed_countries))]
                country2 = all_countries_in_game[random.randrange(
                    1, len(all_countries_in_game))]
            country1.neighboring_countries.append(country2.name)
            self.wormholed_countries.append([country1, country2])
            create_good_line(country1, country2)
            print(self.linelist)
            return None

        for _ in range(numberofwormholes):

            while (country2.name in country1.neighboring_countries
                   or country1.name in country2.neighboring_countries
                   or country1.continent_name == country2.continent_name):
                country1 = all_countries_in_game[random.randrange(
                    1, len(all_countries_in_game))]
                country2 = all_countries_in_game[random.randrange(
                    1, len(all_countries_in_game))]
            country1.neighboring_countries.append(country2.name)
            self.wormholed_countries.append([country1, country2])
            create_good_line(country1, country2)
            print(self.linelist)

    def destroy_all_wormholes(self):
        self.colorarray = [
            "indian red", "dark slate grey", "dark green", "dark violet",
            "dark goldenrod", "tomato3", "medium violet red", "brown2",
            "PaleGreen4"
        ]
        for item in self.wormholed_countries:
            item[0].neighboring_countries.remove(item[1].name)
        self.wormholed_countries = list()
        print("delete")
        print(self.linelist)
        for item in self.linelist:
            self.c.delete(item)
        for item in self.linelist:
            self.linelist.remove(item)

        for item in self.pointlist:
            self.c.delete(item)
        for item in self.pointlist:
            self.pointlist.remove(item)

    def popup_win_or_loose(self, country_a: Country, country_b: Country, property: Category, wl: str):

        def kill_guessed_correct():
            self.transition(same_player_again=True)
            self.win.destroy()

        def kill_button():
            if wl == "no data" or wl == "draw":
                self.transition(same_player_again=True)
            else:
                self.transition(same_player_again=False)
            self.win.destroy()

        def _on_mousewheel(event):
            canvas11.yview_scroll(int(-1 * (float(event.delta) / 120)),
                                  "units")

        self.win = Toplevel()
        additional_information = property.is_active
        # win.geometry("1400x825")
        frame11 = ttk.Frame(self.win)
        frame11.pack(fill="both", expand=True)
        canvas11 = ttk.Canvas(frame11)
        canvas11.pack(side="left", expand=True, fill="both")

        my_scrollbar11 = ttk.Scrollbar(frame11,
                                      orient="vertical"
                                      )
        my_scrollbar11.config(command=canvas11.yview)
        my_scrollbar11.pack(side="right", fill="y")

        frame12 = ttk.Frame(canvas11)
        canvas11.create_window((0, 0), window=frame12, anchor="nw")

        frame12.bind(
            "<Configure>",
            lambda e: canvas11.configure(scrollregion=canvas11.bbox("all")))

        canvas11.bind_all("<MouseWheel>", _on_mousewheel)

        url1 = "pictures/flag_pictures/w320/" + country_a.get_two_country_code(
        ).lower() + ".png"
        print(country_b.get_two_country_code())
        print("das war der Code")
        url2 = "pictures/flag_pictures/w320/" + country_b.get_two_country_code(
        ).lower() + ".png"
        img1 = ImageTk.PhotoImage(Image.open(url1))
        img2 = ImageTk.PhotoImage(Image.open(url2))
        frame12.img1 = img1
        frame12.img2 = img2
        panel1 = ttk.Label(frame12, image=img1)
        panel2 = ttk.Label(frame12, image=img2)

        url3 = "pictures/success3.png"
        url4 = "pictures/fail2.png"
        url5 = "pictures/vs.png"
        url6 = "pictures/no_data.png"
        url7 = "pictures/draw.png"
        url8 = "pictures/top5.png"
        url9 = "pictures/worst5.png"
        url10 = "pictures/great_success.png"

        img3 = ImageTk.PhotoImage(Image.open(url3))
        img4 = ImageTk.PhotoImage(Image.open(url4))
        img5 = ImageTk.PhotoImage(Image.open(url5))
        img6 = ImageTk.PhotoImage(Image.open(url6))
        img7 = ImageTk.PhotoImage(Image.open(url7))
        img8 = ImageTk.PhotoImage(Image.open(url8))
        img9 = ImageTk.PhotoImage(Image.open(url9))
        img10 = ImageTk.PhotoImage(Image.open(url10))

        frame12.img3 = img3
        frame12.img4 = img4
        frame12.img5 = img5
        frame12.img6 = img6
        frame12.img7 = img7
        frame12.img8 = img8
        frame12.img9 = img9
        frame12.img10 = img10

        panel3 = ttk.Label(frame12, image=img3)
        panel4 = ttk.Label(frame12, image=img4)
        panel5 = ttk.Label(frame12, image=img5)
        panel6 = ttk.Label(frame12, image=img6)
        panel7 = ttk.Label(frame12, image=img7)
        panel8_1 = ttk.Label(frame12, image=img8)
        panel8_2 = ttk.Label(frame12, image=img8)

        panel9_1 = ttk.Label(frame12, image=img9)
        panel9_2 = ttk.Label(frame12, image=img9)

        try:
            displayed_world_rank_a = str(
                country_a.dict_of_attributes[property.name].rank) if country_a.dict_of_attributes[property.name].rank != -1 else "--"
            displayed_how_many_ranked_a = str(
                country_a.dict_of_attributes[property.name].how_many_ranked) if country_a.dict_of_attributes[property.name].how_many_ranked != 1 else "--"

            l1 = ttk.Label(frame12, text=country_a.name + "\n" + property.name.replace(".csv", "") + "\n" +
                          format((country_a.dict_of_attributes[property.name].value), ",") + "\n" +
                          "worldrank:" +
                          displayed_world_rank_a
                          + "\n (of " + displayed_how_many_ranked_a + " countries ranked)", font="Helvetica 25", wraplength=500)
        except:
            l1 = ttk.Label(frame12,
                          text=country_a.name + "\n" +
                          property.name.replace(".csv", "") + "\n" +
                          "sorry no data",
                          font="Helvetica 25")

        try:
            displayed_world_rank_b = str(
                country_b.dict_of_attributes[property.name].rank) if country_b.dict_of_attributes[property.name].rank != -1 else "--"
            displayed_how_many_ranked_b = str(
                country_b.dict_of_attributes[property.name].how_many_ranked) if country_b.dict_of_attributes[property.name].how_many_ranked != 1 else "--"

            l2 = ttk.Label(
                frame12,
                text=country_b.name + "\n" + property.name.replace(".csv", "") +
                "\n" + format(
                    (country_b.dict_of_attributes[property.name].value), ",") +
                "\n" + "worldrank:" +
                displayed_world_rank_b + "\n (of " +
                displayed_how_many_ranked_b +
                " countries ranked)",
                font="Helvetica 25",
                wraplength=500)
        except:
            traceback.print_exc()
            l2 = ttk.Label(frame12,
                          text=country_b.name + "\n" +
                          property.name.replace(".csv", "") + "\n" +
                          "sorry no data",
                          font="Helvetica 25")

        killbutton = ttk.Button(frame12,
                               image=img7,
                               command=kill_button,
                               width=400,
                               )

        l1.grid(row=1, column=0)
        l2.grid(row=1, column=2)

        panel1.grid(row=0, column=0)
        panel2.grid(row=0, column=2)
        panel5.grid(row=0, column=1)
        killbutton.grid(row=2, column=1)

        if wl == "you win!":
            killbutton["image"] = img3
            killbutton["width"] = 300
            killbutton["height"] = 300
            # panel3.grid(row=2,column=1)

        if wl == "you loose!":
            killbutton["image"] = img4
            killbutton["width"] = 300
            killbutton["height"] = 300

        if wl == "no data":
            killbutton["image"] = img6
            killbutton["width"] = 300
            killbutton["height"] = 300

        if wl == "draw":
            killbutton["image"] = img7
            killbutton["width"] = 300
            killbutton["height"] = 300

        if wl == "hard defeat":
            killbutton["image"] = img10
            killbutton["width"] = 300
            killbutton["height"] = 300
            killbutton.configure(command=kill_guessed_correct)

        if additional_information:
            guessed_correct_button = ttk.Button(frame12,
                                               text="guessed correct",
                                               command=kill_guessed_correct)
            guessed_correct_button.grid(row=3, column=1)
            try:
                wiki_summary_A_extra = country_a.dict_of_attributes[
                    property.name].additional_information
                wiki_summary_B_extra = country_b.dict_of_attributes[
                    property.name].additional_information
                wikiurl_A = country_a.dict_of_attributes[property.name].wikipedia_link
                wikiurl_B = country_b.dict_of_attributes[property.name].wikipedia_link
            except:
                traceback.print_exc()
                wiki_summary_A_extra = ""
                wiki_summary_B_extra = ""
                wikiurl_A = ""
                wikiurl_B = ""
            height = 320
            try:

                urlA = "pictures/attribute_pictures/" + property.name.replace(
                    ".csv", "") + "/" + country_a.dict_of_attributes[
                        property.name].additional_information_name + ".jpg"
                try:
                    imgA = Image.open(urlA)
                except FileNotFoundError:
                    imgA = Image.open("pictures/no_image_available.png")
                w = float(imgA.width)
                h = float(imgA.height)
                imgA = ImageTk.PhotoImage(
                    imgA.resize((int(height * w / h), int(height)),
                                Image.LANCZOS))
                frame12.imgA = imgA
                panelA = ttk.Label(frame12, image=imgA)
                panelA.grid(row=2, column=0)
                panelA_extra = ttk.Label(
                    frame12,
                    text=country_a.dict_of_attributes[property.name].additional_information_name,
                    font="Helvetica 20",
                    wraplength=500)
                panelA_extra.grid(row=3, column=0)
            except:
                traceback.print_exc()
            try:

                urlB = "pictures/attribute_pictures/" + property.name.replace(
                    ".csv", "") + "/" + country_b.dict_of_attributes[
                        property.name].additional_information_name + ".jpg"
                try:
                    imgB = Image.open(urlB)
                except FileNotFoundError:
                    imgB = Image.open("pictures/no_image_available.png")
                w = float(imgB.width)
                h = float(imgB.height)
                imgB = ImageTk.PhotoImage(
                    imgB.resize((int(height * w / h), int(height)),
                                Image.LANCZOS))
                frame12.imgB = imgB

                panelB = ttk.Label(frame12, image=imgB)

                panelB.grid(row=2, column=2)

                panelB_extra = ttk.Label(
                    frame12,
                    text=country_b.dict_of_attributes[property.name].additional_information_name,
                    font="Helvetica 20",
                    wraplength=500)

                panelB_extra.grid(row=3, column=2)
            except:
                traceback.print_exc()
            try:
                if country_a.dict_of_attributes[
                        property.name].additional_information_name != country_a.name:
                    if wikiurl_A == "":
                        self.search_string = country_a.dict_of_attributes[
                            property.name].additional_information_name
                        self.search_string = wikipedia.search(
                            self.search_string)[0]
                        print(self.search_string)
                        print(wikipedia.search(self.search_string)[0])
                        print(self.search_string)
                        wiki_url_A = wikipedia.page(self.search_string).url
                        print("hier kommt url")
                        print(type(wiki_url_A))
                        print(wiki_url_A)
                        wiki_summary_A = wikipedia.summary(self.search_string,
                                                           sentences=2)
                    else:
                        wiki_url_A = wikiurl_A
                        wiki_summary_A = wiki_summary_A_extra

                    wiki_url_A_Label = ttk.Label(frame12,
                                                text=wiki_url_A,
                                                cursor="hand2",
                                                font="Helvetica 15")
                    wiki_url_A_Label.bind("<Button-1>",
                                          lambda x: self.callback(wiki_url_A))

                    wiki_summary_A_Label = ttk.Label(frame12,
                                                    text=wiki_summary_A,
                                                    wraplength=500,
                                                    font="Helvetica 15")
                    wiki_summary_A_Label.grid(row=4, column=0)
                    wiki_url_A_Label.grid(row=5, column=0)
            except:
                traceback.print_exc()
            try:
                if country_b.dict_of_attributes[
                        property.name].additional_information_name != country_b.name:
                    if wikiurl_B == "":
                        self.search_string = country_b.dict_of_attributes[
                            property.name].additional_information_name
                        self.search_string = wikipedia.search(
                            self.search_string)[0]
                        print(self.search_string)
                        print(wikipedia.search(self.search_string)[0])
                        print(self.search_string)
                        wiki_url_B = wikipedia.page(self.search_string).url
                        print("hier kommt url")
                        print(type(wiki_url_B))
                        print(wiki_url_B)
                        wiki_summary_B = wikipedia.summary(self.search_string,
                                                           sentences=2)

                    else:
                        wiki_url_B = wikiurl_B
                        wiki_summary_B = wiki_summary_B_extra

                    wiki_url_B_Label = ttk.Label(frame12,
                                                text=wiki_url_B,
                                                fg="blue",
                                                cursor="hand2",
                                                font="Helvetica 15",
                                                wraplength=500)
                    wiki_url_B_Label.bind("<Button-1>",
                                          lambda x: self.callback(wiki_url_B))

                    wiki_summary_B_Label = ttk.Label(frame12,
                                                    text=wiki_summary_B,
                                                    wraplength=500,
                                                    font="Helvetica 15")
                    wiki_summary_B_Label.grid(row=4, column=2)
                    wiki_url_B_Label.grid(row=5, column=2)
            except:
                traceback.print_exc()

        try:
            countrya_top5 = country_a.dict_of_attributes[property.name].rank < 6
        except:
            countrya_top5 = False

        try:
            countryb_top5 = country_b.dict_of_attributes[property.name].rank < 6
        except:
            countryb_top5 = False

        try:
            countrya_worst5 = country_a.dict_of_attributes[property.name].how_many_ranked - \
                country_a.dict_of_attributes[property.name].rank < 6
        except:
            countrya_worst5 = False

        try:
            countryb_worst5 = country_b.dict_of_attributes[property.name].how_many_ranked - \
                country_b.dict_of_attributes[property.name].rank < 6
        except:
            countryb_worst5 = False

        if countrya_top5:
            panel8_1.grid(row=6, column=0)

        if countryb_top5:
            panel8_2.grid(row=6, column=2)

        if countrya_worst5:
            panel9_1.grid(row=6, column=0)

        if countryb_worst5:
            panel9_2.grid(row=6, column=2)

    def setupclaim2countries(self):
        Target = Player(realgrey, "Nobody")
        if self.choosing_index == len(self.backend.list_of_players):
            self.targetcountry1 = all_countries_in_game[random.randrange(
                1, len(all_countries_in_game))]
            self.targetcountry2 = all_countries_in_game[random.randrange(
                1, len(all_countries_in_game))]
            if self.targetcountry1.name == self.targetcountry2.name:
                self.targetcountry2 = all_countries_in_game[random.randrange(
                    1, len(all_countries_in_game))]
            self.claim_country(Target, self.targetcountry1)
            print(self.targetcountry1.name)
            self.claim_country(Target, self.targetcountry2)

    def setupgold(self):

        self.goldids: list[int] = []

        def get_good_ids(numberofgold: int):
            self.goldids = random.sample(range(len(all_countries_in_game)),
                                         numberofgold)
            for i in self.goldids:
                if all_countries_in_game[i].owner_name != "Nobody" or all_countries_in_game[
                        i].name == "Unknown Country":
                    get_good_ids(numberofgold)
            return None

        for player in self.backend.list_of_players:
            player.gold = 0
        Target = Player(gold, "Nobody")
        self.numberofgold = len(all_countries_in_game) // 20
        print(self.numberofgold)
        get_good_ids(self.numberofgold)
        for i in self.goldids:
            self.claim_country(Target, all_countries_in_game[i])
            self.goldlist.append(all_countries_in_game[i])

    def setup_starting_attribute(self) -> Category:

        if self.pred_attribute_name != "Random":
            print(self.pred_attribute_name)
            attribute = dictionary_attribute_name_to_attribute[
                self.pred_attribute_name][0]

        else:
            numberofnodata = 999999
            while numberofnodata > 5:
                attribute = mr_nobody.get_random_attribute_with_cluster()
                numberofnodata = 0
                for country in all_countries_in_game:

                    if country.dict_of_attributes[attribute.name].rank == -1:
                        numberofnodata += 1

            if random.random() < 0.5:

                text: str = "The target attribute is " + attribute.name
                ttk.messagebox.showinfo(self.main, message=text)
                self.reversed_end_attribute = 0

            else:
                self.reversed_end_attribute = 1
                text = "The target attribute is " + attribute.name + "\n REVERSED!!!"
                ttk.messagebox.showinfo(self.main, message=text)

        return attribute

    def setuppredattribute(self):
        self.backend.end_attribute = self.setup_starting_attribute()
        if True:
            self.grey_no_data()

    def grey_no_data(self):
        for country in all_countries_in_game:
            if country == Unknown_country:
                continue
            try:
                country.dict_of_attributes[self.backend.end_attribute.name].value
            except:
                print(country.name)
                traceback.print_exc()
                self.claim_country(No_Data_Body, country)

    def setup_secret_target_countries(self, numberoftargets: int):
        self.really_unknown = Unknown_country

        def checkcountrylist(list1: list[Country]):
            for country in list1:
                if country.owner_name != "Nobody" or country == self.really_unknown:
                    return False
            return True

        def roll_random_country(_):
            return all_countries_in_game[random.randrange(1, len(all_countries_in_game))]

        def show_targets(player: Player):
            self.no_targets_yetlist.remove(player)
            self.target_countries_frame = ttk.Toplevel()
            targetlist = [Unknown_country] * numberoftargets
            while (not checkcountrylist(targetlist)):
                targetlist = [roll_random_country(item) for item in targetlist]

            welcomelabel = ttk.Label(
                self.target_countries_frame,
                text="Welcome " + player.name +
                " those are your countries\n if you don't know where these are feel free to look at the map.",
                font="Helvetica 25")
            welcomelabel.grid(row=0, column=0, columnspan=len(targetlist))
            self.myimage = [0] * numberoftargets
            self.created_circles = list()
            for index, country in enumerate(targetlist):
                item = self.c.create_oval(country.wormhole_coordinates[0] + 20,
                                          country.wormhole_coordinates[1] + 20,
                                          country.wormhole_coordinates[0] - 20,
                                          country.wormhole_coordinates[1] - 20,
                                          width=3,
                                          outline="red")
                self.created_circles.append(item)
                newcountrylabel = ttk.Label(self.target_countries_frame,
                                           text=country.name,
                                           font="Helvetica 25")
                newcountrylabel.grid(row=1, column=index)
                self.myimage[index] = country.get_resized_flag(400)
                newlabel = ttk.Label(self.target_countries_frame,
                                    image=self.myimage[index],
                                    pady=40)
                newlabel.grid(row=2, column=index)
                pass
            self.backend.dict_of_targets[player] = targetlist
            self.got_targets_Button = ttk.Button(self.target_countries_frame,
                                                text="got it",
                                                command=open_next_frame,
                                                font="Helvetica 25")
            self.got_targets_Button.grid(row=3,
                                         column=0,
                                         columnspan=len(targetlist) + 2)

        def open_next_frame():
            for item in self.created_circles:
                self.c.delete(item)
            self.created_circles = []
            self.target_countries_frame.destroy()
            if len(self.no_targets_yetlist) == 0:
                return None
            show_targets(self.no_targets_yetlist[0])

        self.no_targets_yetlist = self.backend.list_of_players.copy()
        show_targets(self.backend.active_player)

    def setup_secret_attribute(self, n: int):
        self.target_countries_frame: ttk.Toplevel
        self.got_targets_Button: ttk.Button
        self.target_attribute_name: str

        def open_next_frame():
            self.target_countries_frame.destroy()
            if len(self.no_targets_yetlist) == 0:
                return None
            show_targets(self.no_targets_yetlist[0])

        def show_targets(player: Player):
            self.no_targets_yetlist.remove(player)
            self.target_countries_frame = ttk.Toplevel()
            self.target_attribute_name = player.get_random_attribute_with_cluster().name
            self.backend.dict_of_target_attribute_name[player] = self.target_attribute_name
            welcomelabel = ttk.Label(self.target_countries_frame,
                                    text="Welcome " + player.name +
                                    "your attribute is the following: \n\n" +
                                    self.target_attribute_name.rstrip(".csv") +
                                    "\n\nclaim one of the top " + str(n) +
                                    " countries in order to win the game",
                                    font="Helvetica 25")
            welcomelabel.grid(row=0, column=0)
            self.backend.dict_of_targets[player] = self.backend.find_top_n_countries(
                n, self.target_attribute_name)
            self.got_targets_Button = ttk.Button(self.target_countries_frame,
                                                text="got it",
                                                command=open_next_frame,
                                                )
            self.got_targets_Button.grid(row=3, column=0)

        self.backend.dict_of_targets = dict()
        self.no_targets_yetlist = self.backend.list_of_players.copy()
        show_targets(self.backend.active_player)

    def setupgame(self):

        if self.wormhole_mode == "fixed starting wormholes":
            self.activate_wormholes(5)
        if self.wormhole_mode == "every round changing wormholes":
            self.activate_wormholes(3)

        if self.winning_condition == "claim 2 countries":
            self.setupclaim2countries()
        if self.winning_condition == "get gold":
            self.setupgold()
        if self.winning_condition == "attribute":
            self.setuppredattribute()
        if self.winning_condition == "secret targets":
            self.setup_secret_target_countries(self.number_of_targets)
        if self.winning_condition == "secret attribute":
            self.setup_secret_attribute(5)

    def scroll_start(self, event):
        self.c.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.c.scan_dragto(event.x, event.y, gain=1)

    def do_zoom(self, event):
        x = self.c.canvasx(event.x)
        y = self.c.canvasy(event.y)
        factor = 1.001**event.delta
        self.c.scale(ttk.ALL, x, y, factor, factor)
