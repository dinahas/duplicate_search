from __future__ import division
from PIL import Image

import os
import subprocess
import cv2

def main():
    for video in os.listdir(dir_main):
        if '.mp4' in video:
            os.makedirs("pict", exist_ok=True)
            subprocess.call(['ffmpeg', '-i', video, '-vf', 'select=gt(scene\,0.3)', '-vsync', '0', '-an', '-frame_pts', '1', 
                     'C:/Users/user/Desktop/NIR/pict/%d.jpg'])
            search_similar(video, subdir, dir_main)
            os.rename(dir_main + video, subdir + video)
            os.rename(subdir, dir_main + os.path.splitext(video)[0])

def search_similar(video, subdir, dir_main):
    fps_curr = cv2.VideoCapture(video).get(cv2.CAP_PROP_FPS)
    fps = 1
    name = ''

    for filename in os.listdir(subdir):
        if '.jpg' in filename:
            for r, d, f in os.walk(dir_main):
                if r not in subdir:
                    for file in f:
                        if '.mp4' in file:
                            name = file
                            fps = cv2.VideoCapture(r + '/' + file).get(cv2.CAP_PROP_FPS)
                    for file in f:
                        if '.jpg' in file:
                            if is_look_alike(subdir + filename, r + '/' + file, tolerance = 9):
                                logs = open(subdir + "logs.txt","a+")
                                logs.write("Схожее видео: %d минута %d секунда и %d минута %d секунда (%s)\n" 
                                           %(int(os.path.splitext(filename)[0]) // fps_curr // 60, int(os.path.splitext(filename)[0]) // fps_curr % 60,
                                            int(os.path.splitext(file)[0]) // fps // 60, int(os.path.splitext(file)[0]) //fps % 60, name))
                                logs.close()
                            
def delete_dir(folder):
    for file in os.listdir(subdir):
        file_path = os.path.join(subdir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def hash_distance(left_hash, right_hash):
    """Compute the hamming distance between two hashes"""
    if len(left_hash) != len(right_hash):
        raise ValueError('Hamming distance requires two strings of equal length')

    return sum(map(lambda x: 0 if x[0] == x[1] else 1, zip(left_hash, right_hash)))

def hashes_are_similar(left_hash, right_hash, tolerance=6):
    """
    Return True if the hamming distance between
    the image hashes are less than the given tolerance.
    """
    return hash_distance(left_hash, right_hash) <= tolerance

def average_hash(image_path, hash_size=8):
    """ Compute the average hash of the given image. """
    with open(image_path, 'rb') as f:
        # Open the image, resize it and convert it to black & white.
        image = Image.open(f).resize((hash_size, hash_size), Image.ANTIALIAS).convert('L')
        pixels = list(image.getdata())

    avg = sum(pixels) / len(pixels)

    # Compute the hash based on each pixels value compared to the average.
    bits = "".join(map(lambda pixel: '1' if pixel > avg else '0', pixels))
    hashformat = "0{hashlength}x".format(hashlength=hash_size ** 2 // 4)
    return int(bits, 2).__format__(hashformat)

def distance(image_path, other_image_path):
    """ Compute the hamming distance between two images"""
    image_hash = average_hash(image_path)
    other_image_hash = average_hash(other_image_path)

    return hash_distance(image_hash, other_image_hash)

def is_look_alike(image_path, other_image_path, tolerance=6):
    image_hash = average_hash(image_path)
    other_image_hash = average_hash(other_image_path)

    return hashes_are_similar(image_hash, other_image_hash, tolerance)
	

print('Введите путь к файлам')
dir_main = input() #'C:/Users/user/Desktop/NIR'
subdir = dir_main + 'pict/'
main()



