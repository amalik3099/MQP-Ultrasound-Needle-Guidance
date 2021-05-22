#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.image as matImg
import numpy as np
from PIL import Image
from natsort import natsorted, ns
import os, sys


def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)


def multi_slice_viewer(volume):
        remove_keymap_conflicts({'j', 'k'})
        fig, ax = plt.subplots()
        ax.volume = volume
        ax.index = 0
        ax.set_title('Ultrasound Slice Viewer')
        ax.set_xlabel('Image Number: 0')
        ax.imshow(volume[ax.index])
        fig.canvas.mpl_connect('key_press_event', process_key)


def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'j':
        previous_slice(ax)
    elif event.key == 'k':
        next_slice(ax)
    fig.canvas.draw()


def previous_slice(ax):
    # 'Go to previous slice'
    volume = ax.volume
    ax.index = (ax.index - 1)   # wrap around using %
    ax.images[0].set_array(volume[ax.index])
    ax.set_xlabel('Image Number: ' + str(ax.index))


def next_slice(ax):
    # 'Go to next slice'
    volume = ax.volume
    ax.index = (ax.index + 1)   # wrap around using %
    ax.images[0].set_array(volume[ax.index])
    ax.set_xlabel('Image Number: ' + str(ax.index))


def main():

    path = "/home/amalik/Documents/listener/src/python/slice_data/"

    list_files = os.listdir(path)  # looking for files in current directory
    list_files = natsorted(list_files) #sort list of images in order of timestamp

    img_list = []

    for filename in list_files:
        if filename.endswith('.png'):
            try:
                # img.verify()  # verify that it is, in fact an image
                img = matImg.imread(path + filename)
                img_list.append(img)
            except (IOError, SyntaxError) as e:
                print('Bad file:', filename)
                os.remove(path+filename)

    multi_slice_viewer(img_list) #run images with sliceviewer
    plt.show() #display viewer 
    

if __name__ == "__main__":
    main()