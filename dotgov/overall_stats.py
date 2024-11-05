import sys
import pandas as pd


if __name__ == "__main__":
    FILE = sys.argv[1] if len(sys.argv) > 1 else 'data/current-full.csv'
    
    df = pd.read_csv(FILE)

    # Aggregate statistics
    total_entries = len(df)

    # Grouping by domain type
    domain_type_counts = df['Domain type'].value_counts()

    print(domain_type_counts)

    print(total_entries)