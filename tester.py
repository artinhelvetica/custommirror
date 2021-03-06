import sys
import tkinter as tk
from PIL import Image, ImageTk
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from io import BytesIO

#from account on spotify for developers, eventually make it read from file
cid = '665d32e35f5f407d9b3b4b64757950a1' #client ID
secret = '8e9be54517c7464fbd09d1cc2d45f000' #client Secret

#mappping icons
icon_manager = {
    'spotify' : "icons\\spotify.png",
    'album' : "icons\\album.jfif"
}
 
class spotify_display(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, background = 'black')
        #will have to make your own spotify developers account for these
        self.client_id = cid
        self.client_secret = secret
        self.username = 'ivotix343'

        
        #test for retrieving user data, scope to read currently playing set
        token = sp.util.prompt_for_user_token(self.username, 'user-read-currently-playing', self.client_id, self.client_secret,"https://localhost:8888/callback")

        if token:
            self.spot = sp.Spotify(auth=token)
            self.result = self.spot.currently_playing()

            if self.result is not None:
                #display Album Art
                self.songart = self.result['item']['album']['images'][1]['url']
                image = Image.open(BytesIO((requests.get(self.songart)).content))
                image = image.resize((300,300), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                self.albumartlb = tk.Label(self, image = photo, background = 'black')
                self.albumartlb.image = photo #keep a reference else it wont display
                self.albumartlb.pack(side = 'top', anchor = 'ne')

                #display Song and Artist
                self.songtxt = str(self.result['item']['name']) + " by " + str(self.result['item']['artists'][0]['name'])
                self.songlb = tk.Label(self, text = self.songtxt, font = ('Helvetica', 10), fg = "white", background = "black")
                self.songlb.pack(side = 'bottom', anchor = 'center', pady = 50)
            else:
                #message for no music playing
                self.wlb = tk.Label(self, text = 'No Music Currently Playing', font = ('Helvetica', 10), fg = "white", background = "black")
                self.wlb.pack(side = 'bottom', anchor = 'center', pady = 50)
        else:
            #message for authentication problems
            self.wlb = tk.Label(self, text = 'Cant get token', font = ('Helvetica', 10), fg = "white", background = "black")
            self.wlb.pack(side = 'bottom', anchor = 'center', pady = 50)


class weather_display(tk.Frame):
    #need to find a good weather api
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, background = 'black')

        self.wtxt = 'Dallas 62 degrees, cloudy'
        self.wlb = tk.Label(self, text = self.wtxt, font = ('Helvetica', 10), fg = "white", background = "black")
        self.wlb.pack(side = 'bottom', anchor = 'center', pady = 50)

        image = Image.open("icons\\cloud2.jfif")
        image = image.resize((400,300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.wplb = tk.Label(self, image = photo, background = 'black')
        self.wplb.image = photo
        self.wplb.pack(side = 'top', anchor = 'center')


class google_display(tk.Frame):
    #this will probably pull from a seperate c++ or node.js file
    #will display user request via google assistant API 
    #will also display Assistant response
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, background = 'black')

        self.assistantrp = 'Good Morning Art, How may I help you?'
        self.alb = tk.Label(self, text = self.assistantrp, font = ('Helvetica', 10,"italic" ), fg = "white", background = "black")
        self.alb.pack(side = 'top', anchor = 'n', pady = 5)

        self.userrp = 'Play Kanashii Ureshii on Spotify.'
        self.ulb = tk.Label(self, text = self.userrp, font = ('Helvetica', 10,"italic" ), fg = "white", background = "black")
        self.ulb.pack(side = 'bottom', anchor = 's', pady = 5)


class news_display(tk.Frame):
    #need to find a good news api to pull from
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, background = 'black')

        self.news1 = 'Map: Confirmed coronavirus cases, worldwide'
        self.n1lb = tk.Label(self, text = self.news1, font = ('Helvetica', 10), fg = "white", background = "black")
        self.n1lb.pack(side = 'top', anchor = 'n', pady = 5)

        self.news2 = 'Group fights for Taiwanese Americans to be counted in census'
        self.n2lb = tk.Label(self, text = self.news2, font = ('Helvetica', 10), fg = "white", background = "black")
        self.n2lb.pack(side = 'bottom', anchor = 's', pady = 5)



class startupscreen:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Software Architecture Demo")
        self.window.geometry("1000x800")
        self.window.configure(background = 'black')

        self.topFrame = tk.Frame(self.window, background = 'black')
        self.bottomFrame = tk.Frame(self.window, background = 'black')
        self.topFrame.pack(side = 'top', pady = 20)
        self.bottomFrame.pack(side = 'bottom')

        #this is where we would configure different applications
        #Spotify Display (top right)
        self.music = spotify_display(self.topFrame)
        self.music.pack(side = 'right', anchor = 'e', padx = 100)

        #Clock and Weather Display (top left)
        self.weather = weather_display(self.topFrame)
        self.weather.pack(side = 'left', anchor = 'w', padx = 100)

        #Google Assistant Display(top of bottom half)
        #will only display if assistent is active, else blank
        self.goog = google_display(self.bottomFrame)
        self.goog.pack(side = 'top', anchor = 'n', pady = 50)

        #News Display (bottom of bottom half)
        self.news = news_display(self.bottomFrame)
        self.news.pack(side = 'bottom', anchor = 's', pady = 50)


if __name__ == '__main__':
    ma = startupscreen()
    ma.window.mainloop()