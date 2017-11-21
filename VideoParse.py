import os
import sys
import imageio
from PIL import Image

interval = 10
frame_size = (128,128)

video_dir = sys.argv[1]
image_dir = sys.argv[2]
if not os.path.exists(image_dir):
	os.makedirs(image_dir)

video = imageio.get_reader(video_dir, 'ffmpeg')
fps = int(video.get_meta_data()['fps'])
frame_cnt = int(video.get_meta_data()['nframes'])

for frame in range(0, frame_cnt, interval*fps):
	image = video.get_data(frame)
	image = Image.fromarray(image)
	image = image.resize(frame_size)
	image.save(os.path.join(image_dir, str(frame).zfill(8) + '.jpg'), 'JPEG')

