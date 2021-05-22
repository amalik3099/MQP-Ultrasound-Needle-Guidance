#!/usr/bin/env python

import argparse
import os.path
import pylisten
from PIL import Image
import sys

## called when a new processed image is streamed
# @param image the scan-converted image data
# @param width width of the image in pixels
# @param height height of the image in pixels
# @param bpp bits per pixel
# @param micronsPerPixel microns per pixel
# @param timestamp the image timestamp in nanoseconds
def newProcessedImage(image, width, height, bpp, micronsPerPixel, timestamp, imu):
    print("aa")
    # print("new image (sc): {0}, {1}x{2} @ {3} bpp, {4:.2f} um/px, imu: {5} pts".format(timestamp, width, height, bpp, micronsPerPixel, len(imu)))
    if bpp == 32:
        img = Image.frombytes('RGBA', (width, height), image)
    else:
        img = Image.frombytes('L', (width, height), image)
    for i in imu:
        print(i.ax, i.ay, i.az, i.gx, i.gy, i.gz, i.mx, i.my, i.mz, i.qw, i.qx, i.qy, i.qz)

    
    # img.save(f"processed_image_{timestamp}.png")
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
    print(help(pylisten))

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
