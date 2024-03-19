import cv2
import os

def frames_count(video_path):
    cam = cv2.VideoCapture(video_path)
    return cam.get(cv2.CAP_PROP_FRAME_COUNT)

def video_to_image(video_path, destination_path, limit, skip=1):
    cam = cv2.VideoCapture(video_path)
    try:
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
    except OSError:
        print ('Error: Creating directory of data')
    print('Creating images...')
    destination_path = destination_path.strip('/') + '/'
    currentframe = 0
    while(True):
        ret,frame = cam.read()
        if ret:
            if(currentframe%skip==0):
                name = destination_path + str(currentframe//skip) + '.jpg'
                print ('\rCreating...' + name, end = "")
                cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break
        if(currentframe//skip > limit):
            break
    cam.release()
    cv2.destroyAllWindows()
    print('\nDone')