

import web_parser, csvParser

def main():
    dl_links = web_parser.get_download_links()
    csv_name = web_parser.retrieve_csv_file(dl_links[0])
    up = csvParser.CSV(csv_name)
    headers = csvParser.loadHeaders('header.csv')
    print {'headers':headers, 'CSV':up, 'link':dl_links[0]}
if __name__ == '__main__':
    main()

