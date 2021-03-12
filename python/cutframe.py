#   Copyright [2021] [bluewhitep]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0~
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import cv2
from IPython.lib import backgroundjobs as bg
from IPython.display import clear_output as clear

import os
import sys
import getopt

VERSION = "0.1.0"
input_file = ""
output_path = "out"


def get_frame(video, mode="read", out_path=None,):
    cap = cv2.VideoCapture(video)
    frame_id = 1
    frame_list = []
    print("Run", end="")
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    while cap.isOpened():
        flag, frame = cap.read()
        if flag == False:
            break

        img_name = out_path + "/" + str(frame_id) + ".png"
        cv2.imwrite(img_name, frame)
        frame_id += 1
        print(".", end="", flush=True)

    cap.release()
    return frame_id


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h:v:i:o:', ['help', 'version', 'input=', 'output='])
    except getopt.GetoptError:
        print("Run \'cutframe.py -h or --help\' for more information.")
        sys.exit(2)

    if opts == []:
        if args == []:
            print("Please enter video path.")
            print("If you need help, run \'cutframe.py -h or --help\' for more information.")
            sys.exit(2)
        elif len(args) == 1:
            input_file = args[0]
        else:
            print("Parameter is too much.")
            print("Run \'cutframe.py -h or --help\' for more information.")
            sys.exit(2)
    else:
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print("The program for cut frame form video. The frame output to out directory.")
                print("Example:")
                print("  python3 cutframe.py -i mov/video.mp4")
                print("-v, --version                           Version.")
                print("-i, --input [video Path]                Input video path.")
                print("-o, --output [dorectory]                Output directory. [default: ./out]")
                sys.exit()
            elif opt in ('-v', '--version '):
                print("version ", VERSION)
                sys.exit()
            elif opt in ('-i', '--input'):
                input_file = arg
            elif opt in ('-o', '--output'):
                output_path = arg

    frame = get_frame(input_file, mode="file", out_path=output_path)

    if frame == 1:
        print("Can't read the video file.")
        sys.exit(2)
    else:
        print("Done!")
        print("OutPath: ", output_path)
        print("Total frame: ", frame)
