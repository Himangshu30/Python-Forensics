from __future__ import print_function
import argparse
from datetime import datetime as dt
import os
import pytz
from pywintypes import Time
import shutil
from win32file import SetFileTime, CreateFile, CloseHandle
from win32file import GENERIC_WRITE, FILE_SHARE_WRITE
from win32file import OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL





parser = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(
        ", ".join(__authors__), __date__)
)
parser.add_argument("source", help="Source file")
parser.add_argument("dest", help="Destination directory or file")
parser.add_argument("--timezone", help="Timezone of the file's timestamp",
                    choices=['EST5EDT', 'CST6CDT', 'MST7MDT', 'PST8PDT'],
                    required=True)
args = parser.parse_args()

source = os.path.abspath(args.source)
if os.sep in args.source:
    src_file_name = args.source.split(os.sep, 1)[1]
else:
    src_file_name = args.source

dest = os.path.abspath(args.dest)
tz = pytz.timezone(args.timezone)

shutil.copy2(source, dest)
if os.path.isdir(dest):
    dest_file = os.path.join(dest, src_file_name)
else:
    dest_file = dest

created = dt.fromtimestamp(os.path.getctime(source))
created = Time(tz.localize(created))
modified = dt.fromtimestamp(os.path.getmtime(source))
modified = Time(tz.localize(modified))
accessed = dt.fromtimestamp(os.path.getatime(source))
accessed = Time(tz.localize(accessed))

print("Source\n======")
print("Created:  {}\nModified: {}\nAccessed: {}".format(
    created, modified, accessed))

handle = CreateFile(dest_file, GENERIC_WRITE, FILE_SHARE_WRITE,
                    None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
SetFileTime(handle, created, accessed, modified)
CloseHandle(handle)

created = tz.localize(dt.fromtimestamp(os.path.getctime(dest_file)))
modified = tz.localize(dt.fromtimestamp(os.path.getmtime(dest_file)))
accessed = tz.localize(dt.fromtimestamp(os.path.getatime(dest_file)))
print("\nDestination\n===========")
print("Created:  {}\nModified: {}\nAccessed: {}".format(
    created, modified, accessed))
