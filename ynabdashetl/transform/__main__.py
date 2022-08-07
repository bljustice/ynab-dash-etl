import argparse

from ynabdashetl.transform import BudgetTransformJob

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_date", help="start date of data to load", type=str)
    args = parser.parse_args()

    job = BudgetTransformJob(args.start_date)
    job.run()
