from openpyxl import load_workbook

def readxlsx(fname):

    wb = load_workbook(filename = fname)
    ws = wb.active
    ls = [] #list of tuples of form (NPI, datestring)
    skip = 2
    for r in ws.rows:
        if skip: #skip first two rows containing header stuff
            skip-=1
            continue
        ls.append((r[0].value, r[1].value))
    return ls