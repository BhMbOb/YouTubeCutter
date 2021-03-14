import os
import sys
import json
import time
from multiprocessing import Pool, Process, Queue, freeze_support
from collections import OrderedDict

import moviepy
import moviepy.editor
import pytube
from pydub import AudioSegment
import imageio_ffmpeg
from mutagen.easyid3 import EasyID3


def cut_mp3_wrapper(args):
    return cut_mp3(*args)


def cut_mp3(mp3, output_path, start, end, artist, album, song_number):
    extract = mp3[start:end]
    extract.export(output_path, format="mp3")
    audio =EasyID3(output_path)
    audio["artist"] = artist
    audio["album"] = album
    audio["tracknumber"] = str(song_number)
    audio.save()
    print("Complete: " + os.path.basename(output_path))


class YoutubeStripper(object):
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.realpath(__file__))
        self.output_dir = os.path.join(self.root_dir, "downloads")
        self.output_cache_dir = os.path.join(self.output_dir, ".cache")
        self.ffmpeg_exe_path = imageio_ffmpeg._utils.get_ffmpeg_exe()

    def run(self):
        """Download and process the album"""
        with open(os.path.join(self.root_dir, "album_data.json"), "r") as f:
            json_data = json.load(f, object_pairs_hook=OrderedDict)
        
        songs = OrderedDict(json_data["songs"])
        metadata = json_data["metadata"]

        youtube = pytube.YouTube(metadata["youtube_url"])
        video = youtube.streams.get_highest_resolution()

        mp4_download_cache_path = video.download(self.output_cache_dir)
        mp3_download_cache_path = mp4_download_cache_path.replace(".mp4", ".mp3")
        name = os.path.basename(mp4_download_cache_path).split(".")[0]

        mp3_output_dir = os.path.join(self.output_dir, name)
        os.makedirs(mp3_output_dir)
        video = moviepy.editor.VideoFileClip(mp4_download_cache_path)
        video.audio.write_audiofile(mp3_download_cache_path)
        song = AudioSegment.from_mp3(mp3_download_cache_path)

        pool_data = []

        for i in range(len(list(songs))):
            key = list(songs)[i]
            value = songs[key]

            start_min = int(value)
            start_sec = int(str(value).split(".")[1])
            start_time = start_min * 60 * 1000 + start_sec * 1000

            if(key == list(songs)[-1]):
                end_time = len(song)
            else:
                next_ = list(songs)[i + 1]
                end_min = int(songs[next_])
                end_sec = int(str(songs[next_]).split(".")[1])
                end_time = end_min * 60 * 1000 + end_sec * 1000

            path = os.path.join(mp3_output_dir, key + ".mp3")

            pool_data.append((
                song,
                path,
                start_time,
                end_time,
                metadata["artist"],
                metadata["album"],
                i + 1
                ))
            print("Began conversion of: " + key)

        pool = Pool(os.cpu_count())
        pool.map(cut_mp3_wrapper, pool_data)


if __name__ == "__main__":
    inst = YoutubeStripper()
    inst.run()
    print("Conversion Complete - you can now close this window")
