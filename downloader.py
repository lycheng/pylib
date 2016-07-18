# -*- coding: utf-8 -*-

import argparse

from pylib.line_stickers_downloader import LineStickerDownloader


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ids', metavar='N', type=int, nargs='+',
                        help='sticker ids')
    parser.add_argument("--dir",
                        help="dir path for images to store, default pwd",
                        type=int)
    parser.add_argument("-d", "--debug", help="just show the images url",
                        action="store_true")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = init_args()

    ldl = LineStickerDownloader(args.debug)
    for sid in args.ids:
        ldl.run(sid)
