from bs4 import BeautifulSoup
import urllib
import re
import zipfile
import os
from os.path import join
import shutil

'''
Change this if the download page ever changed.
'''
download_page = 'http://download.cms.gov/nppes/'
link_page = download_page + 'NPI_Files.html'

'''
This would be prone to change if the website ever changed.
This would require modification to continue to function.
'''
zip_regex = join('.', '(NPPES_Data_Dissemination_' + '.*' + '_Weekly.zip)')


def get_download_links():
    '''This returns all download links for weekly update files.'''
    r = urllib.urlopen(link_page).read()
    soup = BeautifulSoup(r, 'html.parser')
    links = soup.find_all('a', href=True)

    pattern = re.compile(zip_regex)

    weekly_links = []
    for l in links:
        path = l['href']
        m = pattern.match(path)
        if m:
            weekly_links.append(download_page + m.groups()[0])

    return weekly_links


'''
this regex is mainly used to avoid getting the header csv file
Put out here in case of future changes.

Should match *only* the update csv file.
'''
csv_regex = 'npidata_[\\d_\-]*\\.csv'


def retrieve_csv_file(url):
    '''
    This function downloads, upzips, and grabs the desired csv file.
    Theile is placed at the working directory and the filename is returned.
    All extraneous files/folders are deleted
    '''
    week_dir = join('.', 'week')
    urllib.urlretrieve(url, 'week.zip')
    zip_ref = zipfile.ZipFile('week.zip', 'r')
    zip_ref.extractall(week_dir)
    zip_ref.close()
    os.remove('week.zip')
    p = re.compile(csv_regex)
    fname = ''
    for _, _, files in os.walk(week_dir):
        for f in files:
            if p.match(f):
                from_dir = join(week_dir, f)
                to_dir = join('.', f)
                os.rename(from_dir, to_dir)
                fname = f
    shutil.rmtree(week_dir)
    return fname


if __name__ == '__main__':
    links = get_download_links()
    retrieve_csv_file(links[0])
