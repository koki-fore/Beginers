    box = cv2.boxPoints(rect)
    box = np.int0(box)
    im = cv2.drawContours(im,[box],0,(0,0,255),2)