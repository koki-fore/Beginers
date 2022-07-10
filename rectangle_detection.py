import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

def imshow(img):
    plt.imshow(img)
    plt.colorbar()
    plt.show()

def remove_line(img, ksize):
    """画像内のしわを除去

    Args:
        img (np.array): detect_receiptで切り取った画像
        ksize (int): 画像をガウシアンぼかしにかけるときのぼかし量

    Returns:
        img: しわ除去した画像
    """

    # しわ除去のためにぼかし画像を作成
    blur = cv2.blur(img, (ksize, ksize))
    # しわを除去
    np.seterr(invalid='ignore')
    rm_line = img/blur

    # 1以上の値があると邪魔なため
    idx = np.where(rm_line >= 1.00) 
    rm_line[idx] = 1
    
    # 配列がfloat64のため、uint8に変更（PIL変換のため）
    img_rmline = np.array(rm_line*255, np.uint8)

    return img_rmline


def detect_receipt(img, threshold):
    """レシートの傾き補正、背景削除

    Args:
        img (np.array): receipt_csanから送られてきた画像
        threshold (int): 画像二値化のしきい値

    Returns:
        rotatedcroppedimg: 背景削除、回転補正、レシート切り出しを行った画像
    """
    
    height, width, _ = img.shape  # 形状取得 
    center = (int(width/2), int(height/2))  # 中心座標設定

    # グレースケールに変換、二値化する
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # 輪郭を抽出する
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 最大面積の輪郭を取得する
    max_contour = max(contours, key=lambda x: cv2.contourArea(x))

    # 背景削除のためにマスク画像を生成
    mask = np.zeros((height, width, 3), dtype=np.uint8)
    mask = cv2.fillConvexPoly(mask, max_contour, color=[1, 1, 1])
    #imshow(mask)

    # マスク画像を元画像と重ね合わせて背景を削除する
    maskedimg = img * mask
    #img = np.where(mask==255, img, img=[255, 255, 255])
    #imshow(maskedimg)

    # 斜めを考慮した矩形を取得する
    rect = cv2.minAreaRect(max_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # 取得された angle が+90(-90)されている時があるので、補正する
    angle = rect[2]
    if angle > 45:
        angle -= 90
    elif angle < -45:
        angle += 90

    # affine行列を用いて画像を回転させる
    M = cv2.getRotationMatrix2D(center, angle, 1)
    rotatedimg = cv2.warpAffine(maskedimg, M, (width, height))
    #print("rect:\n{}".format(rect))

    # 矩形領域の中心と長さを取得
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    size = (x2-x1, y2-y1)
    center = ((x1+x2)/2, (y1+y2)/2)

    # 斜め矩形領域を切り抜く cv2.getRectSubpix(画像, 矩形領域, 中心座標)
    rotatedcroppedimg = cv2.getRectSubPix(rotatedimg, size, center)

    return rotatedcroppedimg

def process_img(img, threshold, ksize):
    """画像処理全般の根幹

    Args:
        img (np.array): 入力された画像
        threshold (int): 画像二値化のしきい値, detect_receiptで使用
        ksize (int): 画像をガウシアンぼかしにかけるときのぼかし量, remove_lineで使用

    Returns:
        _type_: _description_
    """
    
    #レシート回転補正・位置検出・背景削除
    cutimg = detect_receipt(img, threshold)
    #imshow(cutimg)

    # しわ除去
    cleanedimg = remove_line(cutimg, ksize)
    #imshow(cleanedimg)

    # PIL.Image形式に変換
    cleanedimg = Image.fromarray(cleanedimg)
    return cleanedimg


if __name__ == "__main__":
    img_path = r"C:\Users\Nir\Documents\develop\receipt_img\IMG_5496.jpg"
    img = cv2.imread(img_path)
    process_img(img, 127, 51)
