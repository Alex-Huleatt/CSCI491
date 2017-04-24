class CSV2():
    def __init__(self, fname):
        self.fname = fname
        self.f = open(fname)

    def __del__(self):
        self.f.close()

    def __iter__(self):
        skip = True
        for k in self.f.readlines():
            if skip:
                skip=False
                continue
            yield k.replace('\n', '').replace('"','').split(',')

def loadHeaders(fname):
    headers = open(fname).read().replace('"','').replace('\n','').split(',')
    return headers

def _test():
    head = loadHeaders('header.csv')
    assert len(head)== 329, 'Unexpected number of columns in header.csv'

    test = CSV2('testcsv.csv')
    i = 0
    for k in test:
        i += 1
    assert i == 99, 'Unexpected number of lines read in testcsv %s' % i




