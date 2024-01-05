from __future__ import print_function
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime as dt
from datetime import timedelta



class ParseDate(object):
    def __init__(self, date_value, source, data_type):
        self.date_value = date_value
        self.source = source
        self.data_type = data_type
        self.timestamp = None

    def run(self):
        if self.source == 'unix-epoch':
            self.parse_unix_epoch()
        elif self.source == 'unix-epoch-ms':
            self.parse_unix_epoch(True)
        elif self.source == 'windows-filetime':
            self.parse_windows_filetime()

    @classmethod
    def get_supported_formats(cls):
        return ['unix-epoch', 'unix-epoch-ms', 'windows-filetime']

    def parse_unix_epoch(self, milliseconds=False):
        if self.data_type == 'hex':
            conv_value = int(self.date_value)
            if milliseconds:
                conv_value = conv_value / 1000.0
        elif self.data_type == 'number':
            conv_value = float(self.date_value)
            if milliseconds:
                conv_value = conv_value / 1000.0
        else:
            print("Unsupported data type '{}' provided".format(
                self.data_type))
            sys.exit('1')

        ts = dt.fromtimestamp(conv_value)
        self.timestamp = ts.strftime('%Y-%m-%d %H:%M:%S.%f')

    def parse_windows_filetime(self):
        if self.data_type == 'hex':
            microseconds = int(self.date_value, 16) / 10.0
        elif self.data_type == 'number':
            microseconds = float(self.date_value) / 10
        else:
            print("Unsupported data type '{}' provided".format(
                self.data_type))
            sys.exit('1')

        ts = dt(1601, 1, 1) + timedelta(microseconds=microseconds)
        self.timestamp = ts.strftime('%Y-%m-%d %H:%M:%S.%f')


if __name__ == '__main__':
    parser = ArgumentParser(
        description=__description__,
        formatter_class=ArgumentDefaultsHelpFormatter,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("date_value", help="Raw date value to parse")
    parser.add_argument("source", help="Source format of date",
                        choices=ParseDate.get_supported_formats())
    parser.add_argument("type", help="Data type of input value",
                        choices=('number', 'hex'), default='int')
    args = parser.parse_args()

    date_parser = ParseDate(args.date_value, args.source, args.type)
    date_parser.run()
    print(date_parser.timestamp)
