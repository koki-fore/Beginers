import os
import cv2
import pyocr
import numpy as np
import pandas as pd

from PIL import Image

path='C:\\Program Files\\Tesseract-OCR\\'
os.environ['PATH'] = os.environ['PATH'] + path
#pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# 画像から文字をスキャンする
def receipt_scan(img):
    """_summary_

    Args:
        img (PIL.Image): main 関数で読み込んだ画像

    Returns:
        txt: main 関数に取得した文字列を返す
    """

    # OCRエンジンを取得
    engines = pyocr.get_available_tools()
    engine = engines[0]

    # 対応言語取得
    langs = engine.get_available_languages()

    # 画像の文字を読み込む
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    txt = engine.image_to_string(img, lang="jpn", builder=builder)

    return txt

def main():
    # 画像を単枚入力
    # 複数の場合はまだ考えない
    #img_path = "./receipt_img"
    img_path = "./img"
    img_name = "sample5.jpg"
    save_dir = "./result"

    # 画像を開く
    img = Image.open(os.path.join(img_path, img_name))
    
    # 画像から文字を読み込む(receipt_scan 関数)
    txt = receipt_scan(img)
    #print(txt)
    
    # テキスト出力
    f = open(os.path.join(save_dir, 'result_{}.txt').format(os.path.splitext(img_name)[0]), 'w')
    f.write(txt)
    f.close()


if __name__ == "__main__":
    main()