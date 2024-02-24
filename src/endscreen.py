from __future__ import annotations

import tkinter as tk
from PIL import ImageTk, Image
import traceback
import random

import ttkbootstrap as ttk

from player import Player, call_player_by_name
from country import Country, Unknown_country

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend_game import BackendGame
    from category import Category


def endscreen(cause: str,
              triggered_player_name: str,
              winning_condition: str,
              list_of_players: list[Player],
              attached_backend: BackendGame,
              end_attribute: Category,
              reversed_end_attribute: int,
              winning_country: Country = Unknown_country,
              dict_of_targets: dict[Player, list[Country]] = dict(),
              dict_of_target_attribute_name : dict[Player,str] = dict()) -> str:

    def _on_mousewheel(event):
        canvas21.yview_scroll(int(-1 * (float(event.delta) / 120)),
                              "units")

    win2 = ttk.Window()

    frame21 = ttk.Frame(win2)
    frame21.pack(fill="both", expand=True)
    canvas21 = ttk.Canvas(frame21)

    my_scrollbar12 = ttk.Scrollbar(frame21,
                                  orient="vertical",
                                  command=canvas21.yview)
    my_scrollbar12.pack(side="right", fill="y")
    my_scrollbar12.config(command=canvas21.yview)

    my_scrollbar13 = ttk.Scrollbar(frame21,
                                  orient="horizontal",
                                  command=canvas21.xview)
    my_scrollbar13.pack(side="bottom", fill="x")
    my_scrollbar13.config(command=canvas21.xview)
    canvas21.pack(side="left", expand=True, fill="both")

    win = ttk.Frame(canvas21)
    canvas21.create_window((0, 0), window=win, anchor="nw")
    win2.geometry("1650x825")
    win.bind(
        "<Configure>",
        lambda e: canvas21.configure(scrollregion=canvas21.bbox("all")))
    canvas21.bind_all("<MouseWheel>", _on_mousewheel)

    return_message: str = ''
    match winning_condition:

        case "get gold":
            a: list[Player] = sorted(list_of_players,
                                     key=lambda x: attached_backend.score(
                                         x.list_of_possessed_countries),
                                     reverse=True)
            win2.shitdict: dict[int, dict[int, ImageTk.PhotoImage]] = dict()
            for i in range(len(a)):
                win2.shitdict[i] = dict()
                text = str(i + 1) + ". place : " + a[i].name + " with " + str(
                    a[i].gold) + " gold \n"
                newframe = ttk.Frame(win)
                label1 = ttk.Label(newframe, text=text)
                label1.config(font=("Helvetica", 20))
                flagframe = ttk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries_gold)):
                    doubleframe = ttk.Frame(flagframe)
                    flag = a[i].list_of_possessed_countries_gold[
                        j].get_resized_flag(100)
                    newlabel = ttk.Label(doubleframe, image=flag)
                    countrylabel = ttk.Label(
                        doubleframe,
                        text=a[i].list_of_possessed_countries_gold[j].name)
                    newlabel.pack(side="top")
                    countrylabel.pack(side="bottom")
                    win2.shitdict[i][j] = flag
                    doubleframe.grid(row=0, column=j)
                label1.grid(row=0, column=0)
                flagframe.grid(row=1, column=0)
                newframe.grid(row=i, column=0)
            return_message = "Congratulations, " + a[0].name

        case "attribute":
            a = sorted(
                list_of_players,
                key=lambda x: sum(attached_backend.score(
                    x.list_of_possessed_countries)),
                reverse=True)
            win2.shitdict = dict()

            # sorting
            def bla(x: Country) -> float:
                try:
                    return x.dict_of_attributes[end_attribute.name].value
                except:
                    return -9999999.0

            for i in range(len(a)):
                if "higher is better" in end_attribute.name:
                    a[i].list_of_possessed_countries = sorted(
                        a[i].list_of_possessed_countries,
                        key=lambda x: bla(x),
                        reverse=True)
                else:
                    a[i].list_of_possessed_countries = sorted(
                        a[i].list_of_possessed_countries, key=lambda x: bla(x))
            for i in range(len(a)):
                scorelist = attached_backend.score(
                    a[i].list_of_possessed_countries)
                win2.shitdict[i] = dict()
                text = str(i + 1) + ". place : " + a[i].name + " with " + str(
                    round(sum(scorelist), 2)) + " points \n"
                newframe = ttk.Frame(win)
                label1 = ttk.Label(newframe, text=text)
                label1.config(font=("Helvetica", 44))
                flagframe = ttk.Frame(newframe,
                                     highlightbackground="green",
                                     highlightthickness=2)
                flagframe.grid_columnconfigure(0, weight=1)
                flagframe.grid_rowconfigure(0, weight=1)
                for j in range(len(a[i].list_of_possessed_countries)):

                    doubleframe = ttk.Frame(flagframe,
                                           highlightbackground="white",
                                           highlightthickness=2)
                    name_value_rank_frame = ttk.Frame(doubleframe)

                    flag = a[i].list_of_possessed_countries[
                        j].get_resized_flag(100)

                    country_score_label = ttk.Label(doubleframe,
                                                   text=scorelist[j],
                                                   font="Helvetica 30")
                    newlabel = ttk.Label(doubleframe, image=flag)
                    country = a[i].list_of_possessed_countries[j]
                    if reversed_end_attribute == 1:
                        country.dict_of_attributes[end_attribute.name].rank = country.dict_of_attributes[
                            end_attribute.
                            name].how_many_ranked - country.dict_of_attributes[
                            end_attribute.name].rank

                    countrylabel = ttk.Label(doubleframe,
                                            text=country.name,
                                            font="Helvetica 20")
                    newlabel.grid(row=0)
                    country_score_label.grid(row=1)
                    countrylabel.grid(row=2)
                    if end_attribute.is_active:
                        try:
                            label_of_thing = ttk.Label(
                                name_value_rank_frame,
                                text=str(country.dict_of_attributes[
                                    end_attribute.name].additional_information_name),
                                font="Helvetica 20")
                        except:
                            label_of_thing = ttk.Label(
                                name_value_rank_frame,
                                text="--",
                                font="Helvetica 20")
                        try:
                            width = 200
                            urlA = "pictures/attribute_pictures/" + end_attribute.name.replace(
                                ".csv", "") + "/" + country.dict_of_attributes[
                                    end_attribute.name].additional_information_name + ".jpg"
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
                            panelA = ttk.Label(doubleframe, image=imgA)
                            panelA.imgA = imgA
                            panelA.grid(row=3)
                        except:
                            traceback.print_exc()
                        label_of_thing.grid(row=0)
                        label_of_value = ttk.Label(
                            name_value_rank_frame,
                            text=format((country.dict_of_attributes[
                                end_attribute.name].value), ","),
                            font="Helvetica 20")
                        label_of_value.grid(row=1)
                        label_of_worldrank = ttk.Label(
                            name_value_rank_frame,
                            text="worldrank:" + str(country.dict_of_attributes[
                                end_attribute.name].rank),
                            font="Helvetica 20")
                        label_of_worldrank.grid(row=2)
                        doubleframe.grid_rowconfigure(4, weight=1)
                        name_value_rank_frame.grid(row=4, sticky="s")
                    else:
                        label_of_value = ttk.Label(
                            doubleframe,
                            text=format((country.dict_of_attributes[
                                end_attribute.name].value), ","),
                            font="Helvetica 20")
                        label_of_value.grid(row=5, sticky="s")
                        label_of_worldrank = ttk.Label(
                            doubleframe,
                            text="worldrank:" + str(country.dict_of_attributes[
                                end_attribute.name].rank),
                            font="Helvetica 20")
                        label_of_worldrank.grid(row=6, sticky="s")

                    win2.shitdict[i][j] = flag
                    doubleframe.grid(row=0, column=j, sticky="NS")
                label1.grid(row=0, column=0)
                flagframe.grid(row=1, column=0)
                newframe.grid(row=i, column=0)
            return_message = "Congratulations, " + a[0].name

        case "number of countries":
            a = sorted(
                list_of_players,
                key=lambda x: float(
                    (len(x.list_of_possessed_countries)) + random.random()),
                reverse=True)
            win2.shitdict = dict()
            for i in range(len(a)):
                win2.shitdict[i] = dict()
                text = str(i + 1) + ". place : " + a[i].name + " with " + str(
                    len(a[i].list_of_possessed_countries)) + " countries \n"
                newframe = ttk.Frame(win)
                label1 = ttk.Label(newframe, text=text)
                label1.config(font=("Helvetica", 44))
                flagframe = ttk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries)):
                    doubleframe = ttk.Frame(flagframe)
                    flag = a[i].list_of_possessed_countries[
                        j].get_resized_flag(100)
                    newlabel = ttk.Label(doubleframe, image=flag)
                    countrylabel = ttk.Label(
                        doubleframe,
                        text=a[i].list_of_possessed_countries[j].name)
                    newlabel.pack(side="top")
                    countrylabel.pack(side="bottom")
                    win2.shitdict[i][j] = flag
                    doubleframe.grid(row=0, column=j)
                label1.grid(row=0, column=0)
                flagframe.grid(row=1, column=0)
                newframe.grid(row=i, column=0)
            return_message = "Congratulations, " + a[0].name

        case "twocountriesclaimed":
            text = ""
            return_message = "Congratulations, " + triggered_player_name

        case "secret targets":
            a = sorted(
                list_of_players,
                key=lambda x: float((len(
                    set(x.list_of_possessed_countries).intersection(
                        set(dict_of_targets[x])))) + random.random()),
                reverse=True)
            win2.shitdict = dict()
            for i in range(len(a)):
                win2.shitdict[i] = dict()
                text = str(i + 1) + ". place : " + a[i].name
                newframe = ttk.Frame(win)
                label1 = ttk.Label(newframe, text=text)
                label1.config(font=("Helvetica", 44))
                flagframe = ttk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries)):
                    if a[i].list_of_possessed_countries[
                            j] in dict_of_targets[a[i]]:
                        doubleframe = ttk.Frame(flagframe)
                        flag = a[i].list_of_possessed_countries[
                            j].get_resized_flag(100)
                        newlabel = ttk.Label(doubleframe, image=flag)
                        countrylabel = ttk.Label(
                            doubleframe,
                            text=a[i].list_of_possessed_countries[j].name)
                        newlabel.pack(side="top")
                        countrylabel.pack(side="bottom")
                        win2.shitdict[i][j] = flag
                        doubleframe.grid(row=0, column=j)
                label1.grid(row=0, column=0)
                flagframe.grid(row=1, column=0)
                newframe.grid(row=i, column=0)
            return_message = "Congratulations, " + a[0].name

        case "secret attribute":
            text = ""
            return_message = "Congratulations, " + triggered_player_name

            real_winner : Player = call_player_by_name(triggered_player_name)

            to_display_text: str = "Congratulations, " + triggered_player_name + "\nbecause " + winning_country.name + " is worldrank\n" + \
                str(dict_of_targets[real_winner].index(winning_country) + 1) + "\nin\n" + \
                dict_of_target_attribute_name[real_winner] + \
                "\nyou win the game!!!"

            showing_winner_label = ttk.Label(
                win,
                text=to_display_text,
                font="Helvetivca 30")

            showing_winner_label.grid(row=0, column=0)
        case _:
            return_message = 'Unknown winning condition'
    win2.mainloop()
    return return_message
