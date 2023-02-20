import argparse
from utils.json_writer import JsonOcr, write_json
import ws

ocr_models = { 
    'manga_ocr': r'models/manga-ocr-base',
    'ocr_48px_ctc': r'models/ocr-ctc.ckpt',
}
detector_model = r'models/comictextdetector.pt'

inpainting_model = r'models/inpainting_lama_mpe.ckpt'

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="input file")
parser.add_argument("-o", "--output", default=r'tmp/results',
                    type=str, help="output directory")
parser.add_argument("--ocr-model", default='manga_ocr',
                    type=str, help="change directory of ocr model")
parser.add_argument("--detector-model", default=detector_model,
                    type=str, help="change directory of detector model")
parser.add_argument("-m", "--mode", help="select run mode", choices=["cli", "ws"], default="cli")
parser.add_argument("--ws-port", help="specify websocket port (default: 5005)", type=int, default=5005)

args = parser.parse_args()

ocr_model = ocr_models[args.ocr_model]

if args.mode=="cli":
    json_ocr = JsonOcr(ocr_model, detector_model)
    write_json(args.input, args.output, json_ocr)
elif args.mode=="ws":
    ws.start(port=args.ws_port)