import threading

import cv2
from deepface import DeepFace

# specify no of cameras you want to use 
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#specify the dimension
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


#we want to detect the face once a while in the frame

counter = 0


face_match = False

# load the reference image

# ref_image = cv2.imread("my_reference_image.jpg")
ref_image = cv2.imread("my_reference_image_3.jpg")
# ref_image = cv2.imread("my_reference_image_2.jpeg")

def check_face(frame):
    global face_match
    try:
        # check the current frame or image with the reference image
        if DeepFace.verify(frame, ref_image.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

while True:
    returnValue, frame = cap.read()

    if returnValue:
        # for every 30 iterations
        if counter % 30 == 0:
            try:
                #start a new thread
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            #if a there is no match it throws a generic error
            except ValueError:
                pass
        counter += 1

        if face_match:
            cv2.putText(frame, "WE GOT HIM", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255,0), 3)
            #take a picture or capture image
            if counter % 30 == 0:
                img_name = "faces/facial_rec_{}.png".format(counter)
                cv2.imwrite(img_name, frame)

        else:
            cv2.putText(frame, "NO MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        #show the result
        cv2.imshow("CCTV - Facial Rec for MIS 500", frame)

    #get the key from every iteration
    key = cv2.waitKey(1)
    # if I press q break
    if key == ord("q"):
        break

cv2.destroyAllWindows()