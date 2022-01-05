# __main__.py

import cv2
import numpy as np
import glob
import tqdm
import importlib
import pathlib
import shutil
import os
import subprocess
import time
import torch.multiprocessing as mp
import torch
import dsfd
import dsfd.face_detection
import utils
import argparse

def main():
		pass



def detect_face_multiprocessing(worker_i):
		
		torch.set_num_threads(1)
		# initialize the process group
		# torch.distributed.init_process_group("gloo", rank=worker_i, world_size=mp.cpu_count())
		print(f"worker #{worker_i} spawned")
		# worker_i - current worker
		file_name = "../test57.mp4"
		cap = cv2.VideoCapture(file_name)
		width, height = (
						int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
						int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		)
		frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		fps = int(cap.get(cv2.CAP_PROP_FPS))
		# num_workers = mp.cpu_count()
		num_workers = 12
		print(f"frame_count:  {frame_count}")
		print(f"num_workers:  {num_workers}")
		frame_jump_unit =  frame_count // num_workers
		print(f"frame_jump_unit:   {frame_jump_unit}")
		cap.set(cv2.CAP_PROP_POS_FRAMES, frame_jump_unit * worker_i)
		
		
		# Define the codec and create VideoWriter object
		fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
		out = cv2.VideoWriter()
		out.open("output_{}.mp4".format(worker_i), fourcc, fps, (width, height), True)
		
		i = 0
		#  device=torch.device("cpu"), 
		# dsfd = importlib.import_module("DSFD-Pytorch-Inference")
		# print(dsfd)
		print("before detector")
		detector = dsfd.face_detection.build_detector("RetinaNetMobileNetV1", device=torch.device("cpu"), confidence_threshold=.5, nms_iou_threshold=.3)
		print(f"detector:    {detector}")
		print("after detector")
		rectangles = []
		
		try:
				print("inside try")
				print(f"i: {i}")
				print(f"frame_jump_unit:  {frame_jump_unit}")
				while i < frame_jump_unit:
						print(f"i= {i}")
						ret, frame = cap.read()
						if not ret:
						 		break

						im = frame
						#  Perform face detection on each frame
						detections = detector.detect(im[:, :, ::-1])
						rectangles.append(detections)
						for face in detections:
						 		(x1, y1, x2, y2, _) = np.rint(face)
						 		print("(x1, y1, x2, y2, _) = ( {}, {}, {}, {})".format(x1,y1,x2,y2))
						 		color = (255, 0, 0)
						 		cv2.rectangle(im, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
						
						# write the frame
						out.write(im)
						i += 1
		except:
				# Release resources
				cap.release()
				out.release()

		# Release resources
		cap.release()
		out.release()


if __name__ == '__main__':
		torch.multiprocessing.set_start_method('spawn', force=True)
		
		file_name = "../test57.mp4"
		output_file_name = "test57_result.mp4"
		width, height, frame_count, fps = get_video_frame_details(file_name)
		print(f"Video frame count = {frame_count}")
		print(f"Width = {width}, Height = {height}, FPS = {fps}")
		num_workers = 12 
		print("Number of CPU: " + str(num_workers))
		frame_jump_unit =  frame_count // (num_workers)
		print(f"frame_jump_unit:		{frame_jump_unit}")
		frame_jump_unit =  frame_count // num_workers
		print(f"Total number of workers:	{num_workers}")
		start_time = time.time()
		
		# Paralle the execution of a function across multiple input values
		with mp.Pool(processes=num_workers) as p:
				print(p)
				p.map(detect_face_multiprocessing, range(num_workers))
				# p.join()
		

		combine_output_files(num_workers, output_file_name)

		end_time = time.time()

		total_processing_time = end_time - start_time
		inf_fps = frame_count/total_processing_time
		print(f"Time taken: {total_processing_time}")
		print(f"Inference FPS : {inf_fps}")
