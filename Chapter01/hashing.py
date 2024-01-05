from __future__ import print_function
import argparse
import hashlib
import os


available_algorithms = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512
}

parser = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(", ".join(__authors__), __date__)
)
parser.add_argument("FILE_NAME", help="Path of file to hash")
parser.add_argument("ALGORITHM", help="Hash algorithm to use",
                    choices=sorted(available_algorithms.keys()))
args = parser.parse_args()

input_file = args.FILE_NAME
hash_alg = args.ALGORITHM

file_name = available_algorithms[hash_alg]()
abs_path = os.path.abspath(input_file)
file_name.update(abs_path.encode())

print("The {} of the filename is: {}".format(
    hash_alg, file_name.hexdigest()))

file_content = available_algorithms[hash_alg]()
with open(input_file, 'rb') as open_file:
    buff_size = 1024
    buff = open_file.read(buff_size)

    while buff:
        file_content.update(buff)
        buff = open_file.read(buff_size)

print("The {} of the content is: {}".format(
    hash_alg, file_content.hexdigest()))
