#!/usr/bin/env python3
"""
Video Roller Script
"""

__author__ = "Will Conry"
__version__ = "0.1.0"
__license__ = "MIT"

import cv2, argparse
import numpy as np

def main(args):

    vr = vroller(   args.input[0],
                    args.output[0], 
                    args.direction[0],
                    args.framerate[0], 
                    args.buffersize[0], 
                    args.outputformat[0], 
                    args.fullbufferonly,
                    args.preview )

    vr.roll_video()


class vroller:
    # Setup
    def __init__(self, input, output, direction, framerate, buffersize, outputformat, fullbufferonly, preview):

        self.direction = direction

        self.fullbufferonly = fullbufferonly
        self.preview = preview

        self.cap = cv2.VideoCapture(input)
    
        self.ret, self.frame = self.cap.read()

        self.height, self.width, self.layers = self.frame.shape

        if framerate == 0: fps = self.cap.get(cv2.CAP_PROP_FPS)
        else: fps = framerate
        
        if buffersize == 0:
            if direction == 'UP' or direction == 'Down':
                self.n = self.width
            else:
                self.n = self.height
        else:
            self.n = buffersize

        fourcc = cv2.VideoWriter_fourcc(*outputformat)
        self.out = cv2.VideoWriter(output,fourcc, fps, (self.width, self.height))

        self.vbuff = np.full((self.n, self.height, self.width, self.layers), np.uint8(0))
        self.fbuff = np.full((self.height, self.width, self.layers), np.uint8(0))

        self.fNo = 0 ; self.f0 = self.fNo % self.n

        print('Rendering video, press "Q" to cancel.')

    def roll_video(self):

        while(self.cap.isOpened()):
            if self.ret == True:

                self.vbuff[self.f0] = self.frame
                self.roll_chooser()
                self.save_show_increment()

                # Read next frame from input video
                self.ret, self.frame = self.cap.read()

                # Give the user a chance to cancel
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print('Canceling...')
                    break

            else:
                # Don't flush buffer if -fbo is used
                if self.fullbufferonly: break

                # Flush video buffer into output
                for _ in range(self.n):

                    self.vbuff[self.f0] = np.full((self.height, self.width, self.layers), np.uint8(0))
                    self.roll_chooser()
                    self.save_show_increment()

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print('Canceling...')
                        break

                break

        # Release
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

        print('Finished.')

    def roll_chooser(self):
        if self.direction == "DOWN":
            self.roll_down()
        elif self.direction == "UP":
            self.roll_up()
        elif self.direction == "LEFT":
            self.roll_left()
        elif self.direction == "RIGHT":
            self.roll_right()

    def roll_up(self):
        # Create the output frame by taking a slice of each frame from the buffer
        for div in range(self.n):
            start = int(div*self.height/self.n)
            end = int((div+1)*self.height/self.n)
            self.fbuff[start:end,:,:] = self.vbuff[(self.f0+div+1)%self.n,start:end,:,:]

    def roll_down(self):
        for div in range(self.n):
            start = int(div*self.height/self.n)
            end = int((div+1)*self.height/self.n)
            self.fbuff[start:end,:,:] = self.vbuff[(self.f0-div)%self.n,start:end,:,:]

    def roll_left(self):
        for div in range(self.n):
            start = int(div*self.width/self.n)
            end = int((div+1)*self.width/self.n)
            self.fbuff[:,start:end,:] = self.vbuff[(self.f0+div+1)%self.n,:,start:end,:]

    def roll_right(self):
        for div in range(self.n):
            start = int(div*self.width/self.n)
            end = int((div+1)*self.width/self.n)
            self.fbuff[:,start:end,:] = self.vbuff[(self.f0-div)%self.n,:,start:end,:]

    def save_show_increment(self):
        if not self.fullbufferonly or self.fNo >= self.n:
            self.out.write(self.fbuff)
            if self.preview:
                cv2.imshow('Preview',self.fbuff)
        self.fNo = self.fNo + 1 ; self.f0 = self.fNo % self.n


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Python script that adds a rolling shutter effect to videos.')

    parser.add_argument('--input', '-i',
    nargs=1, 
    required=True, 
    type=str,
    help='The name of the input file')

    parser.add_argument('--output', '-o', 
    default=['output.avi'], 
    nargs=1,
    type=str,
    help='The name of the output file')

    parser.add_argument('--direction', '-d', 
    choices=['UP', 'DOWN', 'LEFT', 'RIGHT'],
    default=['DOWN'],
    nargs=1,
    type=str,
    help='The direction of the increasing time offset that creates the rolling shutter effect')

    parser.add_argument('--framerate', '-fr', 
    default=[0], 
    nargs=1,
    type=int,
    help='The framerate of the output video (0 means same as input video)')

    parser.add_argument('--buffersize', '-bs',
    default=[0],  
    nargs=1,
    type=int,
    help='The number of time splices in the output video (0 means full resolution)')

    parser.add_argument('--outputformat', '-of', 
    choices=['DIVX', 'XVID', 'MJPG', 'X264', 'WMV1', 'WMV2'],
    default=['DIVX'], 
    nargs=1,
    type=str,
    help='The format of the output video')

    parser.add_argument('--fullbufferonly', '-fbo',
    action='store_true',
    help='Only use frames that were made from a full buffer in the output video.')

    parser.add_argument('--preview', '-p',
    action='store_true',
    help='Displays a live preview while the video is rendering.')

    args = parser.parse_args()

    main(args)