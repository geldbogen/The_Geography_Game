
def endscreen(self,
                  cause: str = "numberofrounds",
                  winner_name: Player | None = None,
                  gotcha_country: Country | None = None):

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
            a = sorted(self.backend.list_of_players,
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
                self.backend.list_of_players,
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
                self.backend.list_of_players,
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
            winner_name: str = self.targetcountry1.owner_name
            tk.messagebox.showinfo(
                self.root,
                message="Congratulations " + winner_name +
                " you claimed both countries and therefore you are the winner")
            self.d = "disabled"
            self.showing_country_label["text"] = "Congratulations, " + winner_name
            self.showing_current_attribute_text_label[
                "text"] = "Congratulations, " + winner_name
        if self.winning_condition == "secret targets":
            a = sorted(
                self.backend.list_of_players,
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
                "text"] = "Congratulations, " + winner_name.name
            self.showing_current_attribute_text_label[
                "text"] = "Congratulations, " + winner_name.name
            showing_winner_label = tk.Label(
                win,
                text="Congratulations, " + winner_name.name + "\nbecause " +
                gotcha_country.name + " is worldrank\n" +
                str(self.dict_of_targets[winner_name].index(gotcha_country) + 1) +
                "\nin\n" + self.dict_of_target_attribute_name[winner_name] +
                "\nyou win the game!!!",
                font="Helvetivca 30")
            showing_winner_label.grid(row=0, column=0)