from utils.json_writer import dump_json
from dl import ComicTextDetector, MangaOCR, LamaInpainterMPE, SugoiTranslator
from utils.io_utils import imread, imwrite, NumpyEncoder
import os
from pathlib import Path
import numpy as np
from typing import List, Dict, Union

ctd = ComicTextDetector()
# mask, blk_list = ctd.detect(img: np.ndarray)
ocr = MangaOCR()
# blk_list = ocr.run_ocr(img: np.ndarray, blk_list)
inpainter = LamaInpainterMPE()
# inpainter.inpaint(img: np.ndarray, mask: np.ndarray, blk_list=None)
translator = SugoiTranslator('日本語', 'English')
# translator.translate(text)
# translator.translate_textblk_lst(blk_list)


class R2S:
    def __init__(self, ctd=ctd, ocr=ocr, inpainter=inpainter, translator=translator):
        self.ctd = ctd
        self.ocr = ocr
        self.inpainter = inpainter
        self.translator = translator
        self.image = None
        self.im_h = None
        self.im_w = None
        self.blk_list = None
        self.mask = None
        self.inpaint_image = None

    def __call__(self, img: np.ndarray):
        img = imread(img)
        self.image = img
        self.im_h, self.im_w = img.shape[:2]
        self.mask, self.blk_list = self.detect_text(img)
        self.blk_list = self.run_ocr(img, self.blk_list)
        self.json = self.blk_lst_to_json(self.blk_list)
        return self.json

    def detect_text(self, img: np.ndarray):
        return self.ctd.detect(img)

    def run_ocr(self, img: np.ndarray, blk_list=None):
        return self.ocr.run_ocr(img, blk_list)

    def inpaint(self, img: np.ndarray, mask: np.ndarray, blk_list=None):
        return self.inpainter.inpaint(img, mask, blk_list)

    def translate(self, text):
        if isinstance(text, str):
            return self.translator.translate(text)
        else:
            return self.translator.translate_textblk_lst(text)

    def blk_lst_to_json(self, blk_list, w: str = '', h: str = '') -> Dict:
        if not w and not h:
            w = self.im_w
            h = self.im_h

        result = {'img_width': w,
                  'img_height': h,
                  'blocks': []
                  }

        for blk in blk_list:
            result_blk = {
                'text_box': blk.xyxy,
                'text_ocr': blk.text,
                'text_tl': blk.translation,
                'font_size': blk.font_size,
            }
            result['blocks'].append(result_blk)

        return result


# def blk_lst_to_json(blk_list, h: str = '', w: str = '') -> Dict:
#     result = {'img_width': w,
#               'img_height': h,
#               'blocks': []
#               }

#     for blk in blk_list:
#         result_blk = {
#             'text_box': blk.xyxy,
#             'text_ocr': blk.text,
#             'text_tl': blk.translation,
#             'font_size': blk.font_size,
#         }
#         result['blocks'].append(result_blk)

#     return result


# def ocr_inpaint_translate(img: np.ndarray):
#     mask, blk_list = ctd.detect(img)
#     blk_list = ocr.run_ocr(img, blk_list)
#     blk_list = translator.translate_textblk_lst(blk_list)
#     inpaint = inpainter.inpaint(img, mask, blk_list)
#     return inpaint, blk_list


# def redraw(img: np.ndarray, mask: np.ndarray):
#     return inpainter.inpaint(img, mask)


# def get_json(img, blk_list=None):
#     img = imread(img)
#     im_h, im_w = img.shape[:2]
#     imwrite('test.png', img)
#     if blk_list is None:
#         _, blk_list = ocr_inpaint_translate(img)
#         return (blk_lst_to_json(blk_list, im_h, im_w))
#     return blk_lst_to_json(blk_list, im_h, im_w)

if __name__ == "__main__":
    test_img = r'data/testpacks/custom/07.png'
    image_path = Path(test_img).expanduser().absolute()
    img = imread(image_path)

    test_dir = image_path.parent

    mask_dir = os.path.join(test_dir, 'mask')
    os.makedirs(mask_dir, exist_ok=True)

    ocr_dir = os.path.join(test_dir, 'ocr_test')
    os.makedirs(ocr_dir, exist_ok=True)

    inpaint_dir = os.path.join(test_dir, 'inpainted')
    os.makedirs(inpaint_dir, exist_ok=True)

    def detect_text(img: np.ndarray):
        # ctd = ComicTextDetector()
        mask, blk_list = ctd.detect(img)
        return mask, blk_list

    def mangaocr(img: np.ndarray, blk_list):
        # ocr = MangaOCR()
        blk_list = ocr.run_ocr(img, blk_list)
        return blk_list

    def inpaint_lama_mpe(img: np.ndarray, mask: np.ndarray, blk_list=None, inpaint_by_block=True):
        # inpainter = LamaInpainterMPE()
        inpainter.inpaint_by_block = inpaint_by_block
        inpainted = inpainter.inpaint(img, mask, blk_list)
        return inpainted

    def sugoi_translate(text: str):
        # translator = SugoiTranslator('日本語', 'English')
        translation = translator.translate(text)
        print(f'src: {text}, translation: {translation}')

    mask, blk_list = detect_text(img)
    blk_list = mangaocr(img, blk_list)
    inpainted = inpaint_lama_mpe(img, mask, blk_list)
    imwrite(mask_dir + '/' + image_path.name, mask)
    imwrite(inpaint_dir + '/' + image_path.name, inpainted)
