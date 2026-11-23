import pandas as pd

from config import PROSPECT_LADDERS
from metrics.prospect_model import backtest

TABLE = "data/prospect_table.parquet"


def main():
    table = pd.read_parquet(TABLE)
    for target in PROSPECT_LADDERS:
        print(target)
        print(backtest(table, target).round(3))


if __name__ == "__main__":
    main()
