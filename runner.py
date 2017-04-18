

import web_parser, csvParser

def main():
    dl_links = web_parser.get_download_links()
    csv_name = web_parser.retrieve_csv_file(dl_links[0])
    gener = csvParser.get_generator(csv_name)
    print 'Got generator for %s from %s: ' % (csv_name, dl_links[0]), gener

if __name__ == '__main__':
    main()

