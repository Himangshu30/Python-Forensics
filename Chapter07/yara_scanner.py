from __future__ import print_function
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
import csv
import yara




def process_directory(yrules, folder_path):
    match_info = []
    for root, _, files in os.walk(folder_path):
        for entry in files:
            file_entry = os.path.join(root, entry)
            match_info += process_file(yrules, file_entry)
    return match_info


def process_file(yrules, file_path):
    match = yrules.match(file_path)
    match_info = []
    for rule_set in match:
        for hit in rule_set.strings:
            match_info.append({
                'file_name': file_path,
                'rule_name': rule_set.rule,
                'rule_tag': ",".join(rule_set.tags),
                'hit_offset': hit[0],
                'rule_string': hit[1],
                'hit_value': hit[2]
            })
    return match_info


def write_csv(outfile, fieldnames, data):
    with open(outfile, 'w', newline="") as open_outfile:
        csvfile = csv.DictWriter(open_outfile, fieldnames)
        csvfile.writeheader()
        csvfile.writerows(data)


def write_stdout(columns, match_info):
    for entry in match_info:
        for col in columns:
            print("{}: {}".format(col, entry[col]))
        print("=" * 30)


def main(yara_rules, path_to_scan, output):
    if os.path.isdir(yara_rules):
        yrules = yara.compile(yara_rules)
    else:
        yrules = yara.compile(filepath=yara_rules)

    if os.path.isdir(path_to_scan):
        match_info = process_directory(yrules, path_to_scan)
    else:
        match_info = process_file(yrules, path_to_scan)

    columns = ['rule_name', 'hit_value', 'hit_offset', 'file_name',
               'rule_string', 'rule_tag']

    if output is None:
        write_stdout(columns, match_info)
    else:
        write_csv(output, columns, match_info)


if __name__ == '__main__':
    parser = ArgumentParser(
        description=__description__,
        formatter_class=ArgumentDefaultsHelpFormatter,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument(
        'yara_rules',
        help="Path to Yara rule to scan with. May be file or folder path.")
    parser.add_argument(
        'path_to_scan',
        help="Path to file or folder to scan")
    parser.add_argument(
        '--output',
        help="Path to output a CSV report of scan results")
    args = parser.parse_args()

    main(args.yara_rules, args.path_to_scan, args.output)
