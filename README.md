# Video Roller

This python script is used to make videos with a rolling shutter effect. The output video is composed of segments of the input video but the starting time for each consecutive segment is delayed. This makes one side of the video lag behind the other thus creating the rolling shutter effect.

## Usage

```
usage: vroller.py [-h] --input INPUT [--output OUTPUT] [--direction {UP,DOWN,LEFT,RIGHT}] [--framerate FRAMERATE] [--buffersize BUFFERSIZE]
                  [--outputformat {DIVX,XVID,MJPG,X264,WMV1,WMV2}] [--fullbufferonly] [--preview]

Python script that adds a rolling shutter effect to videos.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        The name of the input file
  --output OUTPUT, -o OUTPUT
                        The name of the output file
  --direction {UP,DOWN,LEFT,RIGHT}, -d {UP,DOWN,LEFT,RIGHT}
                        The direction of the increasing time offset that creates the rolling shutter effect
  --framerate FRAMERATE, -fr FRAMERATE
                        The framerate of the output video (0 means same as input video)
  --buffersize BUFFERSIZE, -bs BUFFERSIZE
                        The number of time splices in the output video (0 means full resolution)
  --outputformat {DIVX,XVID,MJPG,X264,WMV1,WMV2}, -of {DIVX,XVID,MJPG,X264,WMV1,WMV2}
                        The format of the output video
  --fullbufferonly, -fbo
                        Only use frames that were made from a full buffer in the output video.
  --preview, -p         Displays a live preview while the video is rendering.
```

### Dependencies:
- python
- python-numpy
- opencv
- hdf5

## Technology

- [OpenCV](https://github.com/opencv/opencv)
- [NumPy](https://github.com/numpy/numpy)

## License

It is licensed under the MIT License.