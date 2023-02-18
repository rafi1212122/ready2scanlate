import argparse
from utils.json_writer import JsonOcr, write_json

ocr_model = 'models/manga-ocr-base'
detector_model = 'models/comictextdetector.pt'

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="input file")
parser.add_argument("-o", "--output", default='./results/',
                    type=str, help="output directory")
parser.add_argument("--ocr-model", default=ocr_model,
                    type=str, help="change directory of ocr model")
parser.add_argument("--detector-model", default=detector_model,
                    type=str, help="change directory of detector model")

args = parser.parse_args()

json_ocr = JsonOcr(ocr_model, detector_model)
write_json(args.input, json_ocr, args.output)
