from __future__ import print_function
import argparse
from multiprocessing import freeze_support
import os
import sys
import time

try:
    import pyscreenshot
    import wx
except ImportError:
    print("[-] Install wx and pyscreenshot to use this script")
    sys.exit(1)

"


def main(output_dir, interval, total):
    i = 0
    while True:
        i += 1
        time.sleep(interval)
        image = pyscreenshot.grab()
        output = os.path.join(output_dir, "screenshot_{}.png").format(i)
        image.save(output)
        print("[+] Took screenshot {} and saved it to {}".format(
            i, output_dir))
        if total is not None and i == total:
            print("[+] Finished taking {} screenshots every {} "
                  "seconds".format(total, interval))
            sys.exit(0)


if __name__ == "__main__":
    # Command-line Argument Parser
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("OUTPUT_DIR", help="Desired Output Path")
    parser.add_argument(
        "INTERVAL", help="Screenshot interval (seconds)", type=int)
    parser.add_argument(
        "-total", help="Total number of screenshots to take", type=int)
    args = parser.parse_args()

    if not os.path.exists(args.OUTPUT_DIR):
        os.makedirs(args.OUTPUT_DIR)

    main(args.OUTPUT_DIR, args.INTERVAL, args.total)
