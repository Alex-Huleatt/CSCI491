import argparse

parser = argparse.ArgumentParser(
    description='NPPES database and file handler script.')
#Add Option for full reset
parser.add_argument(
    '--fullreset', help='Not supported.', action='store_true', default=False)
#Option for Verbose mode
parser.add_argument('--v', help='Verbose mode',
                    action='store_true', default=False)
#Add Option for Downloading full data
parser.add_argument('--df', type=float, help='Download full data', default=7.0)
#Add Option to Manually download and apply the weekly file
parser.add_argument('--dw', help='Manually download and Apply weekly file')
#Add Option to Import the full data set into Database Schema
parser.add_argument('--i', help='Import into Database Schema', action='store_true', default=True)
#Add Option to Manually download and apply the deactivation file
parser.add_argument('--dd', type=float, help='Download full data', default=7.0)

#Setting args to the arguments to Run
args = parser.parse_args()
#write the file on stdout
#ex: write(get_download_links) from web_parser.py
#sys.stdout.write(get_download_links)
print(parser)



