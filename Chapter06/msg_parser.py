from __future__ import print_function
from argparse import ArgumentParser
import os
import win32com.client
import pywintypes




def extract_msg_body(msg, out_dir):
    # Extract HTML Data
    html_data = msg.HTMLBody.encode('cp1252')
    outfile = os.path.join(out_dir, os.path.basename(args.MSG_FILE))
    open(outfile + ".body.html", 'wb').write(html_data)
    print("Exported: {}".format(outfile + ".body.html"))

    # Extract plain text
    body_data = msg.Body.encode('cp1252')
    open(outfile + ".body.txt", 'wb').write(body_data)
    print("Exported: {}".format(outfile + ".body.txt"))


def extract_attachments(msg, out_dir):
    attachment_attribs = [
        'DisplayName', 'FileName', 'PathName', 'Position', 'Size'
    ]
    i = 1  # Attachments start at 1
    while True:
        try:
            attachment = msg.Attachments(i)
        except pywintypes.com_error:
            break

        print("\nAttachment {}".format(i))
        print("=" * 15)
        for entry in attachment_attribs:
            print('{}: {}'.format(entry, getattr(attachment, entry,
                                                 "N/A")))
        outfile = os.path.join(os.path.abspath(out_dir),
                               os.path.split(args.MSG_FILE)[-1])
        if not os.path.exists(outfile):
            os.makedirs(outfile)
        outfile = os.path.join(outfile, attachment.FileName)
        attachment.SaveAsFile(outfile)
        print("Exported: {}".format(outfile))
        i += 1


def display_msg_attribs(msg):
    # Display Message Attributes
    attribs = [
        'Application', 'AutoForwarded', 'BCC', 'CC', 'Class',
        'ConversationID', 'ConversationTopic', 'CreationTime',
        'ExpiryTime', 'Importance', 'InternetCodePage', 'IsMarkedAsTask',
        'LastModificationTime', 'Links', 'OriginalDeliveryReportRequested',
        'ReadReceiptRequested', 'ReceivedTime', 'ReminderSet',
        'ReminderTime', 'ReplyRecipientNames', 'Saved', 'Sender',
        'SenderEmailAddress', 'SenderEmailType', 'SenderName', 'Sent',
        'SentOn', 'SentOnBehalfOfName', 'Size', 'Subject',
        'TaskCompletedDate', 'TaskDueDate', 'To', 'UnRead'
    ]
    print("\nMessage Attributes")
    print("==================")
    for entry in attribs:
        print("{}: {}".format(entry, getattr(msg, entry, 'N/A')))


def display_msg_recipients(msg):
    # Display Recipient Information
    recipient_attrib = [
        'Address', 'AutoResponse', 'Name', 'Resolved', 'Sendable'
    ]
    i = 1
    while True:
        try:
            recipient = msg.Recipients(i)
        except pywintypes.com_error:
            break

        print("\nRecipient {}".format(i))
        print("=" * 15)
        for entry in recipient_attrib:
            print("{}: {}".format(entry, getattr(recipient, entry, 'N/A')))
        i += 1


def main(msg_file, output_dir):
    mapi = win32com.client.Dispatch(
        "Outlook.Application").GetNamespace("MAPI")
    msg = mapi.OpenSharedItem(os.path.abspath(args.MSG_FILE))
    display_msg_attribs(msg)
    display_msg_recipients(msg)
    extract_msg_body(msg, output_dir)
    extract_attachments(msg, output_dir)


if __name__ == '__main__':
    parser = ArgumentParser(
        description=__description__,
        epilog="Developed by {} on {}".format(
            ", ".join(__authors__), __date__)
    )
    parser.add_argument("MSG_FILE", help="Path to MSG file")
    parser.add_argument("OUTPUT_DIR", help="Path to output folder")
    args = parser.parse_args()
    out_dir = args.OUTPUT_DIR
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    main(args.MSG_FILE, args.OUTPUT_DIR)
