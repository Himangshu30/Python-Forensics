from __future__ import print_function
import argparse
import csv
import os
import sqlite3
import sys




def main(database, out_directory):
    print("[+] Connecting to SQLite database")
    conn = sqlite3.connect(database)
    c = conn.cursor()

    print("[+] Querying IEF database for list of all tables to extract")
    c.execute("select * from sqlite_master where type='table'")
    # Remove tables that start with "_" or end with "_DATA"
    tables = [x[2] for x in c.fetchall() if not x[2].startswith('_') and
              not x[2].endswith('_DATA')]

    print("[+] Dumping {} tables to CSV files in {}".format(
        len(tables), out_directory))
    for table in tables:
        c.execute("pragma table_info('{}')".format(table))
        table_columns = [x[1] for x in c.fetchall()]
        c.execute("select * from '{}'".format(table))
        table_data = c.fetchall()

        csv_name = table + '.csv'
        csv_path = os.path.join(out_directory, csv_name)
        print('[+] Writing {} table to {} CSV file'.format(table,
                                                           csv_name))
        with open(csv_path, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(table_columns)
            csv_writer.writerows(table_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("IEF_DATABASE", help="Input IEF database")
    parser.add_argument("OUTPUT_DIR", help="Output DIR")
    args = parser.parse_args()

    if not os.path.exists(args.OUTPUT_DIR):
        os.makedirs(args.OUTPUT_DIR)

    if os.path.exists(args.IEF_DATABASE) and \
            os.path.isfile(args.IEF_DATABASE):
        main(args.IEF_DATABASE, args.OUTPUT_DIR)
    else:
        print("[-] Supplied input file {} does not exist or is not a "
              "file".format(args.IEF_DATABASE))
        sys.exit(1)
