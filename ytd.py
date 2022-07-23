"""
Author:Muwanguzi Joseph
Project:Youtube Downloader
Description:
"""
from pytube import YouTube,Search
from pytube.exceptions import RegexMatchError,VideoUnavailable
from urllib.error import URLError
from clipboard import paste
from win10toast  import ToastNotifier
# from progress.bar import ShadyBar
# from progress.spinner import Spinner
import os
import math

class SearchVideo:
    pass
class YoutubeVideo:
    def __init__(self) :
        commands=["cls","color 9"]
        video_link = paste()
        url = ""
        self.toast = ToastNotifier()
        
        
        for c in commands:
            os.system(c)
            
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
    
    def _get_video_duration(self):
        time = self.yt.length
        hr = "" if time//3600 == 0 else str(time//3600)+":" #don't display hour if is 0
        min_ = math.floor((time%3600)/60)
        sec=time%60
        duration = f"{hr}{min_}:{sec}"
        return duration
     
        
    def video_info(self):
        video = self.get_video()
        video_size = math.floor(video.filesize/1049600)
        title= video.title
        description = self.yt.description
        
        info_dict={"title":title,
                   "size":video_size,
                   "duration":self._get_video_duration(),
                   "description":description,
                   "thumbnail": self.yt.thumbnail_url,
                   }
        
        return  info_dict
    
    def download_complete(self):
         """
         notify when download is complete
         """    
         self.toast.show_toast("Audio download","Download complete",duration=60)
                   
    def download_video(self):
        print("downloading video----")
        video=self.get_video()
        directory = self.download_directory("videos")
        video.download(max_retries=30,output_path=directory)
        self.download_complete()
       
    def download_audio(self):
        """
         get audio formats from the youtube video downloads
        """
        print("downloading audio ---")
        
        audio= self.yt.streams.get_audio_only()
        directory = self.download_directory("audio")
        audio.download(max_retries=3,output_path=directory)
        
        os.chdir(directory)  # directory where the downloaded is located
        self.rename_to_mp3(audio)
        self.download_complete()
    
        
    def rename_to_mp3(self,file):
        """
        Replaces mp4 video extension on the downloaded audio file to mp3.
        Removes undesired naming on the video like "official video "

        Args:
            file (str): Audio file to be renamed
        """
    
        new_audio_name = file.default_filename.removesuffix('.mp4')+".mp3"
        
        patterns_to_omit=("official","(",")","lyrics","video")
        
        #check for patterns to omit from the file name
        for p in new_audio_name.lower().split():
            if p in patterns_to_omit:
                print("pat ",p)                                
                new_audio_name=new_audio_name.replace(p,"")
        
        try:
            # rename download when complete
            os.rename(file.default_filename,new_audio_name)
        except FileExistsError:
            print(f"File name {new_audio_name} already exists")
        
                 
    def download_directory(self,sub_folder=None):
        """
        if directory doesn't exit creates  it to the current folder,
        where downloaded file is stored
        Returns:
            str: directory
        """
        BASE_DIR =os.environ.get("HOMEPATH")
        
        path=f'{BASE_DIR}\Desktop\downloads'
        directory=os.path.join(path,"YTDownloader")
        if sub_folder:
            directory+=f"\{sub_folder}"

        if not os.path.exists(directory):
            os.makedirs(directory)  
             
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
    print(" Note:This script automatically  gets the copied url\n Make sure to copy link before starting\n")
    print(" Collecting video information ------")
    print(yt.video_info())
    

    
    while True:
           choice = input(' Enter "V" to download video or \n"A" for audio or any other key to Quit >> ').upper()
           print()
           if choice == "V":
               yt.download_video()
           elif choice == "A":
               yt.download_audio()
           else:
              break
    
    print(" PROGRAM EXITED")
    

except (
        VideoUnavailable,RegexMatchError,URLError
        ):
    print("""
            ERROR- Something is wrong
                  
                Possible causes
                     >Invalid video url copied
                     >Poor internet connection
                     >Video may be not available
          """)
