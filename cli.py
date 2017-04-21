import argparse
import sys


parser = argparse.ArgumentParser(
    description='NPPES database and file handler script.')
#Add Option for full reset
parser.add_argument(
    '--fullreset', help='Not supported.', action='store_true', default=False)
#Option for Verbose mode
parser.add_argument('--v', help='Verbose mode',
                    action='store_true', default=False)
#Add Option for Days till Update
parser.add_argument('--update', type=float, help='Set days till update.', default=7.0)
#Add Option to Run Deactivation File
parser.add_argument('--deactivate', help='Run Deactivation File.')
#Setting args to the arguments to Run
args = parser.parse_args()
#write the file on stdout
#ex: write(get_download_links) from web_parser.py
#sys.stdout.write()
