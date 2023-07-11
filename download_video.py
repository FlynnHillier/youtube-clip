from pytube import YouTube

def downloadVideo(url,output_path):
    yt = YouTube(url=url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=output_path)