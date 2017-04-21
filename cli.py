import argparse


parser = argparse.ArgumentParser(
    description='NPPES database and file handler script.')

parser.add_argument(
    '--fullreset', help='Not supported.', action='store_true', default=False)

parser.add_argument('--v', help='Verbose mode',
                    action='store_true', default=False)
parser.add_argument('--update', type=float, help='Set days till update.', default=7.0)

parser.add_argument('--deactivate', help='Run Deactivation File.')

print parser.parse_args()
