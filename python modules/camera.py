import cv2
import utils
import random
import numpy as np
import os
from time import sleep

class camera:
    def __init__(self, device_id, crop_tuple, puzzle_dims, puzzle_num):
        self.device_id = device_id
        self.puzzle_image_path = "full" + str(puzzle_num) + ".JPG"
        self.crop_tuple = crop_tuple
        self.puzzle_dims = puzzle_dims



    def crop_photo(self, photo_path):
        img = cv2.imread(photo_path)
        x = self.crop_tuple[0]
        w = self.crop_tuple[1]
        y = self.crop_tuple[2]
        h = self.crop_tuple[3]
        crop_img = img[y:y + h, x:x + w]
        cv2.imwrite(photo_path, crop_img)

    def show(self):
        cam = cv2.VideoCapture(2)  # 0 -> index of camera

        while True:  # frame captured without any errors
            s, img = cam.read()
            x = self.crop_tuple[0]
            w = self.crop_tuple[1]
            y = self.crop_tuple[2]
            h = self.crop_tuple[3]
            thickness_ = 0.5
            img = cv2.line(img, (x, y), (x+ w , y), color=(0, 0, 255), thickness = 1)
            img = cv2.line(img, (x +w, y), (x+ w , y +h), color=(0, 0, 255), thickness= 1)
            img = cv2.line(img, (x , y), (x , y +h), color=(0, 0, 255), thickness= 1)
            img = cv2.line(img, (x, y +h), (x+ w , y +h), color=(0, 0, 255), thickness= 1)
            cv2.imshow("cam-test", img)
            #cv2.waitKey(0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()

    def take_photo(self, photo_name):
        cam = cv2.VideoCapture(self.device_id)
        ret, frame = cam.read()
        cv2.imwrite(photo_name, frame)
        sleep(2)
        cam.release()
        print("Taking photo " + photo_name)
        return photo_name

    def detect_rect(self):
        im = cv2.imread('box.jpeg')
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
        cv2.imshow("box",im)
        cv2.waitKey(0)

    def delete_photo(self, photo_name):
        os.remove(photo_name)


    def find_matching_coaards(self, small_img):
        img1 = cv2.imread(small_img, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(self.puzzle_image_path, cv2.IMREAD_GRAYSCALE)

        pieces_in_row = self.puzzle_dims[0]  # int(args.pieces_in_row)
        pieces_in_colomn = self.puzzle_dims[1]  # int(args.pieces_in_colomn)

        height = img2.shape[0]
        width = img2.shape[1]

        if img1 is None or img2 is None:
            print('Could not open or find the images!')
            exit(0)
        # -- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
        minHessian = 400
        detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)
        keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
        keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
        # -- Step 2: Matching descriptor vectors with a FLANN based matcher
        # Since SURF is a floating-point descriptor NORM_L2 is used
        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
        # -- Filter matches using the Lowe's ratio test
        ratio_thresh = 0.7
        good_matches = []
        for m, n in knn_matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)

        good_matches = sorted(good_matches, key=lambda x: x.distance)

        best_keypoints_and_grades = [(keypoints2[match.trainIdx].pt, match.distance) for match in good_matches[:10]]

        int_keypoints = [((int)((shape[0])[0]), (int)((shape[0])[1])) for shape in best_keypoints_and_grades]

        squares_matches = [utils.translate(keypoint, width, pieces_in_row, height, pieces_in_colomn) for keypoint in
                           int_keypoints]


        #Matrix = [[0 for x in range(pieces_in_row)] for y in range(pieces_in_colomn)]
        if len(squares_matches) == 0:
            return 0
        most_common_coaards = utils.most_common(squares_matches)
        print("Found Matching coaards for " + small_img)
        #return most_common_coaards[0] + most_common_coaards[1] * pieces_in_row

        # -- Draw matches
        img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
        cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches[:10], img_matches,
                       flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        # -- Show detected matches
        #img_matches = cv2.resize(img_matches, tuple([(int)(0.3 * x) for x in img_matches.shape[:2]]),
         #                       interpolation=cv2.INTER_AREA)
        img2 = cv2.resize(img2, tuple([(int)(0.3 * x) for x in img2.shape[:2]]), interpolation=cv2.INTER_AREA)
        utils.draw_lines_on_photo(img2, 6, 4)
        cv2.imshow('Good Matches', img_matches)
        #cv2.imshow('Original photo', img2)
        cv2.waitKey(20000)
        
        
        #drawing circles on the photo
        length = len(int_keypoints)
        my_grades = [shape[1] for shape in best_keypoints_and_grades]
        color = (255, 0, 0)
        for keypoint in int_keypoints:
            img2 = cv2.circle(img2, keypoint, 20,
                             (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
        return most_common_coaards[0] + most_common_coaards[1] * pieces_in_row






