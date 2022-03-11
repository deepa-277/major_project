
import email
import cv2 as cv
from emailclient import EmailClient
from threading import Thread
import time


email_sent = False
count = 0
e_client = EmailClient()

def detect_face():
    global e_client, email_sent, count

    cam=cv.VideoCapture(0)

    face_cascade = cv.CascadeClassifier(cv.data.haarcascades +'haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier(cv.data.haarcascades +'haarcascade_eye.xml')


    while (True):
        _, img = cam.read()
        img = cv.flip(img, 1)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv.putText(img, "Human Face", (x, y - 30), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes: 
                cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cv.imwrite('detected_image.png', img)
                if count == 20:
                    sent = e_client.sendemail(img)
                    if sent:
                        print('Email sent successfully!!')
                        email_sent = True
                    else:
                        print('Something went wrong!!')
                count += 1
        cv.imshow("Frame", img)
        if cv.waitKey(1) == ord('q'):
            break
    print(count)
    cam.release()
    cv.destroyAllWindows()

def read_email():
    global e_client, email_sent, count
    
    while True:
        if email_sent == False:
            continue
        read = e_client.retriveemail()
        if read:
            print('Open the door!!')
            email_sent = False
            count = 0
        else:
            print('You are not allowed to enter!!') 
        print('Waiting for email...')
        time.sleep(3)
        


if __name__ == "__main__":
    thread_1 = Thread(target=detect_face, args=())
    thread_2 = Thread(target=read_email, args=())
    thread_1.start()
    thread_2.start()
    thread_2.join()
    thread_1.join()


    
