import time
import cv2
import numpy as np

# Video source - can be camera index number given by 'ls /dev/video*
# or can be a video file, e.g. '~/Video.avi'
cap = cv2.VideoCapture(0)

framerate = 0
mask = None
alpha = 0.6

try:
    while(True):
        timestamp = time.time()

        ret, frame = cap.read()

        if mask is None:
            mask = np.ones(frame.shape[:2])

        # mask = (frame.ptp(axis=2) < 20) & (frame[:, :, 0] > 70)

        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_update = ((frame2[:, :, 0] > 50) & (frame2[:, :, 0] < 120) & (frame2[:, :, 1] > 100))
        # mask = (frame2[:, :, 0] > 170) & (frame2[:, :, 0] < 190)  #  & (frame2[:, :, 1] > 80)

        mask = (1 - alpha) * mask + alpha * mask_update

        frame[mask > 0.5] = [0, 0, 0]
        # frame *= mask

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        framerate = 0.9 * framerate + 0.1 / (time.time() - timestamp)
        # print(framerate)
finally:
    cap.release()
    cv2.destroyAllWindows()
