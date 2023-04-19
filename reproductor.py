from tkinter import *
from tkinter import ttk
import pygame
import os

class MusicPlayer:

  def __init__(self,root):
    self.root = root
    self.root.title("Music Player")
    self.root.geometry("1000x200")
    pygame.init()
    pygame.mixer.init()
    self.track = StringVar()
    self.status = StringVar()

    home = os.path.expanduser("~")

    allowed_extensions = ['.mp3', '.wav', '.ogg']
    disallowed_extensions = ['.jpg', '.apk', '.pdf', '.png']
    
     # Agregar estilo para botones redondeados
    style = ttk.Style()
    style.configure('RoundedButton.TButton', borderwidth=0, relief="flat", background="#B0FC38", foreground="navyblue", font=("arial", 16, "bold"), padding=10, width=8, anchor="center")
    style.map('RoundedButton.TButton', background=[('active', '#8F00FF')])


    trackframe = LabelFrame(self.root,text="Song Track",font=("arial",15,"bold"),bg="#8F00FF",fg="white",bd=5,relief=GROOVE)
    trackframe.place(x=0,y=0,width=600,height=100)
    songtrack = Label(trackframe,textvariable=self.track,width=20,font=("arial",24,"bold"),bg="#8F00FF",fg="#B0FC38").grid(row=0,column=0,padx=10,pady=5)
    trackstatus = Label(trackframe,textvariable=self.status,font=("arial",24,"bold"),bg="#8F00FF",fg="#B0FC38").grid(row=0,column=1,padx=10,pady=5)

    buttonframe = LabelFrame(self.root,text="Control Panel",font=("arial",15,"bold"),bg="#8F00FF",fg="white",bd=5,relief=GROOVE)
    buttonframe.place(x=0,y=100,width=600,height=100)

    # Boton de play
    playbtn = ttk.Button(buttonframe,text="PLAY",command=self.playsong, style='RoundedButton.TButton' )
    playbtn.grid(row=0,column=0,padx=10,pady=5)

    # Boton de pausa
    playbtn = ttk.Button(buttonframe,text="PAUSE",command=self.pausesong,style='RoundedButton.TButton')
    playbtn.grid(row=0,column=1,padx=10,pady=5)

    # Boton de despausa
    playbtn = ttk.Button(buttonframe,text="UNPAUSE",command=self.unpausesong, style='RoundedButton.TButton')
    playbtn.grid(row=0,column=2,padx=10,pady=5)

    #boton de pausa
    playbtn = ttk.Button(buttonframe,text="STOP",command=self.stopsong,style="RoundedButton.TButton")
    playbtn.grid(row=0,column=3,padx=10,pady=5)
#    backbtn = Button(buttonframe,text="BACK",command=self.back_folder,width=6,height=1,font=("arial",16,"bold"),fg="white",bg="#B0FC38").grid(row=0,column=4,padx=10,pady=5)



    songsframe = LabelFrame(self.root,text="Song Playlist",font=("arial",15,"bold"),bg="#8F00FF",fg="white",bd=5,relief=GROOVE)
    songsframe.place(x=600,y=0,width=400,height=200)
    scroll_y = Scrollbar(songsframe,orient=VERTICAL)
    self.playlist = Listbox(songsframe,yscrollcommand=scroll_y.set,selectbackground="#B0FC38",selectmode=SINGLE,font=("arial",12,"bold"),bg="#CF9FFF",fg="navyblue",bd=5,relief=GROOVE)
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_y.config(command=self.playlist.yview)
    self.playlist.pack(fill=BOTH)
    os.chdir(home)
    songtracks = os.listdir()
    
    for track in songtracks:
        ext = os.path.splitext(track)[1].lower()
        if ext not in disallowed_extensions:
            self.playlist.insert(END, track)
    
    for track in songtracks:
        if os.path.isdir(track):
           continue           
        ext = os.path.splitext(track)[1]
        if ext in allowed_extensions or ext[1:] in allowed_extensions:
            self.playlist.insert(END, track)

    for track in songtracks:
      self.playlist.insert(END,track)
    self.playlist.bind("<Double-Button-1>", self.open_folder)

    # if os.path.isdir(track) or os.path.splitext(track)[1] in allowed_extensions:
    #         self.playlist.insert(END, track)
    
  


  def playsong(self):
    self.track.set(self.playlist.get(ACTIVE))
    self.status.set("-Playing")
    pygame.mixer.music.load(self.playlist.get(ACTIVE))
    pygame.mixer.music.play()

  def open_folder(self, event):
        selected_song = self.playlist.get(self.playlist.curselection())
        if os.path.isdir(selected_song):
            os.chdir(selected_song)
            self.playlist.delete(0, END)
        # Agrega botón de regresar
            self.playlist.insert(END, "..")
            songtracks = os.listdir()
            for track in songtracks:
                self.playlist.insert(END, track)

    # Función para regresar al directorio anterior
  def go_back():
        os.chdir("..")
        self.playlist.delete(0, END)
        songtracks = os.listdir()
        for track in songtracks:
            self.playlist.insert(END, track)


  def stopsong(self):
    self.status.set("-Stopped")
    pygame.mixer.music.stop()

  def pausesong(self):
    self.status.set("-Paused")
    pygame.mixer.music.pause()

  def unpausesong(self):
    self.status.set("-Playing")
    pygame.mixer.music.unpause()

root = Tk()
MusicPlayer(root)
root.mainloop()
