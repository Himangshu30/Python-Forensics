from __future__ import print_function
from argparse import ArgumentParser, FileType
from email import message_from_file
import os
import quopri
import base64




def process_payload(payload):
    print(payload.get_content_type() + "\n" + "=" * len(
        payload.get_content_type()))
    body = quopri.decodestring(payload.get_payload())
    if payload.get_charset():
        body = body.decode(payload.get_charset())
    else:
        try:
            body = body.decode()
        except UnicodeDecodeError:
            body = body.decode('cp1252')

    if payload.get_content_type() == "text/html":
        outfile = os.path.basename(args.EML_FILE.name) + ".html"
        open(outfile, 'w').write(body)
    elif payload.get_content_type().startswith('application'):
        outfile = open(payload.get_filename(), 'wb')
        body = base64.b64decode(payload.get_payload())
        outfile.write(body)
        outfile.close()
        print("Exported: {}\n".format(outfile.name))
    else:
        print(body)


def main(input_file):
    emlfile = message_from_file(input_file)

    # Start with the headers
    for key, value in emlfile._headers:
        print("{}: {}".format(key, value))

    # Read payload
    print("\nBody\n")
    if emlfile.is_multipart():
        for part in emlfile.get_payload():
            process_payload(part)
    else:
        process_payload(emlfile[1])


if __name__ == '__main__':
    parser = ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("EML_FILE",
                        help="Path to EML File", type=FileType('r'))
    args = parser.parse_args()

    main(args.EML_FILE)
