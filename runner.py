

import web_parser
import csvParser
import db_dev as db

col_name_map = {'Provider License Number_1': 'LicenseNumber1',
                'Provider Organization Name (Legal Business Name)': 'Name',
                'Is Organization Subpart': 'IsOrganizationSubpart',
                'Authorized Official Credential Text': 'AuthorizedOfficialCredential',
                'Provider Second Line Business Mailing Address': 'SecondLineMailingAddress',
                'Authorized Official Last Name': 'AuthorizedOfficialLastName',
                'Authorized Official First Name': 'AuthorizedOfficialFirstName',
                'Provider Business Mailing Address Postal Code': 'MailingAddressPostalCode',
                'Provider Business Practice Location Address City Name': 'PracticeAddressCity',
                'Is Sole Proprietor': 'IsSoleProprietor',
                'Authorized Official Telephone Number': 'AuthorizedOfficialTelephone',
                'Provider Business Mailing Address Country Code (If outside U.S.)': 'MailingAddressCountryCode',
                'Provider Other Organization Name': 'OtherName',
                'Provider Business Practice Location Address State Name': 'PracticeAddressState',
                'Provider Business Mailing Address Telephone Number': 'MailingAddressTelephone',
                'Provider Business Mailing Address Fax Number': 'MailingAddressFax',
                'Provider First Line Business Mailing Address': 'FirstLineMailingAddress',
                'Authorized Official Title or Position': 'AuthorizedOfficialTitle',
                'Healthcare Provider Taxonomy Code_1': 'TaxonomyCode1',
                'Provider Business Practice Location Address Postal Code': 'PracticeAddressPostalCode',
                'NPI Deactivation Date': 'DeactivationDate',
                'Provider First Line Business Practice Location Address': 'FirstLinePracticeAddress',
                'Provider Second Line Business Practice Location Address': 'SecondLinePracticeAddress',
                'NPI': 'NPI',
                'Provider Business Practice Location Address Telephone Number': 'PracticeAddressTelephone',
                'Provider Business Mailing Address City Name': 'MailingAddressCity',
                'Provider Business Practice Location Address Fax Number': 'PracticeAddressFax',
                'Provider Other Organization Name Type Code': 'OtherNameTypeCode',
                'Provider Business Mailing Address State Name': 'MailingAddressState',
                'Provider License Number State Code_1': 'LicenseStateCode1',
                'Provider Business Practice Location Address Country Code (If outside U.S.)': 'PracticeAddressCountryCode',
                'Healthcare Provider Primary Taxonomy Switch_1': 'TaxonomySwitch1'}


def main():
    print 'Get dl links'
    dl_links = web_parser.get_download_links()
    print 'Retrieve csv'
    csv_name = web_parser.retrieve_csv_file(dl_links[0])
    print 'parse csv'
    up = csvParser.CSV(csv_name)
    print 'load headers'
    headers = csvParser.loadHeaders('header.csv')
    print 'connect to db'
    curs = db.init_cursor()
    print 'update db'
    db.update(curs, col_name_map, headers, up)
    curs.close()

if __name__ == '__main__':
    main()
