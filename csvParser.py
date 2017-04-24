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

if __name__ == '__main__':
    pass