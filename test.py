import yt_dlp # pip install yt_dlp

def hook(d):
    if d['status'] == 'finished':
        filename = d['filename']
        print(filename) # Here you will see the PATH where was saved.

# ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': '%(title)s.%(ext)s', # You can change the PATH as you want
#         'download_archive': 'downloaded.txt',
#         'noplaylist': True,
#         'quiet': True,
#         'no_warnings': True,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'progress_hooks': [hook]
# }

ydl_opts = {
    # 'extract_flat': True,
    'skip_download':True,
    'ignoreerrors': True
}


def client(video_url, download=False):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
         return ydl.extract_info(video_url, download=download)




# url = 'https://www.youtube.com/watch?v=aAdaXsaQIvY&list=PLKZIpl8QZ9BCGCgsWmmV8B8hN7wCAN7uy'
url = 'https://www.youtube.com/watch?v=X707dBfCys0&list=PLGs0VKk2DiYxQBoqxy3mucGGGbr9O6jPs'

song_details = client(url, download=False) # get the json details about the song
print(song_details)
# formats = song_details['formats']
# print(f'Total: {len(formats)}')
# print(song_details['format_note'])
# print(song_details['audio_ext'])
# print(song_details['filesize'])