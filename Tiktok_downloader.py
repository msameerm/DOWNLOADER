import os
import json
import yt_dlp
import subprocess

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
        print(f"Downloading Video {index:02} out of {total_videos:02}")

        def progress_hook(d):
            if d['status'] == 'downloading':
                percentage = d['_percent_str'].strip()
                video_id = d['info_dict']['id']
                print(f"Video Id({video_id}) {percentage} downloaded", end='\r')
            elif d['status'] == 'finished':
                print(f"\nVideo Id({d['info_dict']['id']}) downloaded")

        ydl_opts = {
            'progress_hooks': [progress_hook],
            'quiet': True,  # Suppress detailed logs
            'no_warnings': True,  # Suppress warnings
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

def main():
    profile_url = input("Enter TikTok profile URL: ")
    
    # Fetching videos
    print("Fetching videos...")
    video_urls = get_tiktok_videos(profile_url)
    
    # Showing number of fetched videos
    num_videos = len(video_urls)
    print(f"Number of videos fetched: {num_videos}")
    
    if num_videos > 0:
        print("Downloading videos...")
        download_videos(video_urls)
        print("\nDownload completed.")
    else:
        print("No videos found.")

if __name__ == "__main__":
    main()
