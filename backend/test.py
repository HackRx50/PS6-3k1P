import subprocess
from functions import *

# Paths to files
input_file = "vids/opd_tax_Gain_new_ver1.mp4"
subtitle_file = "tmp/subtitles.srt"
output_file = "vids/output_with_subtitles.mp4"

add_subtitle(input_file, subtitle_file, output_file)
