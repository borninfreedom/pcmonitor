import cv2
from datetime import datetime
import os
import time
import threading
import glob
import logging
from config import image_period, fast_image_period, img_width, img_height, video_fps
from utils import same_similarity
import atexit
import signal
from termcolor import colored


LOG_LEVEL = logging.DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
fh = logging.FileHandler('main.log')
fh.setLevel(LOG_LEVEL)
logger.addHandler(ch)
logger.addHandler(fh)


class Monitor:

    def __init__(self, image_period=image_period, fast_image_period=fast_image_period, video_fps=video_fps,
                 img_width=img_width, img_height=img_height, with_logger=False):
        self.launch_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.img_path = self.launch_time
        self.video_path = 'videos'
        self.with_logger = with_logger
        self.create_folders()

        video_path = os.path.join('videos', f'{self.launch_time}.avi')
        self.video_maker = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), video_fps,
                                           (img_width, img_height))
        atexit.register(self.cap2video)

    def create_folders(self):
        if not os.path.exists(self.img_path):
            os.makedirs(self.img_path)
        if not os.path.exists(self.video_path):
            os.mkdir(self.video_path)

    def capture(self):
        cap = cv2.VideoCapture(0)
        ret, frame_pre = cap.read()
        index = 0
        img_name = os.path.join(self.img_path, f'{index}.jpg')
        cv2.imwrite(img_name, frame_pre)

        while ret:
            ret, frame = cap.read()

            ss = same_similarity(frame_pre, frame)
            if self.with_logger:
                logger.debug(f'frame{ss=}')
            if ss > 0.84:
                time.sleep(image_period)
                continue
            else:
                index += 1
                img_name = os.path.join(self.img_path, f'{index}.jpg')
                cv2.imwrite(img_name, frame)
                time.sleep(fast_image_period)
            frame_pre = frame

    # if you encounter ctrl c error, run pip install -U scipy scikit-image
    # link https://programmerah.com/solved-forrtl-error-200-program-aborting-due-to-control-c-event-41009/
    # link https://stackoverflow.com/questions/15457786/ctrl-c-crashes-python-after-importing-scipy-stats
    def cap2video(self):
        print(colored('Making the captures to a video, please wait a minute.','red'), flush=True)
        i = 0
        while True:
            img = cv2.imread(os.path.join(self.img_path, f'{i}.jpg'))
            if img is None:
                break
            self.video_maker.write(img)
            i += 1
        print(colored('Done, the video is in the videos directory.','green'),flush=True)


if __name__ == '__main__':
    mon = Monitor()
    mon.capture()
