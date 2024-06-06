##################################################
# Image Recognition functions                    #
# Version 1.0.1.14 - Released 2024-06-04         #
# Author - Lawrence Lutton                       #
##################################################

import cv2
from matplotlib import pyplot as plt
import urllib.request
import numpy as np
import os
import glob
from os import walk

# image = "Resources/images-2.jpeg"
# image = "images-2.jpeg"
# image = "Resources/engineer-2.jpg"

def read_iamge():
    # LOAD AN IMAGE USING 'IMREAD'
    img = cv2.imread("Resources/engineer-1.jpg")
    # DISPLAY
    cv2.imshow("Engineer", img)
    cv2.waitKey(0)

def face_detector(image):
    face_Cascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    image = cv2.imread(image)
    # image = cv2.imread("Resources/engineer-2.jpg")
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    faces = face_Cascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Creates the environment of
        # the picture and shows it
        # plt.subplot(1, 1, 1)
        # plt.imshow(img_rgb)
        # plt.show()
        print("Found a face")
        cv2.imwrite(f"python2.jpeg", img_rgb)
        return 1

    # cv2.imshow("Result", image)
    # cv2.waitKey(0)

def stop_sign_recognition(image):
    print("Stop sign recognition")
    print(image)
    # Opening image
    # img = cv2.imread("Resources/images-2.jpeg")
    # image = "python1.jpeg"
    img = cv2.imread(image)
    # OpenCV opens images as BRG
    # but we want it as RGB We'll
    # also need a grayscale version
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Use minSize because for not
    # bothering with extra-small
    # dots that would look like STOP signs
    stop_data = cv2.CascadeClassifier("Resources/stop_data.xml")

    found = stop_data.detectMultiScale(img_gray,
                                       minSize=(20, 20))

    # Don't do anything if there's
    # no sign
    amount_found = len(found)

    if amount_found != 0:

        # There may be more than one
        # sign in the image
        for (x, y, width, height) in found:
            # We draw a green rectangle around
            # every recognized sign
            cv2.rectangle(img_rgb, (x, y),
                          (x + height, y + width),
                          (0, 255, 0), 5)
            print("Found a stop sign")
            cv2.imwrite(f"python2.jpeg", img_rgb)
            # Creates the environment of
            # the picture and shows it
            # plt.subplot(1, 1, 1)
            # plt.imshow(img_rgb)
            # plt.show()
            return 1


def training_folder():

    def load_images_from_folder(folder):
        images = []
        for filename in os.listdir(folder):
            file = os.path.join(folder, filename)
            img = cv2.imread(file)
            if img is not None:
                images.append(img)
        return images

    finalCascadeFile = 'Resources/lawrence-cascade.xml'
    cascade_lawrence = cv2.CascadeClassifier(finalCascadeFile)
    images = load_images_from_folder("Resources/photos")
    for i in range(0, len(images)):
        image = images[i]
        rectangles = cascade_lawrence.detectMultiScale(image)
        print(rectangles)
        print("no of objects in the image: " + str(len(rectangles)))
        for cords in rectangles:
            print(type(cords[0]))
            image = cv2.rectangle(image, (cords[0], cords[1]), (cords[0] + cords[2], cords[1] + cords[3]), (255, 0, 0),
                                  2)

            cv2.imwrite("Resources/Lawrence/newImage_" + str(i) + ".jpg", image)
    print("all images detected")

def learning_video_cap():

    face_cascade = cv2.CascadeClassifier('Resources/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('Resources/haarcascade_eye.xml')

    # this is the cascade we just made. Call what you want
    # watch_cascade = cv2.CascadeClassifier('watchcascade10stage.xml')

    cap = cv2.VideoCapture(0)

    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # add this
        # image, reject levels level weights.
        # watches = watch_cascade.detectMultiScale(gray, 50, 50)

        # add this
        # for (x, y, w, h) in watches:
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # saving the image
    # pygame.image.save(image, "filename.jpg")

    cap.release()
    cv2.destroyAllWindows()

def store_raw_images():
    # neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'
    # neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1

    # neg_image_urls = next(walk('idenprof/test/engineer/'), (None, None, []))[2]  # [] if no file
    # neg_image_urls = 'idenprof/test/engineer/*.*'

    if not os.path.exists('neg'):
        os.makedirs('neg')

    neg_image_urls = []
    for i in glob.glob("idenprof/test/engineer/*.jpg"):
        try:
            print(i)
            # (i, "idenprof/test/engineer/" + "engineer-" + str(pic_num) + ".jpg")
            # img = cv2.imread("idenprof/test/engineer/" + "engineer-" + str(pic_num) + ".jpg", cv2.IMREAD_GRAYSCALE)
            img = cv2.imread(f"{i}", cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite(f"neg/" + "engineer-" + str(pic_num) + ".jpg", resized_image)
            pic_num += 1


        except Exception as e:
            print(str(e))

def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

"""
def store_raw_images():
    neg_images_link = '//image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 953

    if not os.path.exists('neg'):
        os.makedirs('neg')

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/" + str(pic_num) + ".jpg")
            img = cv2.imread("neg/" + str(pic_num) + ".jpg", cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/" + str(pic_num) + ".jpg", resized_image)
            pic_num += 1

        except Exception as e:
            print(str(e))
"""

# face_detector(image)
# stop_sign_recognition(image)
# learning_video_cap()
# store_raw_images()
# find_uglies()
# training_folder()
