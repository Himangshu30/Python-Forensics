from __future__ import print_function
import argparse
import biplist
import os
import sys



def main(plist):
    print("[+] Opening {} file".format(plist))
    try:
        plist_data = biplist.readPlist(plist)
    except (biplist.InvalidPlistException,
            biplist.NotBinaryPlistException) as e:
        print("[-] Invalid PLIST file - unable to be opened by biplist")
        sys.exit(2)

    print("[+] Printing Info.plist Device "
          "and User Information to Console\n")
    for k in plist_data:
        if k != 'Applications' and k != 'iTunes Files':
            print("{:<25s} - {}".format(k, plist_data[k]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("PLIST_FILE", help="Input PList File")
    args = parser.parse_args()

    if not os.path.exists(args.PLIST_FILE) or \
            not os.path.isfile(args.PLIST_FILE):
        print("[-] {} does not exist or is not a file".format(
            args.PLIST_FILE))
        sys.exit(1)

    main(args.PLIST_FILE)
