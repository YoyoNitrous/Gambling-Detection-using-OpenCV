from threading import Thread
import cv2


class VideoStream:
    """Camera object"""
    def __init__(self, resolution=(640,480),framerate=30,PiOrUSB=2,src=0):

       
        self.PiOrUSB = PiOrUSB

        if self.PiOrUSB == 1: # PiCamera
            from picamera.array import PiRGBArray
            from picamera import PiCamera

            self.camera = PiCamera()
            self.camera.resolution = resolution
            self.camera.framerate = framerate
            self.rawCapture = PiRGBArray(self.camera,size=resolution)
            self.stream = self.camera.capture_continuous(
                self.rawCapture, format = "bgr", use_video_port = True)

            self.frame = []

        if self.PiOrUSB == 2:
            self.stream = cv2.VideoCapture(src)
            ret = self.stream.set(3,resolution[0])
            ret = self.stream.set(4,resolution[1])

            (self.grabbed, self.frame) = self.stream.read()

	# Create a variable to control when the camera is stopped
        self.stopped = False

    def start(self):
        Thread(target=self.update,args=()).start()
        return self

    def update(self):

        if self.PiOrUSB == 1: # PiCamera
            
            for f in self.stream:
                self.frame = f.array
                self.rawCapture.truncate(0)

                if self.stopped:
                    self.stream.close()
                    self.rawCapture.close()
                    self.camera.close()

        if self.PiOrUSB == 2: # USB camera

            while True:
         
                if self.stopped:
                
                    self.stream.release()
                    return

                (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
