import csv

class CSV2():
    def __init__(self, fname):
        self.fname = fname
        self.f = csv.reader(open(fname), delimiter=',')

    def __iter__(self):
        skip = True
        for k in self.f:
            if skip: #we skip the first line, containing header
                skip = False
                continue
            yield k

def loadHeaders(fname):
    headers = open(fname).read().replace('"','').replace('\n','').split(',')
    return headers
