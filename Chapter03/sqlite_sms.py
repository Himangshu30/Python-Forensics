from __future__ import print_function
import argparse
import csv
import os
import sqlite3
import sys



def main(database, out_csv):
    print("[+] Attempting connection to {} database".format(database))
    if not os.path.exists(database) or not os.path.isfile(database):
        print("[-] Database does not exist or is not a file")
        sys.exit(1)

    # Connect to SQLite Database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Query DB for Column Names and Data of Message Table
    c.execute("pragma table_info(message)")
    table_data = c.fetchall()
    columns = [x[1] for x in table_data]

    c.execute("select * from message")
    message_data = c.fetchall()

    print("[+] Writing Message Content to {}".format(out_csv))
    write_csv(out_csv, columns, message_data)


def write_csv(output, cols, msgs):
    with open(output, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(cols)
        csv_writer.writerows(msgs)


if __name__ == '__main__':
    # Command-line Argument Parser
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("SQLITE_DATABASE", help="Input SQLite database")
    parser.add_argument("OUTPUT_CSV", help="Output CSV File")
    args = parser.parse_args()

    directory = os.path.dirname(args.OUTPUT_CSV)
    if directory != '' and not os.path.exists(directory):
        os.makedirs(directory)

    main(args.SQLITE_DATABASE, args.OUTPUT_CSV)
