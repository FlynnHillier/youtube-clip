from pathlib import Path
import shutil
from datetime import datetime
import whisper
from pytube import YouTube
from pydub import AudioSegment
import moviepy.editor as mp

def cleanup(temp_path:str) -> None:
    shutil.rmtree(temp_path)


def transcribeYT(youtube:YouTube,output_path : str =""):
    audioStreams = youtube.streams.filter(type="video")
    if len(audioStreams) == 0:
        raise BaseException("no audio streams were found within provided Youtube instance.")

    #use first audio stream (maybe select more appropriate stream in future)
    targetStream = audioStreams.first()



    #temp store targetstream
    temp_path = "temp_path"
    if not Path(temp_path).exists():
        Path(temp_path).mkdir()

    targetAudioPath = targetStream.download(temp_path)

    # sound = AudioSegment.from_mp3(targetAudioPath)
    
    destination = str(Path(temp_path).joinpath("stream.wav"))
    mp.VideoFileClip(targetAudioPath).audio.write_audiofile(destination)
    # sound.export(destination,format="wav")
    

    modelVersion = "base.en"
    model = whisper.load_model(modelVersion)
    
    result = model.transcribe(destination)

    outFilePath = str(Path(output_path).joinpath(f"{youtube.title}_transcript.txt"))
    with open(outFilePath,"w",encoding="utf-8") as txt:
        txt.write(result["text"])
        txt.close()

    cleanup(temp_path)

    

