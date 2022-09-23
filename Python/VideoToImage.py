from DuplicateRemover import Duplicates
import cv2
from glob import glob


def collect(video_path):
    video = cv2.VideoCapture(video_path)
    take_from_second = 2  # сколько кадров брать из одной секунды
    fps = int(round(video.get(cv2.CAP_PROP_FPS), 0)) / take_from_second
    # frame_count = int(round(video.get(cv2.CAP_PROP_FRAME_COUNT), 0))
    # print(fps, frame_count)
    count = 0
    success = True
    frames = []

    while success:
        success, image = video.read()
        if not success:
            break
        # print('read a new frame:',success)
        if count % fps == 0:
            name = video_path.replace('.mp4', '') + str(count+1).zfill(8) + '.png'
            frames.append(name)
            cv2.imwrite(name, image)
        count += 1

    return frames


folders = ['../edited/Нормальная слизистая желудка/', '../edited/Застойное содержимое/']
for folder in folders:
    videos = glob(folder + '*.mp4')
    for video in videos:
        frames = collect(video)
        print(folder + ' :', Duplicates(frames))
