from tkinter import *
from tkinter import ttk
import pygame
import os
import eyed3
from PIL import Image, ImageTk, ImageOps
import io

def is_audio_file(file_path):
  audio_extensions = ('.mp3', '.wav', '.flac', '.ogg', '.m4a')
  return file_path.lower().endswith(audio_extensions)



class MusicPlayer:

  def __init__(self,root):
    self.root = root
    self.root.title("Music Player")
    self.root.geometry("980x500")
    #self.root.resizable(False, False)
    pygame.init()
    pygame.mixer.init()
    self.track = StringVar()
    self.status = StringVar()
    
    home = os.path.expanduser("~")


    allowed_extensions = ['.mp3', '.wav', '.ogg']
    disallowed_extensions = ['.jpg', '.apk', '.pdf', '.png']

    # Añade un marco para la información de la canción
    info_frame = LabelFrame(self.root, text="Song Info", font=("arial", 15, "bold"), bg="#8F00FF", fg="white", bd=5, relief=GROOVE)
    info_frame.place(x=0, y=200, width=980, height=300)

     # Añade un widget para mostrar la portada del álbum
    self.album_art = Label(info_frame, bg="#8F00FF", width=400, height=400)
    self.album_art.pack(side=LEFT, padx=10, pady=5)

      # Añade un widget para mostrar el autor de la canción
    self.author_label = Label(info_frame, text="Autor: sin autor", font=("arial", 18, "bold"), bg="#8F00FF", fg="#B0FC38")
    self.author_label.pack(side=LEFT, padx=10, pady=5)


    style = ttk.Style()
    style.configure('RoundedButton.TButton', borderwidth=5, relief="flat", background="#B0FC38", foreground="navyblue", font=("arial", 12, "bold"), padding=6, width=8, anchor="center")
    style.map('RoundedButton.TButton', background=[('active', '#8F00FF')])

    #play_image = PhotoImage(file="recursos/play.png")
    play_img = Image.open("recursos/play.png")
    play_img = play_img.resize((20,20))
    # Agregar padding de 10 pixeles a cada lado
    play_img = ImageOps.expand(play_img, border=(10, 0, 10, 0))

    pause_img = Image.open("recursos/pause.png")
    pause_img = pause_img.resize((20,20))
    # Agregar padding de 10 pixeles a cada lado
    pause_img = ImageOps.expand(pause_img, border=(10, 0, 10, 0))

    unpause_img = Image.open("recursos/unpause.png")
    unpause_img = unpause_img.resize((20,20))
    # Agregar padding de 10 pixeles a cada lado
    unpause_img = ImageOps.expand(unpause_img, border=(10, 0, 10, 0))

    
    stop_img = Image.open("recursos/stop.png")
    stop_img = stop_img.resize((20,20))
    # Agregar padding de 10 pixeles a cada lado
    stop_img = ImageOps.expand(stop_img, border=(10, 0, 10, 0))


    self.play_imgtk = ImageTk.PhotoImage(play_img)
    self.pause_imgtk = ImageTk.PhotoImage(pause_img)
    self.unpause_imgtk = ImageTk.PhotoImage(unpause_img)
    self.stop_imgtk = ImageTk.PhotoImage(stop_img)


    trackframe = LabelFrame(self.root,text="Song Track",font=("arial",15,"bold"),bg="#8F00FF",fg="white",bd=5,relief=GROOVE)
    trackframe.place(x=0,y=0,width=600,height=100)
    songtrack = Label(trackframe,textvariable=self.track,width=20,font=("arial",24,"bold"),bg="#8F00FF",fg="#B0FC38").grid(row=0,column=0,padx=10,pady=5)
    trackstatus = Label(trackframe,textvariable=self.status,font=("arial",24,"bold"),bg="#8F00FF",fg="#B0FC38").grid(row=0,column=1,padx=10,pady=5)

  
    buttonframe = LabelFrame(self.root,text="Control Panel",font=("arial",15,"bold"),bg="#8F00FF",fg="white",bd=5,relief=GROOVE)
    buttonframe.place(x=0,y=100,width=600,height=100)

    # Agrega el control de volumen en el marco de botones
    volume_frame = LabelFrame(buttonframe, text="Volume", font=("arial", 7, "bold"), bg="#8F00FF", fg="white", bd=1, relief=GROOVE)
    volume_frame.grid(row=0, column=4, padx=0, pady=0)
    self.volume_scale = Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, resolution=0.01, bg="#8F00FF", fg="#B0FC38", command=self.set_volume)
    self.volume_scale.set(0.5)  
    self.volume_scale.pack()


    # Boton de play
    playbtn = ttk.Button(buttonframe,image=self.play_imgtk ,command=self.playsong, style='RoundedButton.TButton' )
    playbtn.grid(row=0,column=0,padx=10,pady=5)

    # Boton de pausa
    playbtn = ttk.Button(buttonframe,image=self.pause_imgtk  ,command=self.pausesong,style='RoundedButton.TButton')
    playbtn.grid(row=0,column=1,padx=10,pady=5)

    # Boton de despausa
    playbtn = ttk.Button(buttonframe,image=self.unpause_imgtk ,command=self.unpausesong, style='RoundedButton.TButton')
    playbtn.grid(row=0,column=2,padx=10,pady=5)

    #boton de pausa
    playbtn = ttk.Button(buttonframe, image=self.pause_imgtk,command=self.stopsong,style="RoundedButton.TButton")
    playbtn.grid(row=0,column=3,padx=10,pady=5)
#    backbtn = Button(buttonframe,text="BACK",command=self.back_folder,width=6,height=1,font=("arial",16,"bold"),fg="white",bg="#B0FC38").grid(row=0,column=4,padx=10,pady=5)
    

    songsframe = LabelFrame(self.root,text="Song Playlist",font=("arial",15,"bold"),bg="#8F00FF",fg="white",bd=5,relief=GROOVE)
    songsframe.place(x=600,y=0,width=385,height=200)
    scroll_y = Scrollbar(songsframe,orient=VERTICAL)
    self.playlist = Listbox(songsframe,yscrollcommand=scroll_y.set,selectbackground="#B0FC38",selectmode=SINGLE,font=("arial",12,"bold"),bg="#CF9FFF",fg="navyblue",bd=5,relief=GROOVE)
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_y.config(command=self.playlist.yview)
    self.playlist.pack(fill=BOTH)
    os.chdir(home)
    songtracks = os.listdir()

    # for track in songtrack:
    #     if not track.startswith('.')
    
    for track in songtracks:
        ext = os.path.splitext(track)[1].lower()
        if ext not in disallowed_extensions:
            self.playlist.insert(END, track)
    
    for track in songtracks:
        if os.path.isdir(track):
           continue           
        ext = os.path.splitext(track)[1]
        # if ext in allowed_extensions or ext[1:] in allowed_extensions:
        #     self.playlist.insert(END, track)
        if not track.startswith('.'):
          self.playlist.insert(END,track)
        self.playlist.bind("<Double-Button-1>", self.open_folder)

    for track in songtracks:
      if not track.startswith('.'):
        self.playlist.insert(END,track)
    self.playlist.bind("<Double-Button-1>", self.open_folder)
  


  def playsong(self):
    self.track.set(self.playlist.get(ACTIVE))
    self.status.set("-Playing")
    pygame.mixer.music.load(self.playlist.get(ACTIVE))
    pygame.mixer.music.play()

     # Actualiza la información de la canción
    self.update_song_info(self.playlist.get(ACTIVE))
  

  def update_song_info(self, song_file):
      audio_file = eyed3.load(song_file)

      # Actualiza el autor
      if audio_file.tag.artist:
          self.author_label.config(text="Autor: " + audio_file.tag.artist)
      else:
          self.author_label.config(text="Autor: sin autor")

        # Actualiza la portada del álbum
      if audio_file.tag.images:
          album_art_data = audio_file.tag.images[0].image_data
          album_art_image = Image.open(io.BytesIO(album_art_data))
          album_art_image = album_art_image.resize((300, 300), Image.ANTIALIAS)
          album_art_photo = ImageTk.PhotoImage(album_art_image)
      else:
         # Cambiar 'path/to/default/image.jpg' al path de tu imagen predeterminada
          default_image_path = 'path/to/default/image.jpg'
          default_image = Image.open(default_image_path)
          default_image = default_image.resize((300, 300), Image.ANTIALIAS)
          album_art_photo = ImageTk.PhotoImage(default_image)

      self.album_art.config(image=album_art_photo)
      self.album_art.image = album_art_photo

  def set_volume(self, volume_level):
        pygame.mixer.music.set_volume(float(volume_level))

 
  def open_folder(self, event):
        selected_song = self.playlist.get(self.playlist.curselection())
        if os.path.isdir(selected_song):
            os.chdir(selected_song)
            self.playlist.delete(0, END)
    
            self.playlist.insert(END, "..")
            songtracks = os.listdir()
            for track in songtracks:
                self.playlist.insert(END, track)
            songtracks = os.listdir()
            for track in songtracks:
                if is_audio_file(track) or os.path.isdir(track):
                    if not track.startswith('.'):  # Ignorar carpetas ocultas
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
