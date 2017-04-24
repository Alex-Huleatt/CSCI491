from bs4 import BeautifulSoup
import urllib
import re
import zipfile
import os
from os.path import join  # For convenience
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
zip_regex = join('.','(NPPES_Data_Dissemination_' + '.*' + '_Weekly\.zip)')

monthly_regex = 'NPPES_Data_Dissemination_\w*_\d*\.zip'
deactiv_regex = join('.','(NPPES_Deactivated_NPI_Report_\d+\.zip)')

def get_download_links(reg=zip_regex):
    '''This returns all download links for weekly update files.'''
    try:
        r = urllib.urlopen(link_page).read()
        soup = BeautifulSoup(r, 'html.parser')
        links = soup.find_all('a', href=True)

        pattern = re.compile(reg)

        weekly_links = []
        for l in links:
            path = l['href']
            m = pattern.match(path)
            if m:
                weekly_links.append(download_page + m.groups()[0])
        print weekly_links
        return weekly_links
    except Exception as e: #pragma: no cover
        print 'Error getting download links.'
        raise e



'''
this regex is mainly used to avoid getting the header csv file
Put out here in case of future changes.

Should match *only* the update csv file.
'''
csv_regex = 'npidata_[\\d_\-]*\\.csv'
xslx_regex = '.*\.xlsx'

def retrieve_csv_file(url, reg=csv_regex):
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
    p = re.compile(reg)
    print reg
    fname = ''
    for _, _, files in os.walk(week_dir):
        for f in files:
            if p.match(f):
                from_dir = join(week_dir, f)
                to_dir = join('.', f)
                os.rename(from_dir, to_dir)
                fname = f
    shutil.rmtree(week_dir)  # delete temporary dir.
    
    assert os.path.isfile(fname), 'Expected file %s' % fname #pragma: no cover
    return fname

def _test():
    get_download_links()