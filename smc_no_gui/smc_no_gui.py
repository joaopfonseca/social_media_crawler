import argparse

parser = argparse.ArgumentParser(description='Description of what the program does here')
parser.add_argument('-creds_id', type=int, nargs=1, required=True,
                    help='ID (number) of the set of credentials to use. You can update this list in the file creds.py')
parser.add_argument('-keyword', type=str, nargs=1, required=True,
                    help='Keyword to crawl')

args = parser.parse_args()
keyword   = args.keyword[0].strip()
kw_number = args.creds_id[0]

import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

print('#---------------------------------------------------------------------------------------------------#')
print('#----------------------------------------- Initializing... -----------------------------------------#')
print('#---------------------------------------------------------------------------------------------------#')

import src as wc
wc.auto_crawler(keyword, kw_number)
