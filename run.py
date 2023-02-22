import argparse
import ws
import web
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="input file")
parser.add_argument("-o", "--output", default=r'tmp/results',
                    type=str, help="output directory")
parser.add_argument("--ocr-model", default='manga_ocr',
                    type=str, help="change directory of ocr model")
parser.add_argument("--detector-model", default='',
                    type=str, help="change directory of detector model")
parser.add_argument("-m", "--mode", help="select run mode", choices=["cli", "ws", "rest"], default="cli")
parser.add_argument("--ws-port", help="specify websocket port (default: 5005)", type=int, default=5005)
parser.add_argument("--http-port", help="specify http port (default: 5000)", type=int, default=5000)

args = parser.parse_args()

if args.mode=="cli":
    pass
elif args.mode=="ws":
    asyncio.run(ws.main(port=args.ws_port))
elif args.mode=="rest":
    web.app.run("0.0.0.0", args.http_port)
