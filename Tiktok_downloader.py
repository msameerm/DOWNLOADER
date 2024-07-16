import os
import json
import yt_dlp
import subprocess
from colorama import Fore, Style, init
import time
import sys
import re

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

def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    max_length = 255 - len(".mp4.part")  # Account for the file extension
    return sanitized[:max_length]

def get_tiktok_videos(profile_url):
    # Command to list all videos from the TikTok profile
    command_list = [
        'yt-dlp',
        '--flat-playlist',
        '-j',
        profile_url
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
            'outtmpl': '%(title).100s_%(id)s.%(ext)s'  # Template for output filename, truncated title to 100 chars
        }

        success = False
        while not success:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                    success = True
            except Exception as e:
                print(f"{Fore.RED}\nConnection error or file name too long. Retrying in 10 seconds...")
                time.sleep(10)  # Wait before retrying

def main_menu():
    print_logo()
    print(f"{Fore.GREEN}1: Download TikTok Videos")
    print(f"{Fore.RED}2: Exit Tool")

def main():
    while True:
        main_menu()
        choice = input("Select an option: ")

        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print_logo()
            profile_url = input(f"{Fore.CYAN}Enter TikTok profile URL: ")
            
            # Fetching videos
            print(f"{Fore.CYAN}Fetching videos...")
            video_urls = get_tiktok_videos(profile_url)
            
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
