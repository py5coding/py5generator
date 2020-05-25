import cv2
import numpy as np

# Video source - can be camera index number given by 'ls /dev/video*
# or can be a video file, e.g. '~/Video.avi'
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    mask = (frame.ptp(axis=2) < 20) & (frame[:, :, 0] > 70)

    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame2[:, :, 0] = 120  # (frame2[:, :, 0] + 180) % 255
    # frame2[:, :, 1] = 4 * frame2[:, :, 1]
    # frame2[:, :, 2] = frame2[:, :, 2] // 2
    frame3 = cv2.cvtColor(frame2, cv2.COLOR_HSV2BGR)
    frame3[mask] = [0, 0, 0]

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
