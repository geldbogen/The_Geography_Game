class MainWindow():
    def __init__(self,bild,listofplayers,wormholemode,startingcountries="random",numberofrounds=99999999999,winningcondition="number of countries",numberofwormholes=3,pred_attribute="random",peacemode=0,reversed_end_attribute=0):
        
        self.rerolls=3
        self.numberoftargets=2
        self.pred_attribute_name=pred_attribute
        self.winningcondition=winningcondition
        self.flagframedict=dict()
        self.numberofrounds=numberofrounds
        self.index=0
        self.goldlist=list()
        self.choosingindex=-1
        self.startingcountries=startingcountries
        self.reversed_end_attribute=reversed_end_attribute
        main=tk.Tk()
        sv_ttk.set_theme("dark")  # Set light theme

        self.list_of_players=listofplayers
        print(self.list_of_players)
        print(len(listofplayers))
        self.activeplayercounter=0
        self.active_player=self.list_of_players[self.activeplayercounter]
        self.numberofplayers=len(self.list_of_players)
        self.endattribute=None
        self.wormholemode=wormholemode
        self.wormholed_countries=list()
        self.numberofwormholes=numberofwormholes
        print(self.winningcondition)

        self.peacemode=peacemode

        self.currentattribute=all_categories[0]

        self.main=main

        self.chosencountrya=None
        self.turncounter=0

        self.frame1=tk.Frame(main,width=300,height=300) 
        self.frame1.pack(side="bottom", fill="both",expand=True)
        
        #frame1=frame2+areyousurebuttons

        self.frame2=tk.Frame(self.frame1)
        # frame2= frame3 + flags    

        self.frame3=tk.Frame(self.frame2)
        self.buttonframe=tk.Frame(self.frame1)
        self.buttonframe2=tk.Frame(self.frame1)
        self.bild=bild
        self.c=tk.Canvas(self.frame3,bg="white",width=1000,height=600)
        
        ph=ImageTk.PhotoImage(image=bild,master=self.c)
        self.c.background=ph
        self.image_on_canvas=self.c.create_image(0,0,image=self.c.background,anchor="nw")
        
        #scrollbar
        my_scrollbar1=tk.Scrollbar(self.frame3,orient="vertical",command=self.c.yview)
        my_scrollbar1.pack(side="right",fill="y")
        my_scrollbar1.config(command=self.c.yview)
        my_scrollbar2=tk.Scrollbar(self.frame3,orient="horizontal",command=self.c.xview)
        my_scrollbar2.pack(side="bottom",fill="x")
        my_scrollbar2.config(command=self.c.xview)
        self.c.config(yscrollcommand=my_scrollbar1.set,xscrollcommand=my_scrollbar2.set)
        self.c.config(scrollregion = self.c.bbox("all"))

        for player in self.list_of_players:
            self.flagframedict[player.name]=tk.Frame(self.frame2)
            self.flagframedict[player.name].current_flagdict=dict()
        
        


        self.c.bind("<ButtonPress-1>",self.click)
        
        
        self.c.bind("<ButtonPress-3>", self.scroll_start)
        self.c.bind("<B3-Motion>", self.scroll_move)


       
        #unpacking
        self.frame3.pack(side="bottom",expand=True,fill="both")
        self.frame2.pack(side="top",expand=True,fill="both")
        self.frame1.pack(side="top",expand=True,fill="both")
        self.frame4=tk.Frame(self.frame3)
        self.frame5=tk.Frame(self.frame3)


        self.reroll_button=tk.Button(self.frame5,text="rerolls left:\n " +str(self.active_player.rerolls_left) ,font="Helvetica 25",anchor="sw",command=lambda: self.reroll(player=self.active_player))
        self.reroll_button.pack(side="left",fill="y")

        self.showing_country_label=tk.Label(self.frame5,text="It is the turn of " +self.active_player.name +"\n You have not chosen any country yet",font="Helvetica 25")
        self.showing_country_label.pack(side="bottom",expand=True,fill="both")

        self.turn_counter_label=tk.Label(self.frame4,text=str(self.turncounter),font="Helvetica 50")
        self.turn_counter_label.pack(side="right")
        
        self.showing_current_attribute_text_label=tk.Label(self.frame4,text="Welcome!",font="Helvetica 25")
        self.showing_current_attribute_text_label.pack(anchor="nw",expand=True,fill="both")

        self.frame4.pack(side="top",fill="x")
        self.frame5.pack(side="bottom",fill="x")
        
        self.c.pack(side="top",fill="both",expand=True)
        



        self.button_sure=tk.Button(self.buttonframe,text="Attack!",font="Helvetica 20")
        self.button_not_sure=tk.Button(self.buttonframe,text="No go back",font="Helvetica 20")
        self.button_sure.pack(side="left")
        self.button_not_sure.pack(side="right")
        self.button_claim=tk.Button(self.buttonframe2,text="Yes Please!",font="Helvetica 20")
        
        self.d=""
        self.randompeoplestart=random.sample(range(0,len(self.list_of_players)),len(self.list_of_players))


        #usher choosing countries procedure if that mode was chosen
        if self.startingcountries=="choose":
            self.choosingindex=0
            self.active_player=self.list_of_players[self.randompeoplestart[self.choosingindex]]
            self.showing_current_attribute_text_label["text"]="Choose a starting country of your choice"
            self.showing_country_label["text"]=self.active_player.name + "\n Please choose a starting country"
        
        #roll starting countries for the players
        #TODO take care of ending attribute
        if self.startingcountries=="random":
            self.choosingindex=len(self.list_of_players)
            self.setupgame()
            while True:
                j=0
                self.randomstart=random.sample(range(0,len(all_countries)),len(self.list_of_players))
                for rng in self.randomstart:
                    if len(all_countries[rng].neighboringcountries)<3:
                        j=1
                    for rng2 in self.randomstart:
                        if Countriesareconnected(all_countries[rng2],all_countries[rng]):
                            j=1
                    if self.winningcondition=="attribute":
                        try:
                            all_countries[rng].dictofattributes[self.endattribute.name][0]
                        except:
                            j=1
                if j==0:
                    break
            for i in range (len(self.list_of_players)):
                self.claimcountry(self.list_of_players[i],all_countries[self.randomstart[i]])
                print(all_countries[self.randomstart[i]].name)

        #roll first attribute
        self.getgoodattribute(self.active_player)
        replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
        
        main.mainloop()

    def updateimage(self,newimage):
        newimage=ImageTk.PhotoImage(newimage)
        self.c.background=newimage
        self.c.itemconfig(self.image_on_canvas,image=newimage)
    def click(self,event):
        
        if self.d=="disabled":
            return None
        if self.choosingindex<len(self.list_of_players):
            clickedcountry=getcountrybyposition(self.c.canvasx(event.x),self.c.canvasy(event.y))
            self.showing_country_label["text"]=self.active_player.name + " do you want to start with \n" + clickedcountry.name + " ?"
            self.button_claim["command"]=lambda: self.claimstartingcountry(self.active_player,clickedcountry)
            self.button_claim.pack(side="bottom")
            self.buttonframe2.pack(side="bottom")
            return None
        clickedcountry=getcountrybyposition(self.c.canvasx(event.x),self.c.canvasy(event.y))
        if self.chosencountrya==None:
            self.showing_country_label["text"]="It is the turn of " + self.active_player.name + "\n You have chosen " + clickedcountry.name + " currently controlled by " + clickedcountry.owner
            if clickedcountry.owner==self.active_player.name:
                self.chosencountrya=clickedcountry
                replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute,self.chosencountrya)

                self.showing_country_label["text"]=self.showing_country_label["text"] + "\n You can attack with this country"
        else:
            if self.peacemode==1 and clickedcountry.owner!="Nobody" and callplayerbyname(clickedcountry.owner)!=self.active_player:
                self.chosencountrya=None
                self.showing_country_label["text"]="You can not attack anoter player's countries in peace mode! \n Choose another country!"
                # time.sleep(5)
                # self.showingcountrylabel["text"]=""
                return None
            if Countriesareconnected(clickedcountry,self.chosencountrya):
                if self.active_player!=callplayerbyname(clickedcountry.owner):
                    replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute,self.chosencountrya,clickedcountry)

                    self.showing_country_label["text"]="Does the above sentence looks correct to you?"
                    self.button_sure["command"]= lambda: self.attack(self.chosencountrya,clickedcountry)
                    self.button_not_sure["command"]=self.fuckgoback
                    self.buttonframe.pack(side="bottom")
                    self.d="disabled"
                else:
                    self.showing_country_label["text"]="You already own this country"
            else:
                self.chosencountrya=None
                self.showing_country_label["text"]="These countries do not share a common land border.\n Please choose another pair!"

    def find_distance(self,countrya:Country,countryb:Country):
        mydict=dict()
        myset=set(countrya.name)
        q=[[countrya.name,0]]
        print(q)
        for country in all_countries:
            mydict[country.name]=country.neighboringcountries
        while countryb.name not in myset:
            temp=q[0]
            q.pop(0)
            for countryname in mydict[temp[0]]:
                if countryname in myset:
                    pass
                else:
                    myset.add(countryname)
                    q.append([countryname, temp[1]+1])
                    if countryname==countryb.name:
                        return temp[1]+1
            pass
        return None

    def attack(self,countrya,countryb):
        
        self.buttonframe.pack_forget()
        self.d=""
        self.showing_country_label["text"]=""
        self.chosencountrya=None
        result=self.attackwithattribute(self.currentattribute.name,countrya,countryb)
        if result=="no data":
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="no data")
            self.getgoodattribute(self.active_player)
            replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
            return None
        if result=="draw!":
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="draw!")
            self.getgoodattribute(self.active_player)
            replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
            return None
        if result=="hard defeat!":
            self.claimcountry(self.active_player,countryb)
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="hard defeat!")
            return None
        if result=="True":
            self.claimcountry(self.active_player,countryb)
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="you win!")
            
            
        else:
            self.popupwinorloose(countrya,countryb,self.currentattribute,wl="you loose!")
            if countryb.owner!="Nobody":
                self.claimcountry(callplayerbyname(countryb.owner),countrya)

        
        
                

    def transition(self,sameplayeragain=False):

        if not sameplayeragain:
            if self.checkifgameshouldend():
                return None
            self.activeplayercounter=self.activeplayercounter+1
        self.index=self.activeplayercounter%len(self.list_of_players)
        
        if not sameplayeragain:
            if self.index==0:
                self.turncounter+=1

        #update the interface
        self.turn_counter_label["text"]=str(self.turncounter)
        self.flagframedict[self.active_player.name].pack_forget()
        self.active_player=self.list_of_players[self.index]
        self.showing_country_label["text"]="It is the turn of " +self.active_player.name +"\n You have not chosen any country yet"
        
        #roll a new attribute
        self.getgoodattribute(self.active_player)
        replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
        self.flagframedict[self.active_player.name].pack(side="top")
        if self.wormholemode=="every round changing wormholes":
            if self.index==0:
                try:
                    self.destroy_all_wormholes()    
                except:
                    traceback.print_exc()
                self.activate_wormholes(3)    
        if self.wormholemode=="every round changing wormholes from your countries":
            try:
                self.destroy_all_wormholes()
            except:
                traceback.print_exc()
            if len(self.active_player.list_of_possessed_countries)>=3:
                print("wormholes werden aktiviert")
                self.activate_wormholes(1,player=self.active_player)
        self.reroll_button["text"]="rerolls left:\n " +str(self.active_player.rerolls_left)

    def reroll(self,player:Player):
        if player.rerolls_left==0:
            return None
        player.rerolls_left-=1
        
        self.getgoodattribute(self.active_player)
        replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
        self.reroll_button["text"]="rerolls left:\n " +str(self.active_player.rerolls_left)


    def getgoodattribute(self,player,counter=0,i=0) -> None:
        i=0
        counter=0
        atleast_one=False
        self.currentattribute=self.getrandomattribute_with_cluster()


        # if the attribute is end only it should not be a valid attribute
        if self.currentattribute.is_end_only:
            self.getgoodattribute(player)


        for country in player.list_of_possessed_countries:
            #TODO:make it better if just some continents are chosen
            #simulate attacks in order to get an attribute, with which one can actually do something (to no frustrate players)
            for neighboringcountrystring in list(set(country.neighboringcountries)):
                i+=1
                if self.attackwithattribute(self.currentattribute.name,country,callcountrybyname(neighboringcountrystring))=="no data":
                    counter = counter+1
                    print(neighboringcountrystring +" \n" + country.name)
                if self.attackwithattribute(self.currentattribute.name,country,callcountrybyname(neighboringcountrystring)) in ["draw","True"]:
                    if not callcountrybyname(neighboringcountrystring) in player.list_of_possessed_countries:
                        atleast_one=True
        
        print(float(counter)/float(i))
        if float(counter)/float(i)>0.25 or not atleast_one:
            print(self.currentattribute.name)
            print("doesn't work because of the missing above we get a new attribute!")
            self.getgoodattribute(player)
        else:
            if self.currentattribute.numberOfChosenAlready==1:
                self.currentattribute.numberOfChosenAlready=0
                self.getgoodattribute(player)
            else:
                self.currentattribute.numberOfChosenAlready+=1


    def getrandomattribute_with_cluster(self) -> Category:

        # get a random attribute name (including the name of a cluster)
        
        self.currentattributename_with_cluster=random.choice(all_categories_names_and_clusters)

        # if a cluster is chosen choose a random attribute from that cluster
        if len(dictionary_attribute_name_to_attribute[self.currentattributename_with_cluster])>1:
            return random.choice(dictionary_attribute_name_to_attribute[self.currentattributename_with_cluster])
        # if it is not a cluster, just return the attribute
        else: 
            return dictionary_attribute_name_to_attribute[self.currentattributename_with_cluster][0]
        


    def fuckgoback(self):
        # self.buttonsure.pack_forget()
        # self.buttonnotsure.pack_forget()
        self.buttonframe.pack_forget()
        self.chosencountrya=None
        self.showing_country_label["text"]=""
        self.d=""
    def attackwithattribute(self,attributename,countrya,countryb):
        try:
            if isinstance(countrya.dictofattributes[attributename][1],int) and isinstance(countryb.dictofattributes[attributename][1],int):
                if countrya.dictofattributes[attributename][0]==countryb.dictofattributes[attributename][0]:
                    return "draw!"
                if countrya.dictofattributes[attributename][1]< countryb.dictofattributes[attributename][1]:
                    if countrya.dictofattributes[attributename][1]+99< countryb.dictofattributes[attributename][1]:
                        return "hard defeat!"
                    return "True"
                else:
                    return "False"
            else:
                return "no data"
        except:
            return "no data"
        
    def claimcountry(self,player,country):

        def changethingswhencountryclicked(country):
            clickedcountry=country
            if self.chosencountrya==None:
                self.showing_country_label["text"]="It is the turn of " + self.active_player.name + "\n You have chosen " + clickedcountry.name + " currently controlled by " + clickedcountry.owner
                if clickedcountry.owner==self.active_player.name:
                    self.chosencountrya=clickedcountry
                    self.showing_country_label["text"]=self.showing_country_label["text"] + "\n You can attack with this country"
            else:
                if Countriesareconnected(clickedcountry,self.chosencountrya):
                    if self.active_player!=callplayerbyname(clickedcountry.owner):
                        self.showing_country_label["text"]="You want to attack  " + clickedcountry.name + " currently controlled by " + clickedcountry.owner +" with " + self.chosencountrya.name + " are you sure?"
                        self.button_sure["command"]= lambda: self.attack(self.chosencountrya,clickedcountry)
                        self.button_not_sure["command"]=self.fuckgoback
                        self.buttonframe.pack(side="bottom")
                        self.d="disabled"
                    else:
                        self.showing_country_label["text"]="You already own this country"
                else:
                    self.chosencountrya=None
                    self.showing_country_label["text"]="Those countries do not share a common land border. Please choose another pair"
                    time.wait(5)
                    self.showing_country_label["text"]=""
                


        player.list_of_possessed_countries.append(country)
        oldowner=country.owner
        country.owner=player.name
    

        inv_map = {v: k for k, v in greencountrydict.items()}
        color=inv_map[country.name]
        npimage=np.array(greenimage)
        green=np.array(color,dtype=np.uint8)
        greens=list(zip(*np.where(np.all((npimage==green),axis=-1))))
    
        for tuplen in greens:
            self.bild.putpixel((tuplen[1],tuplen[0]),player.color)
        
        if player.name!="Nobody":
            if self.winningcondition!="get gold" or country in self.goldlist:
                frame=self.flagframedict[player.name]
                myimage=country.getresizedflag(50)
                newlabel=tk.Label(frame,image=myimage)
                newlabel.grid(row=0,column=len(player.list_of_possessed_countries)+1)
                newlabel.bind("<Button-1>",lambda x: self.popupcountrystats(country))
                player.labeldict[country]=newlabel
                frame.current_flagdict[country]=myimage
                
        
        
        if oldowner!="Nobody" and not self.winningcondition in ["get gold"]:
            callplayerbyname(oldowner).list_of_possessed_countries.remove(country)
            callplayerbyname(oldowner).labeldict[country].destroy()
        


        self.updateimage(self.bild)

        if self.winningcondition=="get gold":
            if player.name!="Nobody":
                if country in self.goldlist:
                    player.gold=player.gold+1
                    self.goldlist.remove(country)
                    player.list_of_possessed_countries_gold.append(country)
        


    def claimstartingcountry(self,player,country):
        self.buttonframe2.pack_forget()
        self.claimcountry(player,country)
        self.choosingindex=self.choosingindex+1
        if self.choosingindex==len(self.list_of_players):
            self.active_player=self.list_of_players[self.index]
            self.showing_country_label["text"]="It is the turn of " +self.active_player.name +"\n You have not chosen any country yet"
            replace_A_and_B_in_category_name(self.showing_current_attribute_text_label,self.currentattribute)
            self.setupgame()
        else:
            self.active_player=self.list_of_players[self.randompeoplestart[self.choosingindex]]
            self.showing_current_attribute_text_label["text"]="Choose a starting country of your choice"
            self.showing_country_label["text"]=self.active_player.name + " Please choose a starting country"

    def callback(self,url):
        webbrowser.open_new(url)

    def popupcountrystats(self,country):
        def _on_mousewheel(event):
            canvas21.yview_scroll(int(-1*(float(event.delta)/120)), "units")
        
        win2=tk.Toplevel()

        frame21=tk.Frame(win2)
        frame21.pack(fill="both",expand=True)
        canvas21=tk.Canvas(frame21)
        canvas21.pack(side="left",expand=True,fill="both")

        my_scrollbar12=tk.Scrollbar(frame21,orient="vertical",command=canvas21.yview)
        my_scrollbar12.pack(side="right",fill="y")
        my_scrollbar12.config(command=canvas21.yview)


        frame22=tk.Frame(canvas21)
        canvas21.create_window((0,0),window=frame22,anchor="nw")
        win2.geometry("1650x825")
        frame22.bind(
            "<Configure>",
            lambda e: canvas21.configure(
                scrollregion=canvas21.bbox("all")
            )
        )
        canvas21.bind_all("<MouseWheel>",_on_mousewheel)

        img=country.getresizedflag(800)
        self.img221=img
        panel=tk.Label(frame22,image=img)
        panel.grid(column=0,row=0,columnspan=4,sticky="N")
        namelabel=tk.Label(frame22,text=country.name,font="Helvetica 100")
        namelabel.grid(row=1,column=0,columnspan=4)


        mylist=list(country.dictofattributes.keys())
        mylist.sort(key=lambda x: x.lower())
        for index,item in enumerate(mylist):
            mylabel=tk.Label(frame22,text=item.replace(".csv",""),font="Helvetica 15")
            mylabel.grid(row=index+2,column=0,pady=10)
            mylabel2=tk.Label(frame22,text=country.dictofattributes[item][0],font="Helvetica 15")
            try:
                mylabel3=tk.Label(frame22,text=country.dictofattributes[item][3],font="Helvetica 15")
            except IndexError:
                mylabel3=tk.Label(frame22,text="--",font="Helvetica 15")
            mylabel2.grid(row=index+2,column=1,pady=10)
            mylabel3.grid(row=index+2,column=2,pady=10)
            mylabel4=tk.Label(frame22,text=str(country.dictofattributes[item][1]) + "/"+ str(country.dictofattributes[item][2]),font="Helvetica 15")
            mylabel4.grid(row=index+2,column=3,pady=10)
        ddlist=[[propertyname,value[1]/value[2]] for propertyname,value in country.dictofattributes.items()]
        ddlist.sort(key=lambda x: x[1])
        print(ddlist)
        goodlist=ddlist[:5]
        ddlist=[[pname,value] for [pname,value] in ddlist if country.dictofattributes[pname][0] not in [-1,-1.0,-9999.0,-9999]]
        badlist=ddlist[-5:]
        badlist.reverse()
        goodLabel=tk.Label(frame22,text=country.name + " is good in:",font="Helvetica 15")
        badLabel=tk.Label(frame22,text=country.name + " is bad in:",font="Helvetica 15")

        goodLabel.grid(row=len(mylist)+3,column=0,columnspan=4,pady=20)
        for index,ditem in enumerate(goodlist):
            item=ditem[0]
            mylabel=tk.Label(frame22,text=item.replace(".csv",""),font="Helvetica 15")
            mylabel.grid(row=len(mylist) + index+4,column=0,pady=10)
            mylabel2=tk.Label(frame22,text=country.dictofattributes[item][0],font="Helvetica 15")
            try:
                mylabel3=tk.Label(frame22,text=country.dictofattributes[item][3],font="Helvetica 15")
            except IndexError:
                mylabel3=tk.Label(frame22,text="--",font="Helvetica 15")
            mylabel2.grid(row=index+4+len(mylist),column=1,pady=10)
            mylabel3.grid(row=index+4+len(mylist),column=2,pady=10)
            mylabel4=tk.Label(frame22,text=str(country.dictofattributes[item][1]) + "/"+ str(country.dictofattributes[item][2]),font="Helvetica 15")
            mylabel4.grid(row=index+4+len(mylist),column=3,pady=10)

        badLabel.grid(row=len(mylist)+9,column=0,columnspan=4,pady=20)
        for index,ditem in enumerate(badlist):
            item=ditem[0]
            mylabel=tk.Label(frame22,text=item.replace(".csv",""),font="Helvetica 15")
            mylabel.grid(row=len(mylist) + index+10,column=0,pady=10)
            mylabel2=tk.Label(frame22,text=country.dictofattributes[item][0],font="Helvetica 15")
            try:
                mylabel3=tk.Label(frame22,text=country.dictofattributes[item][3],font="Helvetica 15")
            except IndexError:
                mylabel3=tk.Label(frame22,text="--",font="Helvetica 15")
            mylabel2.grid(row=index+10+len(mylist),column=1,pady=10)
            mylabel3.grid(row=index+10+len(mylist),column=2,pady=10)
            mylabel4=tk.Label(frame22,text=str(country.dictofattributes[item][1]) + "/"+ str(country.dictofattributes[item][2]),font="Helvetica 15")
            mylabel4.grid(row=index+10+len(mylist),column=3,pady=10)

    def activate_wormholes(self,numberofwormholes,player=None):    
        self.colorarray=["cyan", "dark slate grey", "dark green", "dark violet", "dark goldenrod", "medium violet red", "brown2", "medium spring green", "grey2"]
        def makeline_not_hidden(line):
            self.c.itemconfig(line,state=tk.NORMAL)
        def makeline_hidden(line):
            self.c.itemconfig(line,state=tk.HIDDEN)
        def create_good_line(country1: Country,country2:Country):
            ml=self.c.create_line(country1.wormholecoordinates[0], country1.wormholecoordinates[1], country2.wormholecoordinates[0], country2.wormholecoordinates[1],width=5,fill="black",dash=[5,2],state=tk.HIDDEN)
            self.linelist.append(ml)
            color=self.colorarray[random.randrange(0,len(self.colorarray))]
            self.colorarray.remove(color)
            startpoint=self.c.create_rectangle(country1.wormholecoordinates[0]+15,country1.wormholecoordinates[1]+15,country1.wormholecoordinates[0]-15,country1.wormholecoordinates[1]-15,fill="gray",stipple="@my_stripple.xbm",outline=color,width=5)
            endpoint=self.c.create_rectangle(country2.wormholecoordinates[0]+15,country2.wormholecoordinates[1]+15,country2.wormholecoordinates[0]-15,country2.wormholecoordinates[1]-15,fill="gray",stipple="@my_stripple.xbm",outline=color,width=5)
            self.pointlist.append(startpoint)
            self.pointlist.append(endpoint)
            self.c.tag_bind(startpoint,"<Enter>",lambda x: makeline_not_hidden(ml))
            self.c.tag_bind(endpoint,"<Enter>",lambda x: makeline_not_hidden(ml))
            self.c.tag_bind(startpoint,"<Leave>",lambda x: makeline_hidden(ml))
            self.c.tag_bind(endpoint,"<Leave>",lambda x: makeline_hidden(ml))
        self.linelist=list()
        self.pointlist=list()
        country1=Germany
        country2=France
        if player!=None:
            while (country2.name in country1.neighboringcountries or country1.name in country2.neighboringcountries or country1.continent==country2.continent or country2 in player.list_of_possessed_countries or country1==Unknown_country or country2==Unknown_country or (self.peacemode==1 and (country1.owner!="Nobody" and country2.owner!="Nobody"))):
                country1=player.list_of_possessed_countries[random.randrange(1,len(player.list_of_possessed_countries))]
                country2=all_countries[random.randrange(1,len(all_countries))]
            country1.neighboringcountries.append(country2.name)
            self.wormholed_countries.append([country1,country2])
            create_good_line(country1,country2)
            print(self.linelist)
            return None
        
        for i in range(numberofwormholes):
            
            while (country2.name in country1.neighboringcountries or country1.name in country2.neighboringcountries or country1.continent==country2.continent):
                country1=all_countries[random.randrange(1,len(all_countries))]
                country2=all_countries[random.randrange(1,len(all_countries))]
            country1.neighboringcountries.append(country2.name)
            self.wormholed_countries.append([country1,country2])
            create_good_line(country1,country2)
            print(self.linelist)

    def destroy_all_wormholes(self):
        self.colorarray=["indian red", "dark slate grey", "dark green", "dark violet", "dark goldenrod", "tomato3", "medium violet red", "brown2", "PaleGreen4"]
        for item in self.wormholed_countries:
            item[0].neighboringcountries.remove(item[1].name)
        self.wormholed_countries=list()
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
    
    def popupwinorloose(self,countrya,countryb,property:Category,wl):
        def kill_guessed_correct():
            self.transition(sameplayeragain=True)
            win.destroy()
        def kill_button():
            if wl=="no data" or wl=="draw!":
                self.transition(sameplayeragain=True)
            else:
                self.transition(sameplayeragain=False)
            win.destroy()
        def _on_mousewheel(event):
            canvas11.yview_scroll(int(-1*(float(event.delta)/120)), "units")
        
        additional_information=property.isActive
        win=tk.Toplevel()
        win.geometry("1400x825")
        frame11=tk.Frame(win)
        frame11.pack(fill="both",expand=True)
        canvas11=tk.Canvas(frame11)
        canvas11.pack(side="left",expand=True,fill="both")
        


        my_scrollbar11=tk.Scrollbar(frame11,orient="vertical",command=canvas11.yview)
        my_scrollbar11.pack(side="right",fill="y")
        my_scrollbar11.config(command=canvas11.yview)
        

        frame12=tk.Frame(canvas11)
        canvas11.create_window((0,0),window=frame12,anchor="nw")

        frame12.bind(
            "<Configure>",
            lambda e: canvas11.configure(
                scrollregion=canvas11.bbox("all")
            )
        )


        canvas11.bind_all("<MouseWheel>",_on_mousewheel)
        

        url1="pictures/flag_pictures/w320/" + countrya.gettwocountrycode().lower() + ".png"
        print(countryb.gettwocountrycode())
        print("das war der Code")
        url2="pictures/flag_pictures/w320/" + countryb.gettwocountrycode().lower() + ".png"
        img1=ImageTk.PhotoImage(Image.open(url1))
        img2=ImageTk.PhotoImage(Image.open(url2))
        frame12.img1=img1
        frame12.img2=img2
        panel1=tk.Label(frame12,image=img1)
        panel2=tk.Label(frame12,image=img2)

        url3="pictures/success3.png"
        url4="pictures/fail2.png"
        url5="pictures/vs.png"
        url6="pictures/no_data.png"
        url7="pictures/draw.png"
        url8="pictures/top5.png"
        url9="pictures/worst5.png"
        url10="pictures/great_success.png"

        img3=ImageTk.PhotoImage(Image.open(url3))
        img4=ImageTk.PhotoImage(Image.open(url4))
        img5=ImageTk.PhotoImage(Image.open(url5))
        img6=ImageTk.PhotoImage(Image.open(url6))
        img7=ImageTk.PhotoImage(Image.open(url7))
        img8=ImageTk.PhotoImage(Image.open(url8))
        img9=ImageTk.PhotoImage(Image.open(url9))
        img10=ImageTk.PhotoImage(Image.open(url10))
        


        frame12.img3=img3
        frame12.img4=img4
        frame12.img5=img5
        frame12.img6=img6
        frame12.img7=img7
        frame12.img8=img8
        frame12.img9=img9
        frame12.img10=img10

        panel3=tk.Label(frame12,image=img3)
        panel4=tk.Label(frame12,image=img4)
        panel5=tk.Label(frame12,image=img5)
        panel6=tk.Label(frame12,image=img6)
        panel7=tk.Label(frame12,image=img7)
        panel8_1=tk.Label(frame12,image=img8)
        panel8_2=tk.Label(frame12,image=img8)

        panel9_1=tk.Label(frame12,image=img9)
        panel9_2=tk.Label(frame12,image=img9)


        
        try:
            l1=tk.Label(frame12,text=countrya.name + "\n" + property.name.replace(".csv","") +"\n" +\
                format((countrya.dictofattributes[property.name][0]),",") + "\n" +"worldrank:"+str(countrya.dictofattributes[property.name][1])+ "\n (of " + str(countrya.dictofattributes[property.name][2])+ " countries ranked)",font="Helvetica 25",wraplength=500 )
        except:
            l1=tk.Label(frame12,text=countrya.name + "\n" + property.name.replace(".csv","") +"\n" + "sorry no data",font="Helvetica 25" )
        
        try:
            l2=tk.Label(frame12,text=countryb.name + "\n" + property.name.replace(".csv","") +"\n" + format((countryb.dictofattributes[property.name][0]),",") + "\n" +"worldrank:"+str(countryb.dictofattributes[property.name][1])+ "\n (of " + str(countryb.dictofattributes[property.name][2])+ " countries ranked)",font="Helvetica 25",wraplength=500)
        except:
            traceback.print_exc()
            l2=tk.Label(frame12,text=countryb.name + "\n" + property.name.replace(".csv","") +"\n" + "sorry no data",font="Helvetica 25")
        
        killbutton=tk.Button(frame12,image=img7,command=kill_button,width=400,height=200)

        l1.grid(row=1,column=0)
        l2.grid(row=1,column=2)

        panel1.grid(row=0,column=0)
        panel2.grid(row=0,column=2)
        panel5.grid(row=0,column=1)
        killbutton.grid(row=2,column=1)


        if wl=="you win!":
            killbutton["image"]=img3
            killbutton["width"]=300
            killbutton["height"]=300
            #panel3.grid(row=2,column=1)
            
        if wl=="you loose!":
            killbutton["image"]=img4
            killbutton["width"]=300
            killbutton["height"]=300

        if wl=="no data":
            killbutton["image"]=img6
            killbutton["width"]=300
            killbutton["height"]=300
            

        if wl=="draw!":
            killbutton["image"]=img7
            killbutton["width"]=300
            killbutton["height"]=300
        
        if wl=="hard defeat!":
            killbutton["image"]=img10
            killbutton["width"]=300
            killbutton["height"]=300
            killbutton.configure(command=kill_guessed_correct)

        
        
        if additional_information:
            guessed_correct_button=tk.Button(frame12,text="guessed correct",font="Helvetica 30",command=kill_guessed_correct)
            guessed_correct_button.grid(row=3,column=1)
            try:
                wiki_summary_A_extra=countrya.dictofattributes[property.name][4]
                wiki_summary_B_extra=countryb.dictofattributes[property.name][4]
                wikiurl_A=countrya.dictofattributes[property.name][5]
                wikiurl_B=countryb.dictofattributes[property.name][5]
            except:
                traceback.print_exc()
                wiki_summary_A_extra=""
                wiki_summary_B_extra=""
                wikiurl_A=""
                wikiurl_B=""
            height=320
            try:
                
                urlA="pictures/attribute_pictures/" + property.name.replace(".csv","") + "/"+ countrya.dictofattributes[property.name][3] + ".jpg"
                try:
                    imgA=Image.open(urlA)
                except FileNotFoundError:
                    imgA=Image.open("pictures/no_image_available.png")
                w=float(imgA.width)
                h=float(imgA.height)
                imgA=ImageTk.PhotoImage(imgA.resize((int(height*w/h),int(height)),Image.LANCZOS))
                frame12.imgA=imgA
                panelA=tk.Label(frame12,image=imgA)
                panelA.grid(row=2,column=0)
                panelA_extra=tk.Label(frame12,text=countrya.dictofattributes[property.name][3],font="Helvetica 20",wraplength=500)
                panelA_extra.grid(row=3,column=0)
            except:
                traceback.print_exc()
            try:

                urlB="pictures/attribute_pictures/" + property.name.replace(".csv","") +"/" + countryb.dictofattributes[property.name][3] + ".jpg"
                try:
                    imgB=Image.open(urlB)
                except FileNotFoundError:
                    imgB=Image.open("pictures/no_image_available.png")
                w=float(imgB.width)
                h=float(imgB.height)
                imgB=ImageTk.PhotoImage(imgB.resize((int(height*w/h),int(height)),Image.LANCZOS))
                frame12.imgB=imgB
                
                
                
                panelB=tk.Label(frame12,image=imgB)
                
                panelB.grid(row=2,column=2)

                
                panelB_extra=tk.Label(frame12,text=countryb.dictofattributes[property.name][3],font="Helvetica 20",wraplength=500)
                
                panelB_extra.grid(row=3,column=2)
            except:
                traceback.print_exc()
            try:
                if countrya.dictofattributes[property.name][3]!=countrya.name:
                    if wikiurl_A=="":
                        self.search_string=countrya.dictofattributes[property.name][3]
                        self.search_string=wikipedia.search(self.search_string)[0]
                        print(self.search_string)
                        print(wikipedia.search(self.search_string)[0])
                        print(self.search_string)
                        wiki_url_A=wikipedia.page(self.search_string).url
                        print("hier kommt url")
                        print(type(wiki_url_A))
                        print(wiki_url_A)
                        wiki_summary_A=wikipedia.summary(self.search_string,sentences=2)
                    else:
                        wiki_url_A=wikiurl_A
                        wiki_summary_A=wiki_summary_A_extra
                
                    wiki_url_A_Label=tk.Label(frame12,text=wiki_url_A,fg="blue",cursor="hand2",font="Helvetica 15")
                    wiki_url_A_Label.bind("<Button-1>",lambda x: self.callback(wiki_url_A))

                    wiki_summary_A_Label=tk.Label(frame12,text=wiki_summary_A,wraplength=500,font="Helvetica 15")
                    wiki_summary_A_Label.grid(row=4,column=0)
                    wiki_url_A_Label.grid(row=5,column=0)
            except:
                traceback.print_exc()
            try:
                if countryb.dictofattributes[property.name][3]!=countryb.name:
                    if wikiurl_B=="":
                        self.search_string=countryb.dictofattributes[property.name][3]
                        self.search_string=wikipedia.search(self.search_string)[0]
                        print(self.search_string)
                        print(wikipedia.search(self.search_string)[0])
                        print(self.search_string)
                        wiki_url_B=wikipedia.page(self.search_string).url
                        print("hier kommt url")
                        print(type(wiki_url_B))
                        print(wiki_url_B)
                        wiki_summary_B=wikipedia.summary(self.search_string,sentences=2)
                        
                    else:
                        wiki_url_B=wikiurl_B
                        wiki_summary_B=wiki_summary_B_extra

                    wiki_url_B_Label=tk.Label(frame12,text=wiki_url_B,fg="blue",cursor="hand2",font="Helvetica 15",wraplength=500)
                    wiki_url_B_Label.bind("<Button-1>",lambda x: self.callback(wiki_url_B))
                    
                    wiki_summary_B_Label=tk.Label(frame12,text=wiki_summary_B,wraplength=500,font="Helvetica 15")
                    wiki_summary_B_Label.grid(row=4,column=2)
                    wiki_url_B_Label.grid(row=5,column=2)
            except:
                traceback.print_exc()



        try:
            countrya_top5=countrya.dictofattributes[property.name][1]<6
        except: countrya_top5=False

        try:
            countryb_top5=countryb.dictofattributes[property.name][1]<6
        except: countryb_top5=False

        try:
            countrya_worst5=countrya.dictofattributes[property.name][2]-countrya.dictofattributes[property.name][1] <6
        except:
            countrya_worst5=False
            
        try:
            countryb_worst5=countryb.dictofattributes[property.name][2]-countryb.dictofattributes[property.name][1] <6
        except:
            countryb_worst5=False  

        if countrya_top5:
            panel8_1.grid(row=6,column=0)

        if countryb_top5:
            panel8_2.grid(row=6,column=2)

        if countrya_worst5:
            panel9_1.grid(row=6,column=0)

        if countryb_worst5:
            panel9_2.grid(row=6,column=2)

        

    def endscreen(self,cause="numberofrounds",winner=None,gotcha_country=None):
        def _on_mousewheel(event):
            canvas21.yview_scroll(int(-1*(float(event.delta)/120)), "units")

        win2=tk.Toplevel()

        frame21=tk.Frame(win2)
        frame21.pack(fill="both",expand=True)
        canvas21=tk.Canvas(frame21)

        my_scrollbar12=tk.Scrollbar(frame21,orient="vertical",command=canvas21.yview)
        my_scrollbar12.pack(side="right",fill="y")
        my_scrollbar12.config(command=canvas21.yview)

        my_scrollbar13=tk.Scrollbar(frame21,orient="horizontal",command=canvas21.xview)
        my_scrollbar13.pack(side="bottom",fill="x")
        my_scrollbar13.config(command=canvas21.xview)
        canvas21.pack(side="left",expand=True,fill="both")

        win=tk.Frame(canvas21)
        canvas21.create_window((0,0),window=win,anchor="nw")
        win2.geometry("1650x825")
        win.bind(
            "<Configure>",
            lambda e: canvas21.configure(
                scrollregion=canvas21.bbox("all")
            )
        )
        canvas21.bind_all("<MouseWheel>",_on_mousewheel)


        if self.winningcondition=="get gold":
                a=sorted(self.list_of_players,key=lambda x: self.score(x.list_of_possessed_countries),reverse=True)
                self.shitdict=dict()
                for i in range (len(a)):
                    self.shitdict[i]=dict()
                    text=str(i+1) + ". place : " + a[i].name  + " with " +str(a[i].gold) +  " gold \n"
                    newframe=tk.Frame(win)
                    label1=tk.Label(newframe,text=text)
                    label1.config(font=("Helvetica", 20))
                    flagframe=tk.Frame(newframe)
                    for j in range(len(a[i].list_of_possessed_countries_gold)):
                        self.doubleframe=tk.Frame(flagframe)
                        flag=a[i].list_of_possessed_countries_gold[j].getresizedflag(100)
                        self.newlabel=tk.Label(self.doubleframe,image=flag)
                        countrylabel=tk.Label(self.doubleframe,text=a[i].list_of_possessed_countries_gold[j].name)
                        self.newlabel.pack(side="top")
                        countrylabel.pack(side="bottom")
                        self.shitdict[i][j]=flag
                        self.doubleframe.grid(row=0,column=j)
                    label1.grid(row=0,column=0)
                    flagframe.grid(row=1,column=0)
                    newframe.grid(row=i,column=0)
                self.d="disabled"
                self.showing_country_label["text"]="Congratulations, " + a[0].name
                self.showing_current_attribute_text_label["text"]="Congratulations, " + a[0].name 
                return None
        
        if self.winningcondition=="attribute":
            a=sorted(self.list_of_players,key=lambda x: sum(self.score(x.list_of_possessed_countries)),reverse=True)
            self.shitdict=dict()
            #sorting
            def bla(x):
                try:
                    return x.dictofattributes[self.endattribute.name][0]
                except: 
                    return -9999999.0
            for i in range (len(a)):
                if "higher is better" in self.endattribute.name:
                    a[i].list_of_possessed_countries=sorted(a[i].list_of_possessed_countries,key=lambda x: bla(x),reverse=True)
                else:
                    a[i].list_of_possessed_countries=sorted(a[i].list_of_possessed_countries,key=lambda x: bla(x))
            for i in range (len(a)):
                scorelist=self.score(a[i].list_of_possessed_countries)
                self.shitdict[i]=dict()
                text=str(i+1) + ". place : " + a[i].name  + " with " +str(round(sum(scorelist),2)) +  " points \n"
                newframe=tk.Frame(win)
                label1=tk.Label(newframe,text=text)
                label1.config(font=("Helvetica", 44))
                flagframe=tk.Frame(newframe,highlightbackground="green",highlightthickness=2)
                flagframe.grid_columnconfigure(0,weight=1)
                flagframe.grid_rowconfigure(0,weight=1)
                for j in range(len(a[i].list_of_possessed_countries)):
                        
                    self.doubleframe=tk.Frame(flagframe,highlightbackground="white",highlightthickness=2)
                    self.name_value_rank_frame=tk.Frame(self.doubleframe)
                    

                    flag=a[i].list_of_possessed_countries[j].getresizedflag(100)
                    
                    countryscorelabel=tk.Label(self.doubleframe,text=scorelist[j],font="Helvetica 30")
                    self.newlabel=tk.Label(self.doubleframe,image=flag)
                    country=a[i].list_of_possessed_countries[j]
                    if self.reversed_end_attribute==1:
                        country.dictofattributes[self.endattribute.name][1]=country.dictofattributes[self.endattribute.name][2]-country.dictofattributes[self.endattribute.name][1]


                    countrylabel=tk.Label(self.doubleframe,text=country.name,font="Helvetica 20")
                    self.newlabel.grid(row=0)
                    countryscorelabel.grid(row=1)
                    countrylabel.grid(row=2)
                    if self.endattribute.isActive:
                        try:
                            label_of_thing=tk.Label(self.name_value_rank_frame,text=str(country.dictofattributes[self.endattribute.name][3]),font="Helvetica 20")
                        except:
                            label_of_thing=tk.Label(self.name_value_rank_frame,text="--",font="Helvetica 20")
                        try:
                            width=200                            
                            urlA="pictures/attribute_pictures/" + self.endattribute.name.replace(".csv","") + "/"+ country.dictofattributes[self.endattribute.name][3] + ".jpg"
                            try:
                                imgA=Image.open(urlA)
                            except FileNotFoundError:
                                imgA=Image.open("pictures/no_image_available.png")
                            w=float(imgA.width)
                            h=float(imgA.height)
                            imgA=ImageTk.PhotoImage(imgA.resize((int(width),int(width*h/w)),Image.LANCZOS))
                            panelA=tk.Label(self.doubleframe,image=imgA)
                            panelA.imgA=imgA
                            panelA.grid(row=3)
                        except:
                            traceback.print_exc()
                        label_of_thing.grid(row=0)
                        label_of_value=tk.Label(self.name_value_rank_frame,text=format((country.dictofattributes[self.endattribute.name][0]),","),font="Helvetica 20")
                        label_of_value.grid(row=1)
                        label_of_worldrank=tk.Label(self.name_value_rank_frame,text="worldrank:" + str(country.dictofattributes[self.endattribute.name][1]),font="Helvetica 20")
                        label_of_worldrank.grid(row=2)
                        self.doubleframe.grid_rowconfigure(4,weight=1)
                        self.name_value_rank_frame.grid(row=4,sticky="s")
                    else:
                        label_of_value=tk.Label(self.doubleframe,text=format((country.dictofattributes[self.endattribute.name][0]),","),font="Helvetica 20")
                        label_of_value.grid(row=5,sticky="s")
                        label_of_worldrank=tk.Label(self.doubleframe,text="worldrank:" + str(country.dictofattributes[self.endattribute.name][1]),font="Helvetica 20")
                        label_of_worldrank.grid(row=6,sticky="s")


                    self.shitdict[i][j]=flag
                    self.doubleframe.grid(row=0,column=j,sticky="NS")
                label1.grid(row=0,column=0)
                flagframe.grid(row=1,column=0)
                newframe.grid(row=i,column=0)
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + a[0].name
            self.showing_current_attribute_text_label["text"]="Congratulations, " + a[0].name 
        
        if self.winningcondition=="number of countries":
            a=sorted(self.list_of_players,key=lambda x: float((len(x.list_of_possessed_countries)) +random.random()),reverse=True)
            self.shitdict=dict()
            for i in range (len(a)):
                self.shitdict[i]=dict()
                text=str(i+1) + ". place : " + a[i].name  + " with " +str(len(a[i].list_of_possessed_countries)) +  " countries \n"
                newframe=tk.Frame(win)
                label1=tk.Label(newframe,text=text)
                label1.config(font=("Helvetica", 44))
                flagframe=tk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries)):
                    self.doubleframe=tk.Frame(flagframe)
                    flag=a[i].list_of_possessed_countries[j].getresizedflag(100)
                    self.newlabel=tk.Label(self.doubleframe,image=flag)
                    countrylabel=tk.Label(self.doubleframe,text=a[i].list_of_possessed_countries[j].name)
                    self.newlabel.pack(side="top")
                    countrylabel.pack(side="bottom")
                    self.shitdict[i][j]=flag
                    self.doubleframe.grid(row=0,column=j)
                label1.grid(row=0,column=0)
                flagframe.grid(row=1,column=0)
                newframe.grid(row=i,column=0)
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + a[0].name
            self.showing_current_attribute_text_label["text"]="Congratulations, " + a[0].name 
        if cause=="twocountriesclaimed":
            text=""
            winner=self.targetcountry1.owner
            messagebox.showinfo(self.root,message="Congratulations " + winner + " you claimed both countries and therefore you are the winner")
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + winner
            self.showing_current_attribute_text_label["text"]="Congratulations, " + winner
        if self.winningcondition=="secret targets":
            a=sorted(self.list_of_players,key=lambda x: float((len(set(x.list_of_possessed_countries).intersection(set(self.dict_of_targets[x])))) +random.random()),reverse=True)
            self.shitdict=dict()
            for i in range (len(a)):
                self.shitdict[i]=dict()
                text=str(i+1) + ". place : " + a[i].name
                newframe=tk.Frame(win)
                label1=tk.Label(newframe,text=text)
                label1.config(font=("Helvetica", 44))
                flagframe=tk.Frame(newframe)
                for j in range(len(a[i].list_of_possessed_countries)):
                    if a[i].list_of_possessed_countries[j] in self.dict_of_targets[a[i]]:
                        self.doubleframe=tk.Frame(flagframe)
                        flag=a[i].list_of_possessed_countries[j].getresizedflag(100)
                        self.newlabel=tk.Label(self.doubleframe,image=flag)
                        countrylabel=tk.Label(self.doubleframe,text=a[i].list_of_possessed_countries[j].name)
                        self.newlabel.pack(side="top")
                        countrylabel.pack(side="bottom")
                        self.shitdict[i][j]=flag
                        self.doubleframe.grid(row=0,column=j)
                label1.grid(row=0,column=0)
                flagframe.grid(row=1,column=0)
                newframe.grid(row=i,column=0)
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + a[0].name
            self.showing_current_attribute_text_label["text"]="Congratulations, " + a[0].name
        if self.winningcondition=="secret attribute":
            text=""
            self.d="disabled"
            self.showing_country_label["text"]="Congratulations, " + winner.name
            self.showing_current_attribute_text_label["text"]="Congratulations, " + winner.name
            showing_winner_label=tk.Label(win,text="Congratulations, " + winner.name + "\nbecause " + gotcha_country.name + " is worldrank\n" + str(self.dict_of_targets[winner].index(gotcha_country)+1) + "\nin\n" + self.dict_of_target_attribute_name[winner] + "\nyou win the game!!!",font="Helvetivca 30")
            showing_winner_label.grid(row=0,column=0)

        
    def setupclaim2countries(self):
        Target=Player(realgrey,"Nobody")
        if self.choosingindex==len(self.list_of_players):
            self.targetcountry1=all_countries[random.randrange(1,len(all_countries))]
            self.targetcountry2=all_countries[random.randrange(1,len(all_countries))]
            if self.targetcountry1.name ==self.targetcountry2.name:
                self.targetcountry2=all_countries[random.randrange(1,len(all_countries))]
            self.claimcountry(Target,self.targetcountry1)
            print(self.targetcountry1.name)
            self.claimcountry(Target,self.targetcountry2)
    def setupgold(self):
        def get_good_ids(numberofgold):
            self.goldids=random.sample(range(len(all_countries)),numberofgold)
            for i in self.goldids:
                if all_countries[i].owner!="Nobody" or all_countries[i].name=="Unknown Country":
                    get_good_ids(numberofgold)
            return None
        for player in self.list_of_players:
            player.gold=0
        Target=Player(gold,"Nobody")
        self.numberofgold=len(all_countries)//20
        print(self.numberofgold)
        get_good_ids(self.numberofgold)
        for i in self.goldids:
            self.claimcountry(Target,all_countries[i])
            self.goldlist.append(all_countries[i])
            
    def getstartingattribute(self) -> Category:
        if self.pred_attribute_name!="Random":
            print(self.pred_attribute_name)
            attribute= dictionary_attribute_name_to_attribute[self.pred_attribute_name][0]
            
        else:
            numberofnodata=999999
            while numberofnodata >5:
                attribute=self.getrandomattribute_with_cluster()
                numberofnodata=0
                for country in all_countries:
                    try:
                        if isinstance(country.dictofattributes[attribute],list):
                            try:
                                i=country.dictofattributes[attribute][1]
                            except IndexError:
                                numberofnodata=numberofnodata+1
                        else:
                            numberofnodata=numberofnodata+1
                    except KeyError:
                        numberofnodata+=1
            if random.random()<0.5:

                text="The target attribute is " + attribute
                v=messagebox.showinfo(self.main,message=text)
                self.reversed_end_attribute=0
                
            else:
                self.reversed_end_attribute=1
                text="The target attribute is " + attribute + "\n REVERSED!!!"
                v=messagebox.showinfo(self.main,message=text)
        return attribute



    def setuppredattribute(self):
        self.endattribute=self.getstartingattribute()
        if True:
            self.grey_no_data()
    
    def grey_no_data(self):
        for country in all_countries:
            if country==Unknown_country:
                continue
            try:
                country.dictofattributes[self.endattribute.name][0]
            except:
                print(country.name)
                traceback.print_exc()
                self.claimcountry(No_Data_Body,country)

    
    def setup_secret_target_countries(self,numberoftargets:int):
        self.really_unknown=Unknown_country
        def checkcountrylist(list1):
            for country in list1:
                if country.owner!="Nobody" or country==self.really_unknown:
                    return False
            return True
        def roll_random_country(oldcountry):
            return all_countries[random.randrange(1,len(all_countries))]

        def show_targets(player:Player):
            self.no_targets_yetlist.remove(player)
            self.target_countries_frame=tk.Toplevel()
            targetlist=[Unknown_country]*numberoftargets
            while (not checkcountrylist(targetlist)):
                targetlist=[roll_random_country(item) for item in targetlist]

            welcomelabel=tk.Label(self.target_countries_frame,text="Welcome " + player.name + " those are your countries\n if you don't know where these are feel free to look at the map.",font="Helvetica 25")
            welcomelabel.grid(row=0,column=0,columnspan=len(targetlist))
            self.myimage=[0]*numberoftargets
            self.created_circles=list()
            for index,country in enumerate(targetlist):
                item=self.c.create_oval(country.wormholecoordinates[0]+20,country.wormholecoordinates[1]+20,country.wormholecoordinates[0]-20,country.wormholecoordinates[1]-20,width=3,outline="red")
                self.created_circles.append(item)
                newcountrylabel=tk.Label(self.target_countries_frame, text=country.name,font="Helvetica 25")
                newcountrylabel.grid(row=1,column=index)
                self.myimage[index]=country.getresizedflag(400)
                newlabel=tk.Label(self.target_countries_frame,image=self.myimage[index],pady=40)
                newlabel.grid(row=2,column=index)
                pass
            self.dict_of_targets[player]=targetlist
            self.got_targets_Button=tk.Button(self.target_countries_frame,text="got it",command=open_next_frame,font="Helvetica 25")
            self.got_targets_Button.grid(row=3,column=0,columnspan=len(targetlist)+2)

        def open_next_frame():
            for item in self.created_circles:
                self.c.delete(item)
            self.created_circles=[]
            self.target_countries_frame.destroy()
            if len(self.no_targets_yetlist)==0:
                return None
            show_targets(self.no_targets_yetlist[0])
        self.dict_of_targets=dict()
        self.no_targets_yetlist=self.list_of_players.copy()
        show_targets(self.active_player)


    def setup_secret_attribute(self,n):
        def find_top_n_countries(n,attribute):
            returnlist=list()
            for country in all_countries:
                try:
                    if country.dictofattributes[attribute][1]<=n:
                        returnlist.append(country)
                except KeyError:
                    continue
            returnlist.sort(key=lambda x: x.dictofattributes[attribute][1])
            return returnlist



        def open_next_frame():
            self.target_countries_frame.destroy()
            if len(self.no_targets_yetlist)==0:
                return None
            show_targets(self.no_targets_yetlist[0])
        
        def show_targets(player:Player):
            self.no_targets_yetlist.remove(player)
            self.target_countries_frame=tk.Toplevel()
            self.target_attribute=self.getrandomattribute_with_cluster()
            self.dict_of_target_attribute_name[player]=self.target_attribute
            welcomelabel=tk.Label(self.target_countries_frame,text="Welcome " + player.name + "your attribute is the following: \n\n" + self.target_attribute.rstrip(".csv") + "\n\nclaim one of the top " +str(n) + " countries in order to win the game" ,font="Helvetica 25")
            welcomelabel.grid(row=0,column=0)
            self.dict_of_targets[player]=find_top_n_countries(n,self.target_attribute)
            self.got_targets_Button=tk.Button(self.target_countries_frame,text="got it",command=open_next_frame,font="Helvetica 25")
            self.got_targets_Button.grid(row=3,column=0) 
       
        self.dict_of_target_attribute_name=dict()
        self.dict_of_targets=dict()
        self.no_targets_yetlist=self.list_of_players.copy()
        show_targets(self.active_player)



    def score(self,countrylist):
        def helphelp(number,list1):
            if self.higherorlower=="higher":
                return  sum([item<=number for item in list1])
            if self.higherorlower=="lower":
                return sum([item>=number for item in list1])
        
        higherorlower=""
        propertylist=list()
        mcountrylist=list()
        dlist=list()
        if self.reversed_end_attribute==0:
            if "higher is better" in self.endattribute.name:
                self.higherorlower="higher"
            else:
                self.higherorlower="lower"
        else:
            if "higher is better" in self.endattribute.name:
                self.higherorlower="lower"
            else:
                self.higherorlower="higher"

        for country in all_countries:
            try:
                if (country.dictofattributes[self.endattribute.name][0])!=float(-1):
                    propertylist.append((country.dictofattributes[self.endattribute.name][0]))            
                    mcountrylist.append(country)
                else: 
                    dlist.append(country)
            except KeyError:
                dlist.append(country)
        print(propertylist)
        returnlist=list()
        for country in countrylist:
            if country in dlist:
                returnlist.append(30.0)
            else:
                returnlist.append(helphelp(country.dictofattributes[self.endattribute.name][0],propertylist))
        returnlist=[float(item)/float(5) for item in returnlist]
        return returnlist        


    def checkifgameshouldend(self):
        if self.activeplayercounter==len(self.list_of_players)*self.numberofrounds-1:
            self.endscreen()
            return True
        if self.winningcondition=="claim 2 countries":
            if self.targetcountry1.owner!="Nobody" and self.targetcountry1.owner==self.targetcountry2.owner:
                self.endscreen(cause="twocountriesclaimed")
                return True
        if self.winningcondition=="get gold":
            if len(self.goldlist)==0:
                self.endscreen(cause="all gold left")
                return True
        if self.winningcondition=="secret targets":
            if set(self.dict_of_targets[self.active_player]).issubset(set(self.active_player.list_of_possessed_countries)):
                self.endscreen(cause="co")
                return True
        if self.winningcondition=="secret attribute":
            if len(set(self.dict_of_targets[self.active_player]).intersection(set(self.active_player.list_of_possessed_countries)))>=1:
                for country in self.active_player.list_of_possessed_countries:
                    if country in self.dict_of_targets[self.active_player]:
                        self.endscreen(cause="co",winner=self.active_player,gotcha_country=country)
                        break
                return True
        return False

    def setupgame(self):
        
        if self.wormholemode=="fixed starting wormholes":
            self.activate_wormholes(5)
        if self.wormholemode=="every round changing wormholes":
            self.activate_wormholes(3)

        if self.winningcondition=="claim 2 countries":
            self.setupclaim2countries()
        if self.winningcondition=="get gold":
            self.setupgold()
        if self.winningcondition=="attribute":
            self.setuppredattribute()
        if self.winningcondition=="secret targets":
            self.setup_secret_target_countries(self
            .numberoftargets)
        if self.winningcondition=="secret attribute":
            self.setup_secret_attribute(5)

    def scroll_start(self, event):
        self.c.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.c.scan_dragto(event.x, event.y, gain=1)

    def do_zoom(self,event):
        x = self.c.canvasx(event.x)
        y = self.c.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.c.scale(ALL, x, y, factor, factor)


