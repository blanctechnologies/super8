import cv2
import subprocess
import argparse


def parse_args():
		"""Parses commandline arugments"""
		parser = argparse.ArgumentParser(prog='super8', description='super8 is an open-source toolset for video analysis')
		parser.add_argument('-i',
                    help='filename of video to process')
		parser.add_argument('--detect_face',
                    help='sum the integers (default: find the max)')
		parser.add_argument('--m',
                    help='add multiprocessing')
		parser.add_argument('--num_threads',
                    help='add multiprocessing')
		parser.add_argument('--vis',
                    help='sum the integers (default: find the max)')
		args = parser.parse_args()	
		

def add_detect_subparser(subparser):
		parser = subparsers.add_parser('detect', help='detect faces in the video')
		parser.add_argument('-i',
                    help='filename of video to process')
		parser.add_argument('--detect_face',
                    help='sum the integers (default: find the max)')
		parser.add_argument('--m',
                    help='add multiprocessing')
		parser.add_argument('--num_threads',
                    help='add multiprocessing')
		parser.add_argument('--vis',
                    help='sum the integers (default: find the max)')
		args = parser.parse_args()	


def get_video_frame_details(file_name):
    cap = cv2.VideoCapture(file_name)
    width, height = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    return width, height, frame_count, fps


def combine_output_files(num_workers, output_file_name):
    print("combinging output files...")
    # Create a list of output files and store the file names in a txt file
    list_of_output_files = ["output_{}.mp4".format(i) for i in range(num_workers)]
    with open("list_of_output_files.txt", "w") as f:
        for t in list_of_output_files:
            f.write("file {} \n".format(t))

    # use ffmpeg to combine the video output files
    ffmpeg_cmd = "ffmpeg -y -loglevel error -f concat -safe 0 -i list_of_output_files.txt -vcodec copy " + output_file_name
    subprocess.Popen(ffmpeg_cmd, shell=True).wait()

    # Remove the temperory output files
    for f in list_of_output_files:
        os.remove(f)
    os.remove("list_of_output_files.txt")
