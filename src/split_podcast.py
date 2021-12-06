from pydub import AudioSegment
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import math

Tk().withdraw()
# Define read and write directories.
target_file =  askopenfilename(title="Select a target podcast .mp3 file...") # .replace('/', '\\')
write_directory = askdirectory(title="Select a directory to save output...")
# Load podcast file.
podcast_file = AudioSegment.from_mp3(target_file)
# Pydub operates in miliseconds. We want 1 minute intervals.
one_minute = 60 * 1000
total_length_of_audio = len(podcast_file)
number_of_output_segments = math.ceil(total_length_of_audio/one_minute)

class AudioSnippet:

    def __init__(self, audio_clip, number):
        self.audio_clip = audio_clip
        self.output_name = str(number) + '.mp3'

    def __repr__(self):
        return f"audio_clip: {self.output_name}, length (ms): {len(self)}"

    def __len__(self):
        return len(self.audio_clip)

    def save_self_to_disk(self, output_directory):
        self.audio_clip.export(output_directory + '/' + self.output_name, format="mp3")
        print(f"Wrote {self.output_name} to disk...")

# TODO: Deal with the edge case where it ends on a milisecond divisible by one minute.
snippet_starts = []
snippet_ends = []

for i in range(number_of_output_segments):
    snippet_starts.append(i * one_minute)
    snippet_ends.append((i + 1) * one_minute)

# The end value will overshoot, so we replace it with the last valid max value.
snippet_ends[-1] = total_length_of_audio - 1

# Create a sorted list which each podcast segment, starting from 1.
output_files = [AudioSnippet(podcast_file[start:end], num + 1) for num, (start, end) in enumerate(zip(snippet_starts, snippet_ends))]

for file in output_files:
    file.save_self_to_disk(write_directory)
print("Done.")
