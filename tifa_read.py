from sas7bdat import SAS7BDAT
with SAS7BDAT('TIFA_2010.sas7bdat') as f:
    for row in f:
        print row