#!/usr/bin/env python

import argparse
import os.path
import pylisten
from PIL import Image
import sys
import numpy as np
import pandas as pd

start = 0.0 
flag = 0
previous_time = 1e-10
## called when a new processed image is streamed
# @param image the scan-converted image data
# @param width width of the image in pixels
# @param height height of the image in pixels
# @param bpp bits per pixel
# @param micronsPerPixel microns per pixel
# @param timestamp the image timestamp in nanoseconds

def imu_data_processing(imu,imu_len):

    imu_data = np.empty(14, dtype=float)
    for i in imu:
        # print(i.ax, i.ay, i.az, i.gx, i.gy, i.gz, i.mx, i.my, i.mz, i.qw, i.qx, i.qy, i.qz)
        imu_data[0] += i.ax
        imu_data[1] += i.ay
        imu_data[2] += i.az
        imu_data[3] += i.gx
        imu_data[4] += i.gy
        imu_data[5] += i.gz
        imu_data[6] += i.mx
        imu_data[7] += i.my
        imu_data[8] += i.mz
        imu_data[9] += i.qw
        imu_data[10] += i.qx
        imu_data[11] += i.qy
        imu_data[12] += i.qz
        imu_data[13] += (i.tm/1e+9)

   
    imu_data = (imu_data/imu_len) 

    # print(imu_data)
    return imu_data

def write_to_csv(imu,time_frame,previous_time):
    global flag
    path = "/home/amalik/Documents/listener/src/python/IMU_data/imu_data.csv"

    frame_data = pd.DataFrame({'acc_x': [imu[0]],'acc_y': [imu[1]],'acc_z': [imu[2]],
                                'gyro_x': [imu[3]],'gyro_y': [imu[4]],'gyro_z': [imu[5]],
                                'mag_x': [imu[6]],'mag_y': [imu[7]],'mag_z': [imu[8]],
                                'quaternion_w': [imu[9]],'quaternion_x': [imu[10]],'quaternion_y': [imu[11]],'quaternion_z': [imu[12]],
                                'rate':[(1/(time_frame-previous_time))],'time':[time_frame]})
    
    # print(imu)
    
    if(not flag):
        frame_data.to_csv(path, mode='a', index=False, header=True)
        flag = 1 
    else:
        frame_data.to_csv(path, mode='a', index=False, header=False)
    


def newProcessedImage(image, width, height, bpp, micronsPerPixel, timestamp, imu):
    print("new image (sc): {0}, {1}x{2} @ {3} bpp, {4:.2f} um/px, imu: {5} pts".format(timestamp, width, height, bpp, micronsPerPixel, len(imu)))
    global start
    global positional_data
    global previous_time
     
    if(start == 0.0):
        start = np.round_((timestamp/1e+9), decimals = 3)

    # img = Image.frombytes('L', (width, height), image)
    if bpp == 32:
        img = Image.frombytes('RGBA', (width, height), image)
    else:
        img = Image.frombytes('L', (width, height), image)

    time_frame = abs(np.round_((timestamp/1e+9 - start), decimals = 3))
    
    # /********************************************
    # for raw imu data:
    imu_data = imu_data_processing(imu, len(imu))
    
    write_to_csv(imu_data,time_frame,previous_time)
    
    # ********************************************/
    previous_time = time_frame
    # /********************************************
    # for positional data:
    # position_data = positional_data_processing(imu_data)
    # write_to_csv(position_data,time_frame)
    # ********************************************/
    
    path_img = "/home/amalik/Documents/listener/src/python/slice_data/" + f"{time_frame}.png"
    img.save(path_img)

    return


## called when a new raw image is streamed
# @param image the raw pre scan-converted image data, uncompressed 8-bit or jpeg compressed
# @param lines number of lines in the data
# @param samples number of samples in the data
# @param bps bits per sample
# @param axial microns per sample
# @param lateral microns per line
# @param timestamp the image timestamp in nanoseconds
# @param jpg jpeg compression size if the data is in jpeg format
def newRawImage(image, lines, samples, bps, axial, lateral, timestamp, jpg):
    print("new image (ps): {0}, {1}x{2} @ {3} bps, {4:.2f} um/s, {5:.2f} um/l".format(timestamp, lines, samples, bps, axial, lateral))
    if jpg == 0:
        img = Image.frombytes('L', (samples, lines), image, "raw")
    else:
        # note! this probably won't work unless a proper decoder is written
        img = Image.frombytes('L', (samples, lines), image, "jpg")
    img.save("raw_image.jpg")
    return

## called when freeze state changes
# @param frozen the freeze state
def freezeFn(frozen):
    if frozen:
        print("imaging frozen")
    else:
        print("imaging running")
    return

## called when a button is pressed
# @param button the button that was pressed
# @param clicks number of clicks performed
def buttonsFn(button, clicks):
    print("button pressed: {0}, clicks: {1}".format(button, clicks))
    return

## main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', '-a', dest='ip', help='ip address of probe.', required=True)
    parser.add_argument('--port', '-p', dest='port', type=int, help='port of the probe', required=True)
    parser.add_argument('--width', '-w', dest='width', type=int, help='image output width in pixels')
    parser.add_argument('--height', '-ht', dest='height', type=int, help='image output height in pixels')
    parser.set_defaults(ip=None)
    parser.set_defaults(port=None)
    parser.set_defaults(width=640)
    parser.set_defaults(height=480)
    args = parser.parse_args()

    # uncomment to get documentation for pylisten module
    # print(help(pylisten))
    if not args.ip or not args.port or args.port < 0:
        print("one or more arguments are invalid")
        parser.print_usage()
        return
    
    # get home path
    path = os.path.expanduser("~/")

    # initialize
    listen = pylisten.Listener(newProcessedImage, newRawImage, freezeFn, buttonsFn)
    ret = listen.init(path, args.width, args.height)
    if ret:
        print("initialization succeeded")
        ret = listen.connect(args.ip, args.port)
        if ret:
            print("connected to {0} on port {1}".format(args.ip, args.port))
        else:
            print("connection failed")
            listen.destroy()
            return
    else:
        print("initialization failed")
        return
  
    # input loop
    key = ''
    while key != 'q' and key != 'Q':
        key = input("press ('q' to quit) ('a' for action): ")
        if key == 'a' or key == 'A':
            key = input("(f)->freeze, (i)->image, (c)->cine, (d/D)->depth, (g/G)->gain: ")
            if key == 'f' or key == 'F':
                listen.userFunction(1)
            elif key == 'i' or key == 'I':
                listen.userFunction(2)
            elif key == 'c' or key == 'C':
                listen.userFunction(3)
            elif key == 'd':
                listen.userFunction(4)
            elif key == 'D':
                listen.userFunction(5)
            elif key == 'g':
                listen.userFunction(6)
            elif key == 'G':
                listen.userFunction(7)

    listen.destroy()

if __name__ == '__main__':
    main()
