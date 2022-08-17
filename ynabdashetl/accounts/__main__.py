import argparse

from ynabdashetl.core import ExtractJob

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--extract_date", help="extract date of data to load", type=str)
    args = parser.parse_args()
    
    job = ExtractJob('accounts', args.extract_date)
    job.run()
