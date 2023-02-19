import argparse
from utils.json_writer import JsonOcr, write_json
import ws

ocr_model = 'models/manga-ocr-base'
detector_model = 'models/comictextdetector.pt'

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="input file")
parser.add_argument("-o", "--output", default='results',
                    type=str, help="output directory")
parser.add_argument("--ocr-model", default=ocr_model,
                    type=str, help="change directory of ocr model")
parser.add_argument("--detector-model", default=detector_model,
                    type=str, help="change directory of detector model")
parser.add_argument("-m", "--mode", help="select run mode", choices=["cli", "ws"], default="cli")
parser.add_argument("--ws-port", help="specify websocket port (default: 5005)", type=int, default=5005)

args = parser.parse_args()

if args.mode=="cli":
    json_ocr = JsonOcr(ocr_model, detector_model)
    write_json(args.input, args.output, json_ocr)
elif args.mode=="ws":
    ws.start(port=args.ws_port)