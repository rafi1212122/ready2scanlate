import cv2
import numpy as np
from PIL import Image
from scipy.signal.windows import gaussian
from comic_text_detector.inference import TextDetector
from manga_ocr import MangaOcr
import json
from pathlib import Path
from torch import cuda


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.generic):
            return obj.item()
        return json.JSONEncoder.default(self, obj)


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def dump_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, cls=NumpyEncoder)


def imread(path):
    """cv2.imread, but works with unicode paths"""
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)


class JsonOcr:
    def __init__(self,
                 ocr_model='models/manga-ocr-base',
                 text_seg_model='models/comictextdetector.pt',
                 force_cpu=False,
                 seg_input_size=1024,
                 text_height=64,
                 max_ratio_vert=16,
                 max_ratio_hor=8,
                 anchor_window=2,
                 ):

        self.text_height = text_height
        self.max_ratio_vert = max_ratio_vert
        self.max_ratio_hor = max_ratio_hor
        self.anchor_window = anchor_window

        self.text_detector = TextDetector(
            model_path=text_seg_model, input_size=seg_input_size, device="cuda" if cuda.is_available() else "cpu")
        self.mocr = MangaOcr(ocr_model, force_cpu)

    def __call__(self, img_path):
        img = imread(img_path)
        H, W, *_ = img.shape
        mask, mask_refined, blk_list = self.text_detector(
            img, refine_mode=1, keep_undetected_mask=True)

        result = {'img_width': W, 'img_height': H, 'blocks': []}

        for blk in blk_list:

            result_blk = {
                'box': list(blk.xyxy),
                'vertical': blk.vertical,
                'font_size': blk.font_size,
                'lines_coords': [],
                'lines': []
            }

            for line_idx, line in enumerate(blk.lines_array()):
                if blk.vertical:
                    max_ratio = self.max_ratio_vert
                else:
                    max_ratio = self.max_ratio_hor

                line_crops, cut_points = self.split_into_chunks(
                    img, mask_refined, blk, line_idx,
                    textheight=self.text_height, max_ratio=max_ratio, anchor_window=self.anchor_window)

                line_text = ''
                for line_crop in line_crops:
                    if blk.vertical:
                        line_crop = cv2.rotate(
                            line_crop, cv2.ROTATE_90_CLOCKWISE)
                    line_text += self.mocr(Image.fromarray(line_crop))

                result_blk['lines_coords'].append(line.tolist())
                result_blk['lines'].append(line_text)

            result['blocks'].append(result_blk)

        return result

    @staticmethod
    def split_into_chunks(img, mask_refined, blk, line_idx, textheight, max_ratio=16, anchor_window=2):
        line_crop = blk.get_transformed_region(img, line_idx, textheight)

        h, w, *_ = line_crop.shape
        ratio = w / h

        if ratio <= max_ratio:
            return [line_crop], []

        else:
            k = gaussian(textheight * 2, textheight / 8)

            line_mask = blk.get_transformed_region(
                mask_refined, line_idx, textheight)
            num_chunks = int(np.ceil(ratio / max_ratio))

            anchors = np.linspace(0, w, num_chunks + 1)[1:-1]

            line_density = line_mask.sum(axis=0)
            line_density = np.convolve(line_density, k, 'same')
            line_density /= line_density.max()

            anchor_window *= textheight

            cut_points = []
            for anchor in anchors:
                anchor = int(anchor)

                n0 = np.clip(anchor - anchor_window // 2, 0, w)
                n1 = np.clip(anchor + anchor_window // 2, 0, w)

                p = line_density[n0:n1].argmin()
                p += n0

                cut_points.append(p)

            return np.split(line_crop, cut_points, axis=1), cut_points


def write_json(image_path, output_dir, json_ocr: JsonOcr):
    image_path = Path(image_path).expanduser().absolute()
    output_dir = Path(output_dir).expanduser().absolute()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = (output_dir / image_path.name).with_suffix('.json')
    result = json_ocr(image_path)
    dump_json(result, json_path)
