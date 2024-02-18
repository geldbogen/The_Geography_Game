import tkinter as tk
from PIL import ImageTk, Image
import sv_ttk
import random
import traceback
import numpy as np
import time
import wikipedia
import webbrowser

from local_attribute import LocalAttribute
from country import Country, get_country_by_position, Unknown_country, Germany, France
from category import Category
from player import Player, call_player_by_name, No_Data_Body, mr_nobody
from image import greencountrydict, green_image
from global_definitions import all_categories, all_countries_in_game, dictionary_attribute_name_to_attribute, gold, realgrey

class MainWindow():

    def __init__(self,
                 bild,
                 list_of_players: list[Player],
                 wormhole_mode,
                 starting_countries_preferences="random",
                 number_of_rounds=99999999999,
                 winning_condition="number of countries",
                 number_of_wormholes=3,
                 pred_attribute="random",
                 peacemode=0,
                 reversed_end_attribute=0):

        self.rerolls = 3
        self.number_of_targets = 2
        self.pred_attribute_name = pred_attribute
        self.winning_condition = winning_condition
        self.flagframe_dict = dict()
        self.number_of_rounds = number_of_rounds
        self.index = 0
        self.goldlist = list()
        self.choosing_index = -1
        self.starting_countries = starting_countries_preferences
        self.reversed_end_attribute = reversed_end_attribute
        self.main = tk.Tk()
        sv_ttk.set_theme("dark")  # Set light theme

        self.list_of_players = list_of_players
        print(self.list_of_players)
        print(len(list_of_players))
        self.active_player_counter = 0
        self.active_player = self.list_of_players[self.active_player_counter]
        self.number_of_players = len(self.list_of_players)
        self.end_attribute = None
        self.wormhole_mode = wormhole_mode
        self.wormholed_countries = list()
        self.number_of_wormholes = number_of_wormholes
        print(self.winning_condition)

        self.peacemode = peacemode

        self.current_attribute = all_categories[0]

        self.chosen_country_a = None
        self.turn_counter = 0

        self.frame1 = tk.Frame(self.main, width=300, height=300)
        self.frame1.pack(side="bottom", fill="both", expand=True)

        # frame1=frame2+areyousurebuttons

        self.frame2 = tk.Frame(self.frame1)
        # frame2= frame3 + flags

        self.frame3 = tk.Frame(self.frame2)
        self.buttonframe = tk.Frame(self.frame1)
        self.buttonframe2 = tk.Frame(self.frame1)
        self.bild = bild
        self.c = tk.Canvas(self.frame3, bg="white", width=1000, height=600)

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

        for player in self.list_of_players:
            self.flagframe_dict[player.name] = tk.Frame(self.frame2)
            self.flagframe_dict[player.name].current_flagdict = dict()

        self.c.bind("<ButtonPress-1>", self.click)

        self.c.bind("<ButtonPress-3>", self.scroll_start)
        self.c.bind("<B3-Motion>", self.scroll_move)

        # unpacking
        self.frame3.pack(side="bottom", expand=True, fill="both")
        self.frame2.pack(side="top", expand=True, fill="both")
        self.frame1.pack(side="top", expand=True, fill="both")
        self.frame4 = tk.Frame(self.frame3)
        self.frame5 = tk.Frame(self.frame3)

        self.reroll_button = tk.Button(
            self.frame5,
            text="rerolls left:\n " + str(self.active_player.rerolls_left),
            font="Helvetica 25",
            anchor="sw",
            command=lambda: self.active_player.reroll(to_update_category_label=self.showing_current_attribute_text_label, to_update_reroll_button_label=self.reroll_button['text']))

        self.reroll_button.pack(side="left", fill="y")

        self.showing_country_label = tk.Label(
            self.frame5,
            text="It is the turn of " + self.active_player.name +
            "\n You have not chosen any country yet",
            font="Helvetica 25")
        self.showing_country_label.pack(side="bottom",
                                        expand=True,
                                        fill="both")

        self.turn_counter_label = tk.Label(self.frame4,
                                           text=str(self.turn_counter),
                                           font="Helvetica 50")
        self.turn_counter_label.pack(side="right")

        self.showing_current_attribute_text_label = tk.Label(
            self.frame4, text="Welcome!", font="Helvetica 25")
        self.showing_current_attribute_text_label.pack(anchor="nw",
                                                       expand=True,
                                                       fill="both")

        self.frame4.pack(side="top", fill="x")
        self.frame5.pack(side="bottom", fill="x")

        self.c.pack(side="top", fill="both", expand=True)

        self.button_sure = tk.Button(self.buttonframe,
                                     text="Attack!",
                                     font="Helvetica 20")
        self.button_not_sure = tk.Button(self.buttonframe,
                                         text="No go back",
                                         font="Helvetica 20")
        self.button_sure.pack(side="left")
        self.button_not_sure.pack(side="right")
        self.button_claim = tk.Button(self.buttonframe2,
                                      text="Yes Please!",
                                      font="Helvetica 20")

        self.d = ""
        self.random_people_start = random.sample(
            range(0, len(self.list_of_players)), len(self.list_of_players))

        # usher choosing countries procedure if that mode was chosen
        if self.starting_countries == "choose":
            self.choosing_index = 0
            self.active_player = self.list_of_players[self.random_people_start[
                self.choosing_index]]
            self.showing_current_attribute_text_label[
                "text"] = "Choose a starting country of your choice"
            self.showing_country_label[
                "text"] = self.active_player.name + "\n Please choose a starting country"

        # roll starting countries for the players
        # TODO take care of ending attribute
        if self.starting_countries == "random":
            self.choosing_index = len(self.list_of_players)
            self.setupgame()
            while True:
                j = 0
                self.randomstart = random.sample(range(0, len(all_countries_in_game)),
                                                 len(self.list_of_players))
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
                                self.end_attribute.name].value
                        except:
                            j = 1
                if j == 0:
                    break
            for i in range(len(self.list_of_players)):
                self.claim_country(self.list_of_players[i],
                                   all_countries_in_game[self.randomstart[i]])
                print(all_countries_in_game[self.randomstart[i]].name)

        # roll first attribute
        self.current_attribute = self.active_player.get_good_attribute()
        self.current_attribute.replace_A_and_B_in_category_name(
            self.showing_current_attribute_text_label)

    def start(self):
        self.main.mainloop()

    def update_image(self, new_image):
        new_image = ImageTk.PhotoImage(new_image)
        self.c.background = new_image
        self.c.itemconfig(self.image_on_canvas, image=new_image)

    def click(self, event):

        if self.d == "disabled":
            return None
        if self.choosing_index < len(self.list_of_players):
            clicked_country = get_country_by_position(self.c.canvasx(event.x),
                                                      self.c.canvasy(event.y))
            self.showing_country_label[
                "text"] = self.active_player.name + " do you want to start with \n" + clicked_country.name + " ?"
            self.button_claim["command"] = lambda: self.claim_starting_country(
                self.active_player, clicked_country)
            self.button_claim.pack(side="bottom")
            self.buttonframe2.pack(side="bottom")
            return None
        clicked_country = get_country_by_position(self.c.canvasx(event.x),
                                                  self.c.canvasy(event.y))
        if self.chosen_country_a == None:
            self.showing_country_label[
                "text"] = "It is the turn of " + self.active_player.name + "\n You have chosen " + clicked_country.name + " currently controlled by " + clicked_country.owner
            if clicked_country.owner == self.active_player.name:
                self.chosen_country_a = clicked_country
                self.current_attribute.replace_A_and_B_in_category_name(
                    self.showing_current_attribute_text_label, self.chosen_country_a)

                self.showing_country_label[
                    "text"] = self.showing_country_label[
                        "text"] + "\n You can attack with this country"
        else:
            if self.peacemode == 1 and clicked_country.owner != "Nobody" and call_player_by_name(
                    clicked_country.owner) != self.active_player:
                self.chosen_country_a = None
                self.showing_country_label[
                    "text"] = "You can not attack anoter player's countries in peace mode! \n Choose another country!"
                # time.sleep(5)
                # self.showingcountrylabel["text"]=""
                return None
            if clicked_country.is_connected_with(self.chosen_country_a):
                if self.active_player != call_player_by_name(
                        clicked_country.owner):
                    self.current_attribute.replace_A_and_B_in_category_name(
                        self.showing_current_attribute_text_label, self.chosen_country_a,
                        clicked_country)

                    self.showing_country_label[
                        "text"] = "Does the above sentence looks correct to you?"
                    self.button_sure["command"] = lambda: self.attack(
                        self.chosen_country_a, clicked_country)
                    self.button_not_sure["command"] = self.fuckgoback
                    self.buttonframe.pack(side="bottom")
                    self.d = "disabled"
                else:
                    self.showing_country_label[
                        "text"] = "You already own this country"
            else:
                self.chosen_country_a = None
                self.showing_country_label[
                    "text"] = "These countries do not share a common land border.\n Please choose another pair!"

    def find_distance(self, country_a: Country, country_b: Country):
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
        result = self.active_player.check_if_attack_is_succesful(self.current_attribute.name,
                                                          country_a, country_b)
        if result == "no data":
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.current_attribute,
                                    wl="no data")
            self.current_attribute = self.active_player.get_good_attribute()
            self.current_attribute.replace_A_and_B_in_category_name(
                self.showing_current_attribute_text_label,
            )
            return None
        if result == "draw":
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.current_attribute,
                                    wl="draw")
            self.current_attribute = self.active_player.get_good_attribute()
            self.current_attribute.replace_A_and_B_in_category_name(
                self.showing_current_attribute_text_label,
            )
            return None
        if result == "hard defeat":
            self.claim_country(self.active_player, country_b)
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.current_attribute,
                                    wl="hard defeat")
            return None
        if result == "win":
            self.claim_country(self.active_player, country_b)
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.current_attribute,
                                    wl="you win!")

        else:
            self.popup_win_or_loose(country_a,
                                    country_b,
                                    self.current_attribute,
                                    wl="you loose!")
            if country_b.owner != "Nobody":
                self.claim_country(call_player_by_name(country_b.owner),
                                   country_a)

    def transition(self, same_player_again=False):

        if not same_player_again:
            if self.check_if_game_should_end():
                return None
            self.active_player_counter = self.active_player_counter + 1
        self.index = self.active_player_counter % len(self.list_of_players)

        if not same_player_again:
            if self.index == 0:
                self.turn_counter += 1

        # update the interface
        self.turn_counter_label["text"] = str(self.turn_counter)
        self.flagframe_dict[self.active_player.name].pack_forget()
        self.active_player = self.list_of_players[self.index]
        self.showing_country_label[
            "text"] = "It is the turn of " + self.active_player.name + "\n You have not chosen any country yet"

        # roll a new attribute
        self.current_attribute = self.active_player.get_good_attribute()
        self.current_attribute.replace_A_and_B_in_category_name(
            self.showing_current_attribute_text_label)
        self.flagframe_dict[self.active_player.name].pack(side="top")
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
            if len(self.active_player.list_of_possessed_countries) >= 3:
                print("wormholes werden aktiviert")
                self.activate_wormholes(1, player=self.active_player)
        self.reroll_button["text"] = "rerolls left:\n " + str(
            self.active_player.rerolls_left)

    def fuckgoback(self):
        # self.buttonsure.pack_forget()
        # self.buttonnotsure.pack_forget()
        self.buttonframe.pack_forget()
        self.chosen_country_a = None
        self.showing_country_label["text"] = ""
        self.d = ""

    def claim_country(self, player: Player, country: Country):

        def changethingswhencountryclicked(country):
            clicked_country = country
            if self.chosen_country_a == None:
                self.showing_country_label[
                    "text"] = "It is the turn of " + self.active_player.name + "\n You have chosen " + clicked_country.name + " currently controlled by " + clicked_country.owner
                if clicked_country.owner == self.active_player.name:
                    self.chosen_country_a = clicked_country
                    self.showing_country_label[
                        "text"] = self.showing_country_label[
                            "text"] + "\n You can attack with this country"
            else:
                if clicked_country.is_connected_with(
                        self.chosen_country_a):
                    if self.active_player != call_player_by_name(
                            clicked_country.owner):
                        self.showing_country_label[
                            "text"] = "You want to attack  " + clicked_country.name + " currently controlled by " + clicked_country.owner + " with " + self.chosen_country_a.name + " are you sure?"
                        self.button_sure["command"] = lambda: self.attack(
                            self.chosen_country_a, clicked_country)
                        self.button_not_sure["command"] = self.fuckgoback
                        self.buttonframe.pack(side="bottom")
                        self.d = "disabled"
                    else:
                        self.showing_country_label[
                            "text"] = "You already own this country"
                else:
                    self.chosen_country_a = None
                    self.showing_country_label[
                        "text"] = "Those countries do not share a common land border. Please choose another pair"
                    time.wait(5)
                    self.showing_country_label["text"] = ""

        player.list_of_possessed_countries.append(country)
        old_owner = country.owner
        country.owner = player.name

        inv_map = {v: k for k, v in greencountrydict.items()}
        color = inv_map[country.name]
        np_image = np.array(green_image)
        green = np.array(color, dtype=np.uint8)
        greens = list(zip(*np.where(np.all((np_image == green), axis=-1))))

        for tuplen in greens:
            self.bild.putpixel((tuplen[1], tuplen[0]), player.color)

        if player.name != "Nobody":
            if self.winning_condition != "get gold" or country in self.goldlist:
                frame = self.flagframe_dict[player.name]
                myimage = country.get_resized_flag(50)
                new_label = tk.Label(frame, image=myimage)
                new_label.grid(row=0,
                               column=len(player.list_of_possessed_countries) +
                               1)
                new_label.bind("<Button-1>",
                               lambda x: self.popup_country_stats(country))
                player.labeldict[country] = new_label
                frame.current_flagdict[country] = myimage

        if old_owner != "Nobody" and not self.winning_condition in [
                "get gold"
        ]:
            call_player_by_name(old_owner).list_of_possessed_countries.remove(
                country)
            call_player_by_name(old_owner).labeldict[country].destroy()

        self.update_image(self.bild)

        if self.winning_condition == "get gold":
            if player.name != "Nobody":
                if country in self.goldlist:
                    player.gold = player.gold + 1
                    self.goldlist.remove(country)
                    player.list_of_possessed_countries_gold.append(country)

    def claim_starting_country(self, player: Player, country: Country):
        self.buttonframe2.pack_forget()
        self.claim_country(player, country)
        self.choosing_index = self.choosing_index + 1
        if self.choosing_index == len(self.list_of_players):
            self.active_player = self.list_of_players[self.index]
            self.showing_country_label[
                "text"] = "It is the turn of " + self.active_player.name + "\n You have not chosen any country yet"
            self.current_attribute.replace_A_and_B_in_category_name(
                self.showing_current_attribute_text_label,
            )
            self.setupgame()
        else:
            self.active_player = self.list_of_players[self.random_people_start[
                self.choosing_index]]
            self.showing_current_attribute_text_label[
                "text"] = "Choose a starting country of your choice"
            self.showing_country_label[
                "text"] = self.active_player.name + " Please choose a starting country"

    def callback(self, url):
        webbrowser.open_new(url)

    def popup_country_stats(self, country: Country):

        def _on_mousewheel(event):
            canvas21.yview_scroll(int(-1 * (float(event.delta) / 120)),
                                  "units")

        win2 = tk.Toplevel()

        frame21 = tk.Frame(win2)
        frame21.pack(fill="both", expand=True)
        canvas21 = tk.Canvas(frame21)
        canvas21.pack(side="left", expand=True, fill="both")

        my_scrollbar12 = tk.Scrollbar(frame21,
                                      orient="vertical",
                                      command=canvas21.yview)
        my_scrollbar12.pack(side="right", fill="y")
        my_scrollbar12.config(command=canvas21.yview)

        frame22 = tk.Frame(canvas21)
        canvas21.create_window((0, 0), window=frame22, anchor="nw")
        win2.geometry("1650x825")
        frame22.bind(
            "<Configure>",
            lambda e: canvas21.configure(scrollregion=canvas21.bbox("all")))
        canvas21.bind_all("<MouseWheel>", _on_mousewheel)

        img = country.get_resized_flag(800)
        self.img221 = img
        panel = tk.Label(frame22, image=img)
        panel.grid(column=0, row=0, columnspan=4, sticky="N")
        namelabel = tk.Label(frame22, text=country.name, font="Helvetica 100")
        namelabel.grid(row=1, column=0, columnspan=4)

        mylist = list(country.dict_of_attributes.keys())
        mylist.sort(key=lambda x: x.lower())
        for index, item in enumerate(mylist):
            mylabel = tk.Label(frame22,
                               text=item.replace(".csv", ""),
                               font="Helvetica 15")
            mylabel.grid(row=index + 2, column=0, pady=10)
            mylabel2 = tk.Label(frame22,
                                text=country.dict_of_attributes[item].value,
                                font="Helvetica 15")
            try:
                mylabel3 = tk.Label(frame22,
                                    text=country.dict_of_attributes[item].additional_information_name,
                                    font="Helvetica 15")
            except IndexError:
                mylabel3 = tk.Label(frame22, text="--", font="Helvetica 15")
            mylabel2.grid(row=index + 2, column=1, pady=10)
            mylabel3.grid(row=index + 2, column=2, pady=10)
            mylabel4 = tk.Label(frame22,
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
        good_label = tk.Label(frame22,
                              text=country.name + " is good in:",
                              font="Helvetica 15")
        bad_label = tk.Label(frame22,
                             text=country.name + " is bad in:",
                             font="Helvetica 15")

        good_label.grid(row=len(mylist) + 3, column=0, columnspan=4, pady=20)
        for index, ditem in enumerate(goodlist):
            item = ditem[0]
            mylabel = tk.Label(frame22,
                               text=item.replace(".csv", ""),
                               font="Helvetica 15")
            mylabel.grid(row=len(mylist) + index + 4, column=0, pady=10)
            mylabel2 = tk.Label(frame22,
                                text=country.dict_of_attributes[item].value,
                                font="Helvetica 15")
            try:
                mylabel3 = tk.Label(frame22,
                                    text=country.dict_of_attributes[item].additional_information_name,
                                    font="Helvetica 15")
            except IndexError:
                mylabel3 = tk.Label(frame22, text="--", font="Helvetica 15")
            mylabel2.grid(row=index + 4 + len(mylist), column=1, pady=10)
            mylabel3.grid(row=index + 4 + len(mylist), column=2, pady=10)
            mylabel4 = tk.Label(frame22,
                                text=str(country.dict_of_attributes[item].rank) +
                                "/" +
                                str(
                                    country.dict_of_attributes[item].how_many_ranked),
                                font="Helvetica 15")
            mylabel4.grid(row=index + 4 + len(mylist), column=3, pady=10)

        bad_label.grid(row=len(mylist) + 9, column=0, columnspan=4, pady=20)
        for index, ditem in enumerate(badlist):
            item = ditem[0]
            mylabel = tk.Label(frame22,
                               text=item.replace(".csv", ""),
                               font="Helvetica 15")
            mylabel.grid(row=len(mylist) + index + 10, column=0, pady=10)
            mylabel2 = tk.Label(frame22,
                                text=country.dict_of_attributes[item].value,
                                font="Helvetica 15")
            try:
                mylabel3 = tk.Label(frame22,
                                    text=country.dict_of_attributes[item].additional_information_name,
                                    font="Helvetica 15")
            except IndexError:
                mylabel3 = tk.Label(frame22, text="--", font="Helvetica 15")
            mylabel2.grid(row=index + 10 + len(mylist), column=1, pady=10)
            mylabel3.grid(row=index + 10 + len(mylist), column=2, pady=10)
            mylabel4 = tk.Label(frame22,
                                text=str(country.dict_of_attributes[item].rank) +
                                "/" +
                                str(
                                    country.dict_of_attributes[item].how_many_ranked),
                                font="Helvetica 15")
            mylabel4.grid(row=index + 10 + len(mylist), column=3, pady=10)

    def activate_wormholes(self, numberofwormholes, player=None):
        self.colorarray = [
            "cyan", "dark slate grey", "dark green", "dark violet",
            "dark goldenrod", "medium violet red", "brown2",
            "medium spring green", "grey2"
        ]

        def makeline_not_hidden(line):
            self.c.itemconfig(line, state=tk.NORMAL)

        def makeline_hidden(line):
            self.c.itemconfig(line, state=tk.HIDDEN)

        def create_good_line(country1: Country, country2: Country):
            ml = self.c.create_line(country1.wormhole_coordinates[0],
                                    country1.wormhole_coordinates[1],
                                    country2.wormhole_coordinates[0],
                                    country2.wormhole_coordinates[1],
                                    width=5,
                                    fill="black",
                                    dash=[5, 2],
                                    state=tk.HIDDEN)
            self.linelist.append(ml)
            color = self.colorarray[random.randrange(0, len(self.colorarray))]
            self.colorarray.remove(color)
            startpoint = self.c.create_rectangle(
                country1.wormhole_coordinates[0] + 15,
                country1.wormhole_coordinates[1] + 15,
                country1.wormhole_coordinates[0] - 15,
                country1.wormhole_coordinates[1] - 15,
                fill="gray",
                stipple="@my_stripple.xbm",
                outline=color,
                width=5)
            endpoint = self.c.create_rectangle(
                country2.wormhole_coordinates[0] + 15,
                country2.wormhole_coordinates[1] + 15,
                country2.wormhole_coordinates[0] - 15,
                country2.wormhole_coordinates[1] - 15,
                fill="gray",
                stipple="@my_stripple.xbm",
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
                (self.peacemode == 1 and
                 (country1.owner != "Nobody" and country2.owner != "Nobody"))):
                country1 = player.list_of_possessed_countries[random.randrange(
                    1, len(player.list_of_possessed_countries))]
                country2 = all_countries_in_game[random.randrange(
                    1, len(all_countries_in_game))]
            country1.neighboring_countries.append(country2.name)
            self.wormholed_countries.append([country1, country2])
            create_good_line(country1, country2)
            print(self.linelist)
            return None

        for i in range(numberofwormholes):

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
            win.destroy()

        def kill_button():
            if wl == "no data" or wl == "draw":
                self.transition(same_player_again=True)
            else:
                self.transition(same_player_again=False)
            win.destroy()

        def _on_mousewheel(event):
            canvas11.yview_scroll(int(-1 * (float(event.delta) / 120)),
                                  "units")

        additional_information = property.is_active
        win = tk.Toplevel()
        win.geometry("1400x825")
        frame11 = tk.Frame(win)
        frame11.pack(fill="both", expand=True)
        canvas11 = tk.Canvas(frame11)
        canvas11.pack(side="left", expand=True, fill="both")

        my_scrollbar11 = tk.Scrollbar(frame11,
                                      orient="vertical",
                                      command=canvas11.yview)
        my_scrollbar11.pack(side="right", fill="y")
        my_scrollbar11.config(command=canvas11.yview)

        frame12 = tk.Frame(canvas11)
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
        panel1 = tk.Label(frame12, image=img1)
        panel2 = tk.Label(frame12, image=img2)

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

        panel3 = tk.Label(frame12, image=img3)
        panel4 = tk.Label(frame12, image=img4)
        panel5 = tk.Label(frame12, image=img5)
        panel6 = tk.Label(frame12, image=img6)
        panel7 = tk.Label(frame12, image=img7)
        panel8_1 = tk.Label(frame12, image=img8)
        panel8_2 = tk.Label(frame12, image=img8)

        panel9_1 = tk.Label(frame12, image=img9)
        panel9_2 = tk.Label(frame12, image=img9)

        try:
            l1 = tk.Label(frame12, text=country_a.name + "\n" + property.name.replace(".csv", "") + "\n" +
                          format((country_a.dict_of_attributes[property.name].value), ",") + "\n" + "worldrank:"+str(country_a.dict_of_attributes[property.name].rank) + "\n (of " + str(country_a.dict_of_attributes[property.name].how_many_ranked) + " countries ranked)", font="Helvetica 25", wraplength=500)
        except:
            l1 = tk.Label(frame12,
                          text=country_a.name + "\n" +
                          property.name.replace(".csv", "") + "\n" +
                          "sorry no data",
                          font="Helvetica 25")

        try:
            l2 = tk.Label(
                frame12,
                text=country_b.name + "\n" + property.name.replace(".csv", "") +
                "\n" + format(
                    (country_b.dict_of_attributes[property.name].value), ",") +
                "\n" + "worldrank:" +
                str(country_b.dict_of_attributes[property.name].rank) + "\n (of " +
                str(country_b.dict_of_attributes[property.name].how_many_ranked) +
                " countries ranked)",
                font="Helvetica 25",
                wraplength=500)
        except:
            traceback.print_exc()
            l2 = tk.Label(frame12,
                          text=country_b.name + "\n" +
                          property.name.replace(".csv", "") + "\n" +
                          "sorry no data",
                          font="Helvetica 25")

        killbutton = tk.Button(frame12,
                               image=img7,
                               command=kill_button,
                               width=400,
                               height=200)

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
            guessed_correct_button = tk.Button(frame12,
                                               text="guessed correct",
                                               font="Helvetica 30",
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
                panelA = tk.Label(frame12, image=imgA)
                panelA.grid(row=2, column=0)
                panelA_extra = tk.Label(
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

                panelB = tk.Label(frame12, image=imgB)

                panelB.grid(row=2, column=2)

                panelB_extra = tk.Label(
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

                    wiki_url_A_Label = tk.Label(frame12,
                                                text=wiki_url_A,
                                                fg="blue",
                                                cursor="hand2",
                                                font="Helvetica 15")
                    wiki_url_A_Label.bind("<Button-1>",
                                          lambda x: self.callback(wiki_url_A))

                    wiki_summary_A_Label = tk.Label(frame12,
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

                    wiki_url_B_Label = tk.Label(frame12,
                                                text=wiki_url_B,
                                                fg="blue",
                                                cursor="hand2",
                                                font="Helvetica 15",
                                                wraplength=500)
                    wiki_url_B_Label.bind("<Button-1>",
                                          lambda x: self.callback(wiki_url_B))

                    wiki_summary_B_Label = tk.Label(frame12,
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

    def endscreen(self,
                  cause="numberofrounds",
                  winner: Player = None,
                  gotcha_country: Country = None):

        def _on_mousewheel(event):
            canvas21.yview_scroll(int(-1 * (float(event.delta) / 120)),
                                  "units")

        win2 = tk.Toplevel()

        frame21 = tk.Frame(win2)
        frame21.pack(fill="both", expand=True)
        canvas21 = tk.Canvas(frame21)

        my_scrollbar12 = tk.Scrollbar(frame21,
                                      orient="vertical",
                                      command=canvas21.yview)
        my_scrollbar12.pack(side="right", fill="y")
        my_scrollbar12.config(command=canvas21.yview)

        my_scrollbar13 = tk.Scrollbar(frame21,
                                      orient="horizontal",
                                      command=canvas21.xview)
        my_scrollbar13.pack(side="bottom", fill="x")
        my_scrollbar13.config(command=canvas21.xview)
        canvas21.pack(side="left", expand=True, fill="both")

        win = tk.Frame(canvas21)
        canvas21.create_window((0, 0), window=win, anchor="nw")
        win2.geometry("1650x825")
        win.bind(
            "<Configure>",
            lambda e: canvas21.configure(scrollregion=canvas21.bbox("all")))
        canvas21.bind_all("<MouseWheel>", _on_mousewheel)

        if self.winning_condition == "get gold":
            a = sorted(self.list_of_players,
                       key=lambda x: self.score(x.list_of_possessed_countries),
                       reverse=True)
            self.shitdict = dict()
            for i in range(len(a)):
                self.shitdict[i] = dict()
                text = str(i + 1) + ". place : " + a[i].name + " with " + str(
                    a[i].gold) + " gold \n"
                newframe = tk.Frame(win)
                label1 = tk.Label(newframe, text=text)
                label1.config(font=("Helvetica", 20))
                flagframe = tk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries_gold)):
                    self.doubleframe = tk.Frame(flagframe)
                    flag = a[i].list_of_possessed_countries_gold[
                        j].get_resized_flag(100)
                    self.newlabel = tk.Label(self.doubleframe, image=flag)
                    countrylabel = tk.Label(
                        self.doubleframe,
                        text=a[i].list_of_possessed_countries_gold[j].name)
                    self.newlabel.pack(side="top")
                    countrylabel.pack(side="bottom")
                    self.shitdict[i][j] = flag
                    self.doubleframe.grid(row=0, column=j)
                label1.grid(row=0, column=0)
                flagframe.grid(row=1, column=0)
                newframe.grid(row=i, column=0)
            self.d = "disabled"
            self.showing_country_label[
                "text"] = "Congratulations, " + a[0].name
            self.showing_current_attribute_text_label[
                "text"] = "Congratulations, " + a[0].name
            return None

        if self.winning_condition == "attribute":
            a = sorted(
                self.list_of_players,
                key=lambda x: sum(self.score(x.list_of_possessed_countries)),
                reverse=True)
            self.shitdict = dict()

            # sorting
            def bla(x):
                try:
                    return x.dict_of_attributes[self.end_attribute.name].value
                except:
                    return -9999999.0

            for i in range(len(a)):
                if "higher is better" in self.end_attribute.name:
                    a[i].list_of_possessed_countries = sorted(
                        a[i].list_of_possessed_countries,
                        key=lambda x: bla(x),
                        reverse=True)
                else:
                    a[i].list_of_possessed_countries = sorted(
                        a[i].list_of_possessed_countries, key=lambda x: bla(x))
            for i in range(len(a)):
                scorelist = self.score(a[i].list_of_possessed_countries)
                self.shitdict[i] = dict()
                text = str(i + 1) + ". place : " + a[i].name + " with " + str(
                    round(sum(scorelist), 2)) + " points \n"
                newframe = tk.Frame(win)
                label1 = tk.Label(newframe, text=text)
                label1.config(font=("Helvetica", 44))
                flagframe = tk.Frame(newframe,
                                     highlightbackground="green",
                                     highlightthickness=2)
                flagframe.grid_columnconfigure(0, weight=1)
                flagframe.grid_rowconfigure(0, weight=1)
                for j in range(len(a[i].list_of_possessed_countries)):

                    self.doubleframe = tk.Frame(flagframe,
                                                highlightbackground="white",
                                                highlightthickness=2)
                    self.name_value_rank_frame = tk.Frame(self.doubleframe)

                    flag = a[i].list_of_possessed_countries[
                        j].get_resized_flag(100)

                    country_score_label = tk.Label(self.doubleframe,
                                                   text=scorelist[j],
                                                   font="Helvetica 30")
                    self.newlabel = tk.Label(self.doubleframe, image=flag)
                    country = a[i].list_of_possessed_countries[j]
                    if self.reversed_end_attribute == 1:
                        country.dict_of_attributes[self.end_attribute.name].rank = country.dict_of_attributes[
                            self.end_attribute.
                            name].how_many_ranked - country.dict_of_attributes[
                            self.end_attribute.name].rank

                    countrylabel = tk.Label(self.doubleframe,
                                            text=country.name,
                                            font="Helvetica 20")
                    self.newlabel.grid(row=0)
                    country_score_label.grid(row=1)
                    countrylabel.grid(row=2)
                    if self.end_attribute.is_active:
                        try:
                            label_of_thing = tk.Label(
                                self.name_value_rank_frame,
                                text=str(country.dict_of_attributes[
                                    self.end_attribute.name].additional_information_name),
                                font="Helvetica 20")
                        except:
                            label_of_thing = tk.Label(
                                self.name_value_rank_frame,
                                text="--",
                                font="Helvetica 20")
                        try:
                            width = 200
                            urlA = "pictures/attribute_pictures/" + self.end_attribute.name.replace(
                                ".csv", "") + "/" + country.dict_of_attributes[
                                    self.end_attribute.name].additional_information_name + ".jpg"
                            try:
                                imgA = Image.open(urlA)
                            except FileNotFoundError:
                                imgA = Image.open(
                                    "pictures/no_image_available.png")
                            w = float(imgA.width)
                            h = float(imgA.height)
                            imgA = ImageTk.PhotoImage(
                                imgA.resize((int(width), int(width * h / w)),
                                            Image.LANCZOS))
                            panelA = tk.Label(self.doubleframe, image=imgA)
                            panelA.imgA = imgA
                            panelA.grid(row=3)
                        except:
                            traceback.print_exc()
                        label_of_thing.grid(row=0)
                        label_of_value = tk.Label(
                            self.name_value_rank_frame,
                            text=format((country.dict_of_attributes[
                                self.end_attribute.name].value), ","),
                            font="Helvetica 20")
                        label_of_value.grid(row=1)
                        label_of_worldrank = tk.Label(
                            self.name_value_rank_frame,
                            text="worldrank:" + str(country.dict_of_attributes[
                                self.end_attribute.name].rank),
                            font="Helvetica 20")
                        label_of_worldrank.grid(row=2)
                        self.doubleframe.grid_rowconfigure(4, weight=1)
                        self.name_value_rank_frame.grid(row=4, sticky="s")
                    else:
                        label_of_value = tk.Label(
                            self.doubleframe,
                            text=format((country.dict_of_attributes[
                                self.end_attribute.name].value), ","),
                            font="Helvetica 20")
                        label_of_value.grid(row=5, sticky="s")
                        label_of_worldrank = tk.Label(
                            self.doubleframe,
                            text="worldrank:" + str(country.dict_of_attributes[
                                self.end_attribute.name].rank),
                            font="Helvetica 20")
                        label_of_worldrank.grid(row=6, sticky="s")

                    self.shitdict[i][j] = flag
                    self.doubleframe.grid(row=0, column=j, sticky="NS")
                label1.grid(row=0, column=0)
                flagframe.grid(row=1, column=0)
                newframe.grid(row=i, column=0)
            self.d = "disabled"
            self.showing_country_label[
                "text"] = "Congratulations, " + a[0].name
            self.showing_current_attribute_text_label[
                "text"] = "Congratulations, " + a[0].name

        if self.winning_condition == "number of countries":
            a = sorted(
                self.list_of_players,
                key=lambda x: float(
                    (len(x.list_of_possessed_countries)) + random.random()),
                reverse=True)
            self.shitdict = dict()
            for i in range(len(a)):
                self.shitdict[i] = dict()
                text = str(i + 1) + ". place : " + a[i].name + " with " + str(
                    len(a[i].list_of_possessed_countries)) + " countries \n"
                newframe = tk.Frame(win)
                label1 = tk.Label(newframe, text=text)
                label1.config(font=("Helvetica", 44))
                flagframe = tk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries)):
                    self.doubleframe = tk.Frame(flagframe)
                    flag = a[i].list_of_possessed_countries[
                        j].get_resized_flag(100)
                    self.newlabel = tk.Label(self.doubleframe, image=flag)
                    countrylabel = tk.Label(
                        self.doubleframe,
                        text=a[i].list_of_possessed_countries[j].name)
                    self.newlabel.pack(side="top")
                    countrylabel.pack(side="bottom")
                    self.shitdict[i][j] = flag
                    self.doubleframe.grid(row=0, column=j)
                label1.grid(row=0, column=0)
                flagframe.grid(row=1, column=0)
                newframe.grid(row=i, column=0)
            self.d = "disabled"
            self.showing_country_label[
                "text"] = "Congratulations, " + a[0].name
            self.showing_current_attribute_text_label[
                "text"] = "Congratulations, " + a[0].name
        if cause == "twocountriesclaimed":
            text = ""
            winner = self.targetcountry1.owner
            tk.messagebox.showinfo(
                self.root,
                message="Congratulations " + winner +
                " you claimed both countries and therefore you are the winner")
            self.d = "disabled"
            self.showing_country_label["text"] = "Congratulations, " + winner
            self.showing_current_attribute_text_label[
                "text"] = "Congratulations, " + winner
        if self.winning_condition == "secret targets":
            a = sorted(
                self.list_of_players,
                key=lambda x: float((len(
                    set(x.list_of_possessed_countries).intersection(
                        set(self.dict_of_targets[x])))) + random.random()),
                reverse=True)
            self.shitdict = dict()
            for i in range(len(a)):
                self.shitdict[i] = dict()
                text = str(i + 1) + ". place : " + a[i].name
                newframe = tk.Frame(win)
                label1 = tk.Label(newframe, text=text)
                label1.config(font=("Helvetica", 44))
                flagframe = tk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries)):
                    if a[i].list_of_possessed_countries[
                            j] in self.dict_of_targets[a[i]]:
                        self.doubleframe = tk.Frame(flagframe)
                        flag = a[i].list_of_possessed_countries[
                            j].get_resized_flag(100)
                        self.newlabel = tk.Label(self.doubleframe, image=flag)
                        countrylabel = tk.Label(
                            self.doubleframe,
                            text=a[i].list_of_possessed_countries[j].name)
                        self.newlabel.pack(side="top")
                        countrylabel.pack(side="bottom")
                        self.shitdict[i][j] = flag
                        self.doubleframe.grid(row=0, column=j)
                label1.grid(row=0, column=0)
                flagframe.grid(row=1, column=0)
                newframe.grid(row=i, column=0)
            self.d = "disabled"
            self.showing_country_label[
                "text"] = "Congratulations, " + a[0].name
            self.showing_current_attribute_text_label[
                "text"] = "Congratulations, " + a[0].name
        if self.winning_condition == "secret attribute":
            text = ""
            self.d = "disabled"
            self.showing_country_label[
                "text"] = "Congratulations, " + winner.name
            self.showing_current_attribute_text_label[
                "text"] = "Congratulations, " + winner.name
            showing_winner_label = tk.Label(
                win,
                text="Congratulations, " + winner.name + "\nbecause " +
                gotcha_country.name + " is worldrank\n" +
                str(self.dict_of_targets[winner].index(gotcha_country) + 1) +
                "\nin\n" + self.dict_of_target_attribute_name[winner] +
                "\nyou win the game!!!",
                font="Helvetivca 30")
            showing_winner_label.grid(row=0, column=0)

    def setupclaim2countries(self):
        Target = Player(realgrey, "Nobody")
        if self.choosing_index == len(self.list_of_players):
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

        def get_good_ids(numberofgold):
            self.goldids = random.sample(range(len(all_countries_in_game)),
                                         numberofgold)
            for i in self.goldids:
                if all_countries_in_game[i].owner != "Nobody" or all_countries_in_game[
                        i].name == "Unknown Country":
                    get_good_ids(numberofgold)
            return None

        for player in self.list_of_players:
            player.gold = 0
        Target = Player(gold, "Nobody")
        self.numberofgold = len(all_countries_in_game) // 20
        print(self.numberofgold)
        get_good_ids(self.numberofgold)
        for i in self.goldids:
            self.claim_country(Target, all_countries_in_game[i])
            self.goldlist.append(all_countries_in_game[i])

    def getstartingattribute(self) -> Category:
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
                    # TODO
                    try:
                        if isinstance(country.dict_of_attributes[attribute], LocalAttribute
                                      ):
                            try:
                                i = country.dict_of_attributes[attribute].rank
                            except IndexError:
                                numberofnodata = numberofnodata + 1
                        else:
                            numberofnodata = numberofnodata + 1
                    except KeyError:
                        numberofnodata += 1
            if random.random() < 0.5:

                text = "The target attribute is " + attribute
                v = tk.messagebox.showinfo(self.main, message=text)
                self.reversed_end_attribute = 0

            else:
                self.reversed_end_attribute = 1
                text = "The target attribute is " + attribute + "\n REVERSED!!!"
                v = tk.messagebox.showinfo(self.main, message=text)
        return attribute

    def setuppredattribute(self):
        self.end_attribute = self.getstartingattribute()
        if True:
            self.grey_no_data()

    def grey_no_data(self):
        for country in all_countries_in_game:
            if country == Unknown_country:
                continue
            try:
                country.dict_of_attributes[self.end_attribute.name].value
            except:
                print(country.name)
                traceback.print_exc()
                self.claim_country(No_Data_Body, country)

    def setup_secret_target_countries(self, numberoftargets: int):
        self.really_unknown = Unknown_country

        def checkcountrylist(list1):
            for country in list1:
                if country.owner != "Nobody" or country == self.really_unknown:
                    return False
            return True

        def roll_random_country(oldcountry):
            return all_countries_in_game[random.randrange(1, len(all_countries_in_game))]

        def show_targets(player: Player):
            self.no_targets_yetlist.remove(player)
            self.target_countries_frame = tk.Toplevel()
            targetlist = [Unknown_country] * numberoftargets
            while (not checkcountrylist(targetlist)):
                targetlist = [roll_random_country(item) for item in targetlist]

            welcomelabel = tk.Label(
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
                newcountrylabel = tk.Label(self.target_countries_frame,
                                           text=country.name,
                                           font="Helvetica 25")
                newcountrylabel.grid(row=1, column=index)
                self.myimage[index] = country.get_resized_flag(400)
                newlabel = tk.Label(self.target_countries_frame,
                                    image=self.myimage[index],
                                    pady=40)
                newlabel.grid(row=2, column=index)
                pass
            self.dict_of_targets[player] = targetlist
            self.got_targets_Button = tk.Button(self.target_countries_frame,
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

        self.dict_of_targets = dict()
        self.no_targets_yetlist = self.list_of_players.copy()
        show_targets(self.active_player)

    def setup_secret_attribute(self, n):

        def find_top_n_countries(n, attribute):
            returnlist = list()
            for country in all_countries_in_game:
                try:
                    if country.dict_of_attributes[attribute].rank <= n:
                        returnlist.append(country)
                except KeyError:
                    continue
            returnlist.sort(key=lambda x: x.dict_of_attributes[attribute].rank)
            return returnlist

        def open_next_frame():
            self.target_countries_frame.destroy()
            if len(self.no_targets_yetlist) == 0:
                return None
            show_targets(self.no_targets_yetlist[0])

        def show_targets(player: Player):
            self.no_targets_yetlist.remove(player)
            self.target_countries_frame = tk.Toplevel()
            self.target_attribute = player.get_random_attribute_with_cluster()
            self.dict_of_target_attribute_name[player] = self.target_attribute
            welcomelabel = tk.Label(self.target_countries_frame,
                                    text="Welcome " + player.name +
                                    "your attribute is the following: \n\n" +
                                    self.target_attribute.rstrip(".csv") +
                                    "\n\nclaim one of the top " + str(n) +
                                    " countries in order to win the game",
                                    font="Helvetica 25")
            welcomelabel.grid(row=0, column=0)
            self.dict_of_targets[player] = find_top_n_countries(
                n, self.target_attribute)
            self.got_targets_Button = tk.Button(self.target_countries_frame,
                                                text="got it",
                                                command=open_next_frame,
                                                font="Helvetica 25")
            self.got_targets_Button.grid(row=3, column=0)

        self.dict_of_target_attribute_name = dict()
        self.dict_of_targets = dict()
        self.no_targets_yetlist = self.list_of_players.copy()
        show_targets(self.active_player)

    def score(self, countrylist):

        def helphelp(number, list1):
            if self.higherorlower == "higher":
                return sum([item <= number for item in list1])
            if self.higherorlower == "lower":
                return sum([item >= number for item in list1])

        higherorlower = ""
        propertylist = list()
        mcountrylist = list()
        dlist = list()
        if self.reversed_end_attribute == 0:
            if "higher is better" in self.end_attribute.name:
                self.higherorlower = "higher"
            else:
                self.higherorlower = "lower"
        else:
            if "higher is better" in self.end_attribute.name:
                self.higherorlower = "lower"
            else:
                self.higherorlower = "higher"

        for country in all_countries_in_game:
            try:
                if (country.dict_of_attributes[self.end_attribute.name].value
                    ) != float(-1):
                    propertylist.append(
                        (country.dict_of_attributes[self.end_attribute.name].value))
                    mcountrylist.append(country)
                else:
                    dlist.append(country)
            except KeyError:
                dlist.append(country)
        print(propertylist)
        returnlist = list()
        for country in countrylist:
            if country in dlist:
                returnlist.append(30.0)
            else:
                returnlist.append(
                    helphelp(
                        country.dict_of_attributes[self.end_attribute.name].value,
                        propertylist))
        returnlist = [float(item) / float(5) for item in returnlist]
        return returnlist

    def check_if_game_should_end(self):
        if self.active_player_counter == len(
                self.list_of_players) * self.number_of_rounds - 1:
            self.endscreen()
            return True
        if self.winning_condition == "claim 2 countries":
            if self.targetcountry1.owner != "Nobody" and self.targetcountry1.owner == self.targetcountry2.owner:
                self.endscreen(cause="twocountriesclaimed")
                return True
        if self.winning_condition == "get gold":
            if len(self.goldlist) == 0:
                self.endscreen(cause="all gold left")
                return True
        if self.winning_condition == "secret targets":
            if set(self.dict_of_targets[self.active_player]).issubset(
                    set(self.active_player.list_of_possessed_countries)):
                self.endscreen(cause="co")
                return True
        if self.winning_condition == "secret attribute":
            if len(
                    set(self.dict_of_targets[self.active_player]).intersection(
                        set(self.active_player.list_of_possessed_countries))
            ) >= 1:
                for country in self.active_player.list_of_possessed_countries:
                    if country in self.dict_of_targets[self.active_player]:
                        self.endscreen(cause="co",
                                       winner=self.active_player,
                                       gotcha_country=country)
                        break
                return True
        return False

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
        self.c.scale(tk.ALL, x, y, factor, factor)