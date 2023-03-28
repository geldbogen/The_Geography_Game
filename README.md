# The_Geography_Game
## Introduction
Welcome to the Geography-Game :earth_africa:

This is a Risk-inspired (https://en.wikipedia.org/wiki/Risk_(game)) digital board game, powered by real-world data. 

As in the game Risk, you want to expand your empire as much as possible and claim as many countries as possible.

![grafik](https://user-images.githubusercontent.com/65167682/228289010-e0c22f31-facc-47f0-a5ab-4f304403f137.png)

The game is for any amount of players (although 2-4 are recommended) and a usual round takes around one hour to complete.

## Basic Rules
The game is (as any normal board game) played in turns. 
Assume we play with three players A 🔴 ,B 🔵, and C 🟢.
After starting the game and choosing a color for each player the interface looks like this:

![grafik](https://user-images.githubusercontent.com/65167682/228300958-3ec3f7a5-b6d9-49f4-9cd5-4660c1d16b62.png)

Hold the right mouse button, and drag the screen to scroll around.

https://user-images.githubusercontent.com/65167682/228301570-970de7ad-02fc-4357-992e-64ed1e92e220.mp4

The lower part of the screen tells you, whose turn it is, and which country (if any) they have already selected. 

![AAA](https://user-images.githubusercontent.com/65167682/228302144-02d21a91-b31e-496d-aa37-2416bfcbe881.png)


Click on a country with the left mouse button, to select it.
For example after A 🔴 clicked on the United States, you can see the following:

![AAB](https://user-images.githubusercontent.com/65167682/228303243-21e65227-19c8-456d-9749-e9505e3059b6.png)

Now, because A 🔴 owns the United States, he can attack with that country. This means, that, after he clicked on the USA, he can click on any neighboring country (or a country with a black line connecting the United States, e.g. the United Kingdom), leading to the following screen:

![AAD](https://user-images.githubusercontent.com/65167682/228306005-a8f1d42a-dd00-416d-a0e0-354217695148.png)

Now, if A 🔴 clicks on the "Attack!" button, an attack is initated.
But how do we determine, if the attack is succesful? Here, the real-world data comes into play. 
On the upper part of the screen you can see the following:

![AAE](https://user-images.githubusercontent.com/65167682/228307041-a951801f-eb54-49a1-a56b-9e245b50157e.png)


Every turn a new attribute is randomly chosen. In this case, it is "number of urban areas with more than 1 mio. citizens" (we only deal with this attribute for the rest of this instruction). This attribute determines, whether you are succesful with your attack. For example, after A 🔴 starts the attack, he would see the following:

![grafik](https://user-images.githubusercontent.com/65167682/228307642-34a3dd19-6da7-4480-83be-0de1ca263611.png)

You can get the following informations from this window:
The United States has 43 urban areas with more than 1 mio. citizens, while Canada has 6. 

![AAF](https://user-images.githubusercontent.com/65167682/228308288-5a07f409-0d0f-434b-a89e-d4c84e4c7a28.png)

Because the United States has more, A 🔴's attack is succesful and Canada now belongs to  A 🔴. 

 A 🔴 can click now on the "success" button to close the window and give the turn to B 🔵.

https://user-images.githubusercontent.com/65167682/228309367-4d4b93c1-3ace-43ef-b17f-e6ef15aeef1c.mp4


Now, it is B 🔵's turn. They think, that France has mor urban areas than Germany, hence they attack Germany with France.

![grafik](https://user-images.githubusercontent.com/65167682/228323090-8d7c403b-6dc6-4670-b1aa-ed22f5c1bea8.png)

However, because Germany has actually more urban areas than France (4 in France and 7 in Germany), they do not get Germany, and their attack fail. After clicking on the "Fail"-Button it is C 🟢's turn. The game usually ends after a specific number of turns is played (see section game modes for more details). Let us skip the turn of C 🟢 (who was able to capture Italy) and come to the next turn of  A 🔴 . The board looks like this:

![grafik](https://user-images.githubusercontent.com/65167682/228324444-a7ef920d-7198-4f07-8eec-afccc7348459.png)


Now, because  A 🔴 owns both, Canada and USA, they can attack with Canada Ireland. They can also attack Mexico with the USA. However, they can NOT attack Mexico with Canada. Only neighboring countries can attack each other.

## More Rules

### Dealing with missing data
If one of the countries don't have any data (or it is missing) regarding the current attribute, the Button changes to a pondering emoji and the player whose turn it was may attack again.
This usually looks like this:

![grafik](https://user-images.githubusercontent.com/65167682/228331533-46246e78-2351-4a5b-82f0-12f1b1fb262c.png)


### Attacking other people's country

Unless you play in peace mode (see section "game modes" for more details), you are able to attack countries which are possessed by other players. However this comes with a caveat: if your attack fails, the attacked player claims the country of the origin of the attack.
Compare the following board state:

![grafik](https://user-images.githubusercontent.com/65167682/228326238-b171578a-44c3-43de-9d29-4843d43cb824.png)

As you can see, the current attribute is "number of airports". Now, player  A 🔴 thinks, that Portugal has more airports than Spain. Therefore he attacks Spain (currently under control of B 🔵) with Portugal

However, he fails.

![grafik](https://user-images.githubusercontent.com/65167682/228326622-d817d066-4798-4e70-8c7f-5de81e5c6082.png)

After this failed attack, B 🔵 immediately takes control of the country where the attack started from (in this case, Portugal), and the board state looks like this:

![grafik](https://user-images.githubusercontent.com/65167682/228326859-9b9d25ce-6e73-4f74-8121-6c0ec433d632.png)

### Rerolls
Every player starts with a set amount of rerolls. They are indicated on the bottom-left corner:

![AAG](https://user-images.githubusercontent.com/65167682/228332402-5da78646-314e-4956-a3e2-a3c2a2efb99c.png)


While it's their turn any player may click on this button in order to get a new atteribute.

### Strong victory

If your country wins with at least 100 worldranks difference, you will get an extra turn. For example, assume the following board state:

![grafik](https://user-images.githubusercontent.com/65167682/228329960-8d1a4666-8515-4332-9eb3-0cc43e001ddf.png)

Because B 🔵 thinks, that France has more airports than Luxembourg (the small nation between France and Germany) they attack it. 
In Fact, because the difference between France and Luxembourg is so big (at least airport-wise) the button changes to "Great Success" and B 🔵 gets an extra turn after this.

![grafik](https://user-images.githubusercontent.com/65167682/228330583-b64d2529-9c58-424a-9264-c3bde8d88acd.png)

