import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

def remove_line(img, ksize):
    blur = cv2.blur(img, (ksize, ksize))
    rij = img/blur
    index_1 = np.where(rij >= 1.00) # 1以上の値があると邪魔なため
    rij[index_1] = 1
    img_rmline = np.array(rij*255, np.uint8)
    #img_rmline = cv2.cvtColor(img_rmline, cv2.COLOR_BGR2GRAY)
    """
    plt.imshow(img_rmline)
    plt.colorbar()
    plt.show()
"""
    return img_rmline


def detect_receipt(img, threshold):
    height, width, _ = img.shape  # 形状取得 
    center = (int(width/2), int(height/2))  # 中心座標設定

    # グレースケールに変換する
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2値化する
    ret, bin_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # 輪郭を抽出する
    contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 最大面積の輪郭を取得する
    max_contour = max(contours, key=lambda x: cv2.contourArea(x))
    """
    # 輪郭の周囲の長さを計算する
    arclen = cv2.arcLength(max_contour, True)
    # 輪郭を近似する。
    approx_cnt = cv2.approxPolyDP(max_contour, epsilon=0.005 * arclen, closed=True)
    
    area = cv2.contourArea(approx_cnt)
    print(f"area: {area}")
    x, y, width, height = cv2.boundingRect(approx_cnt)
    print(f"topleft: ({x}, {y}), width: {width}, height: {height}")
    cutimg = img[y+10: height+y-10, x+10:width+x-10]

    # 元の輪郭及び近似した輪郭の点の数を表示する。
    print(f"before: {len(max_contour)}, after: {len(approx_cnt)}")
"""

    rect = cv2.minAreaRect(max_contour)
    angle = rect[2]
    if angle > 45:
        angle -= 90
    elif angle < -45:
        angle += 90
    print(angle)
    
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    print(box)
    #im = cv2.drawContours(img,[box],0,(0,0,255),10)

    trans = cv2.getRotationMatrix2D(center, angle, scale=1)  # 変換行列の算出
    print(trans)
    img2 = cv2.warpAffine(img, trans, (width, height))
    plt.imshow(img2)
    plt.show()

    return img2

def process_img(img, threshold, ksize):
    
    #レシート位置検出  
    cutimg = detect_receipt(img, threshold)
    """
    plt.imshow(cutimg)
    plt.show()

    # しわ除去
    cleanedimg = remove_line(cutimg, ksize)
    plt.imshow(cleanedimg)
    plt.show()

    # PIL.Image形式に変換
    img_cleaned = Image.fromarray(cleanedimg)
    return img_cleaned
    """

if __name__ == "__main__":
    img_path = r"C:\Users\Nir\Documents\develop\receipt_img\IMG_5499.jpg"
    img = cv2.imread(img_path)
    process_img(img, 127, 51)
