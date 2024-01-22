from globalDefinitions import allPlayers, realgrey

class Player:
    def __init__(self,color,name,reroll_number=3):
        # name of the player
        self.name=name

        # color of the player (on the map)
        self.color=color
        
        # a collection of the flags of the countries that player possesses
        self.labeldict=dict()

        # a list of all countries the player currently controls
        self.list_of_possessed_countries=[]

        # a list of all countries with gold, which the player currently controls
        self.list_of_possessed_countries_gold=[]
        
        # a dictionary needed to translate between 
        # the name of the player and the corresponding class        
        allPlayers[self.name]=self

        # the number of rerolls the player has left
        self.rerolls_left=reroll_number

mrNobody = Player(color="white", name="Nobody")
No_Data_Body = Player(color=realgrey, name="Nobody")