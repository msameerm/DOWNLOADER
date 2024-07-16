import os
import json
import yt_dlp
import subprocess
from colorama import Fore, Style, init
import time
import sys

# Initialize colorama
init(autoreset=True)

logo = f"""
{Fore.GREEN} #####                                     
{Fore.GREEN}#     #   ##   #    # ###### ###### #####  
{Fore.GREEN}#        #  #  ##  ## #      #      #    # 
{Fore.BLUE} #####  #    # # ## # #####  #####  #    # 
{Fore.BLUE}      # ###### #    # #      #      #####  
{Fore.BLUE}#     # #    # #    # #      #      #   #  
{Fore.BLUE} #####  #    # #    # ###### ###### #    # 
                                           
"""

def print_logo():
    print(logo)

def get_youtube_shorts(channel_url):
    # Command to list all shorts from the YouTube channel
    command_list = [
        'yt-dlp',
        '--flat-playlist',
        '-j',
        f'{channel_url}/shorts'
    ]
    
    result = subprocess.run(command_list, capture_output=True, text=True)
    video_data = result.stdout.strip().split('\n')

    video_urls = []
    for video_json in video_data:
        if video_json:
            video_info = json.loads(video_json)
            video_urls.append(video_info['url'])
    
    return video_urls

def download_videos(video_urls):
    total_videos = len(video_urls)
    for index, video_url in enumerate(video_urls, start=1):
        video_id = ""
        percentage = ""
        
        def progress_hook(d):
            nonlocal video_id, percentage
            if d['status'] == 'downloading':
                percentage = d['_percent_str'].strip()
                video_id = d['info_dict']['id']
                sys.stdout.write(
                    f"\r{Fore.GREEN}[Downloading {Fore.GREEN}{index:02} {Fore.WHITE}out of {Fore.RED}{total_videos:02}] ✌️ {Fore.WHITE}({video_id}) ({percentage})"
                )
                sys.stdout.flush()
            elif d['status'] == 'finished':
                print(f"\n{Fore.GREEN}({d['info_dict']['id']}) downloaded")

        ydl_opts = {
            'progress_hooks': [progress_hook],
            'quiet': True,  # Suppress detailed logs
            'no_warnings': True,  # Suppress warnings
            'retries': 10,  # Number of retries
        }

        success = False
        while not success:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                    success = True
            except Exception as e:
                print(f"{Fore.RED}\nConnection error. Retrying in 10 seconds...")
                time.sleep(10)  # Wait before retrying

def main_menu():
    print_logo()
    print(f"{Fore.GREEN}1: Download YouTube Shorts")
    print(f"{Fore.RED}2: Exit Tool")

def main():
    while True:
        main_menu()
        choice = input("Select an option: ")

        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print_logo()
            channel_url = input(f"{Fore.CYAN}Enter YouTube channel URL: ")
            
            # Fetching videos
            print(f"{Fore.CYAN}Fetching shorts...")
            video_urls = get_youtube_shorts(channel_url)
            
            # Showing number of fetched videos
            num_videos = len(video_urls)
            print(f"{Fore.BLUE}[Total {num_videos} Videos]")
            
            if num_videos > 0:
                download_videos(video_urls)
                print(f"{Fore.GREEN}\nALL VIDEOS SUCCESSFULLY DOWNLOADED")
            else:
                print(f"{Fore.RED}No videos found.")
        elif choice == '2':
            print(f"{Fore.RED}Exiting tool.")
            break
        else:
            print(f"{Fore.RED}Invalid option. Please try again.")

if __name__ == "__main__":
    main()
