import argparse
import sys

parser = argparse.ArgumentParser(
    description='NPPES database and file handler script.')

sp = parser.add_subparsers()

sp_reset = sp.add_parser('reset', help='Resets AutoCross')

sp_auto = sp.add_parser('auto', help='Runs AutoCross Automatically')

#Setting args to the arguments to Run
args = parser.parse_args()
print(parser)
