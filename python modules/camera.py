import cv2
import utils
import random
import numpy as np


class camera:
    def __init__(self, device_id, puzzle_image_path):
        self.device_id = device_id
        self.puzzle_image_path = puzzle_image_path

    def take_photo(self, photo_name):
        cam = cv2.VideoCapture(2)
        ret, frame = cam.read()
        img_name = photo_name + ".png"
        cv2.imwrite(img_name, frame)
        return img_name

    def find_matching_coaards(self, small_img, pieces_in_row, pieces_in_colomn ):
        img1 = cv2.imread(small_img, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(self.puzzle_image_path, cv2.IMREAD_GRAYSCALE)

        pieces_in_row = 4  # int(args.pieces_in_row)
        pieces_in_colomn = 4  # int(args.pieces_in_colomn)

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

        return (utils.most_common(squares_matches))
        '''
        # -- Draw matches
        img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
        cv.drawMatches(img1, keypoints1, img2, keypoints2, good_matches[:10], img_matches,
                       flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        # -- Show detected matches
        img_matches = cv.resize(img_matches, tuple([(int)(0.3 * x) for x in img_matches.shape[:2]]),
                                interpolation=cv.INTER_AREA)
        img2 = cv.resize(img2, tuple([(int)(0.3 * x) for x in img2.shape[:2]]), interpolation=cv.INTER_AREA)
        utils.draw_lines_on_photo(img2, 4, 4)
        cv.imshow('Good Matches', img_matches)
        cv.imshow('Original photo', img2)
        cv.waitKey(20000)
        
        
        #drawing circles on the photo
        length = len(int_keypoints)
        my_grades = [shape[1] for shape in best_keypoints_and_grades]
        color = (255, 0, 0)
        for keypoint in int_keypoints:
            img2 = cv2.circle(img2, keypoint, 20,
                             (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
        '''
