class Country:
    def __init__(self,xcoordinate,ycoordinate,name,continent=None):
        self.coordinatelist=[]
        for i in range (len(xcoordinate)):
            self.coordinatelist.append((xcoordinate[i],ycoordinate[i]))
        self.xcoordinate=xcoordinate
        self.neighboringcountries=[]
        self.ycoordinate=ycoordinate
        self.dictofattributes=dict()
        self.name=name
        self.owner="Nobody"
        self.continent=continent
        preallCountries.append(self)
        self.savelocation="data/npdata/" + self.name + "-nparray.npy"
        self.wormholecoordinates=[resize_ratio[0]* xcoordinate[0],resize_ratio[1]*ycoordinate[0]]

    def getcolor(self,image):
        output=[]
        for coordinates in self.coordinatelist:
            output.append(image.getpixel(coordinates))
        return output
    def gettwocountrycode(self) -> str:
        if self.name=="Ivory Coast":
            return "ci"
        if self.name=="Myanmar":
            return "mm"
        if self.name=="Democratic Republic of the Congo":
            return "cd"
        if self.name=="Bosnia and Herzegovina":
            return "ba"
        if self.name=="Czech Republic":
            return "cz"
        if self.name=="Republic of the Congo":
            return "cg"
        for item in countries_for_language_en:
            if item[1]==self.name:
                return item[0]
        return "noflag"
    def setpixels(self,image):
        if self.name=="Unknown Country":
            return None
        print(self.name)
        savearray=np.zeros(shape=(1,2))
        for coordinate in self.coordinatelist:
            image2=image
            seed=(coordinate[0],coordinate[1])
            ImageDraw.floodfill(image2,seed,(0,255,0),thresh=200)
            npimage=np.array(image2)
            print(npimage.shape)
            green=np.array([0,255,0],dtype=np.uint8)
            greens=list(zip(*np.where(np.all((npimage==green),axis=-1))))
            sarray=np.array([*greens])
            savearray=np.append(savearray,sarray,axis=0)
            print(sarray)
            print(sarray.shape)
            print(savearray.shape)
        with open(self.savelocation,"wb") as f:
            np.save(f,savearray)
    def getresizedflag(self,height):
        countryurl="pictures/flag_pictures/w1280/" + self.gettwocountrycode().lower() + ".png"
        flagimage=(Image.open(countryurl))
        w=float(flagimage.width)
        h=float(flagimage.height)
        return ImageTk.PhotoImage(flagimage.resize((int(height*w/h),int(height)),Image.LANCZOS))
    def loadpixels(self):
        global all_countries
        global countrynamelist
        if self.name=="Unknown Country":
            self.set_of_pixels=set()
            all_countries.append(self)
            countrynamelist.append(self.name)
            return None
        try:
            print(self.name)
            marray=np.load(self.savelocation,allow_pickle=True)
            marray=marray.T
            self.set_of_pixels=set(zip(marray[0],marray[1]))
        except Exception as e:
            print(str(e))
            self.setpixels(pngim)  
        all_countries.append(self)
        countrynamelist.append(self.name)