"""
Authour:Muwanguzi Joseph
Project:Youtube Downloader
"""
from pytube import YouTube
from pytube.exceptions import RegexMatchError,VideoUnavailable
from urllib.error import URLError
from clipboard import paste
from win10toast  import ToastNotifier
# from progress.bar import ShadyBar
# from progress.spinner import Spinner
import os
import math


class YoutubeVideo:
    def __init__(self) :
        commands=["cls","color 2"]
        for c in commands:
            os.system(c)
        video_link = paste()
        url = ""
        self.toast = ToastNotifier()
        
        if video_link.startswith("https:") and video_link != "":
            url = video_link
        self.yt = YouTube(url)      
    
    
    def get_video(self):
        """
        Gets video with the highest resolution
        Returns:
            stream with highest resolution
        """

        yt_video = self.yt.streams.get_highest_resolution()
        return yt_video
    
     
    def print_video(self):
        video = self.get_video()
        video_size = math.floor(video.filesize/1049600)
        border ="_"*100
        
        #video time info
        time = self.yt.length
        hr = "" if time//3600 == 0 else str(time//3600)+":" #don't display hour if is 0
        min_ = math.floor((time%3600)/60)
        sec=time%60
        
        print("  VIDEO INFORMATION")
        print(f"""  
                {border}
                    VIDEO NAME:  {video.title}
                {border}
                    DURATION:    {hr}{min_}:{sec}
                {border}  
                    BITRATE:     {video.bitrate}
                {border}
                    SIZE:         {video_size} MB
                {border}
                                                              DESCRIPTION
                                                              ____________
                   
                      {self.yt.description[:500].center(100)}  
              """)
        print()
                   
    def download_video(self):
        print("downloading video----")
        directory = self.download_directory()
        self.get_video().download(output_path=directory,max_retries=30)
        #display notification when download is complete
        self.toast.show_toast("Video download","Download complete",duration=60)
       
    def download_audio(self):
        """
         get audio format from the youtube video download and rename file afterwards
        """
        print("downloading audio ---")
        directory = self.download_directory()
        audio= self.yt.streams.get_audio_only()
        audio.download(output_path=directory)
        
        self.rename_to_mp3(audio)
        self.get_video().download(output_path=directory,max_retries=30)
        #display notification when download is complete
        self.toast.show_toast("Audio download","Download complete",duration=60)
    
        
    def rename_to_mp3(self,file):
        """
        Replaces mp4 video extension on the downloaded audio file to mp3.
        Removes undesired naming on the video like "official video "

        Args:
            file (str): Audio file to be renamed
        """
        
        #change to the directory where the download 
        os.curdir = self.download_directory()
        os.chdir(os.curdir)
        
        new_audio_name = file.default_filename.removesuffix('.mp4')+".mp3"
        
        patterns_to_omit=("official","(",")","lyrics","video")
        
        #check for perterns to omit from the file name
        for p in new_audio_name.lower().split():
            if p in patterns_to_omit:
                print("pat ",p)                                
                new_audio_name=new_audio_name.replace(p,"")
        
        try:
            #is rename download when complete
            os.rename(file.default_filename,new_audio_name)
        except FileExistsError:
            print(f"File name {new_audio_name} already exists")
        
                 
    def download_directory(self):
        """
        if directory doesn't exit creates  it to the current folder,
        where downloaded file is stored
        Returns:
            str: directory
        """
        
        directory=os.path.join(os.getcwd(),"YTDownloader")
        
        if not os.path.exists(directory):
            os.mkdir(directory)  
             
        return directory
    
    # def work_progress(self,style,message,state=""):
    #     work_state = "done"
    #     if style == "spin":
    #         spinner = Spinner(message)
    #         while work_state != state:
    #             spinner.next()
    #         spinner.finish()
        
    #     if style == "bar":
    #         with ShadyBar(message,max=100) as bar:
    #             for x in range(100):
    #                 bar.next()
        
    #     if style == "bar":
    #         with ShadyBar(message,max=100) as bar:
    #             for x in range(100):
    #                 bar.next()
              
try:
    yt = YoutubeVideo()
    print("                                     YOUTUBE DOWNLOADER")
    print()
    print(" Note:This script automatically  gets the coppied url\n Make sure to copy link before startng")
    print()
    print(" Collecting video infomation ------")
    yt.print_video()
    
    while True:
       try:
           choice = int(input(" Enter 1 to download video or 2 for audio: "))
           print()
          
           if choice == 1:
               yt.download_video()
           if choice == 2:
               yt.download_audio()
           else:
               print("Invalid command")
       except ValueError:
           print(" Only integer input is accepted")
    

except (RegexMatchError,
        TimeoutError,
        URLError,
        ConnectionResetError,
        VideoUnavailable,
        NameError):
    print("""
            ERROR- Something is wrong
                  
                Possible causes
                     >Invalid video url copied
                     >Poor internet connection
                     >Video may be not available
          """)
