from __future__ import print_function
import argparse
import csv
import json
import os
import subprocess
import sys



def main(domain_file, output):
    domains = set()
    with open(domain_file) as infile:
        for line in infile:
            domains.add(line.strip())
    json_data = query_domains(domains)
    write_csv(json_data, output)


def query_domains(domains):
    json_data = []
    print("[+] Querying {} domains/IPs using PassiveTotal API".format(
        len(domains)))
    for domain in domains:
        if "https://" in domain:
            domain = domain.replace("https://", "")
        elif "http://" in domain:
            domain = domain.replace("http://", "")

        proc = subprocess.Popen(
            ["pt-client", "pdns", "-q", domain], stdout=subprocess.PIPE)
        results, err = proc.communicate()
        result_json = json.loads(results.decode())
        if "message" in result_json:
            if "quota_exceeded" in result_json["message"]:
                print("[-] API Search Quota Exceeded")
                continue

        result_count = result_json["totalRecords"]

        print("[+] {} results for {}".format(result_count, domain))
        if result_count == 0:
            pass
        else:
            json_data.append(result_json["results"])

    return json_data


def write_csv(data, output):
    if data == []:
        print("[-] No output results to write")
        sys.exit(2)

    print("[+] Writing output for {} domains/IPs with "
          "results to {}".format(len(data), output))
    field_list = ["value", "firstSeen", "lastSeen", "collected",
                  "resolve", "resolveType", "source", "recordType",
                  "recordHash"]

    with open(output, "w", newline="") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=field_list)
        csv_writer.writeheader()
        for result in data:
            for dictionary in result:
                csv_writer.writerow(dictionary)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("INPUT_DOMAINS",
                        help="Text File containing Domains and/or IPs")
    parser.add_argument("OUTPUT_CSV",
                        help="Output CSV with lookup results")
    args = parser.parse_args()

    directory = os.path.dirname(args.OUTPUT_CSV)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(args.INPUT_DOMAINS) and \
            os.path.isfile(args.INPUT_DOMAINS):
        main(args.INPUT_DOMAINS, args.OUTPUT_CSV)
    else:
        print(
            "[-] Supplied input file {} does not exist or is not a "
            "file".format(args.INPUT_DOMAINS))
        sys.exit(1)
