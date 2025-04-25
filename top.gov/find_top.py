import os
import glob
import pandas as pd

def find_gov_domains(data_dir='top.gov/data', filter_df=None):
    # grab all CSV files in the top level of data_dir
    pattern = os.path.join(data_dir, '*.csv')
    for filepath in sorted(glob.glob(pattern)):
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            print(f"⚠️ Could not read {filepath}: {e}")
            continue

        # ensure the column exists
        if 'domain' not in df.columns:
            print(f"⚠️ Skipping {os.path.basename(filepath)} (no 'domain' column)")
            continue

        # find all entries containing '.gov'
        mask = df['domain'].astype(str).str.contains(r'\.gov', regex=True, na=False)
        gov_domains = df.loc[mask, 'domain']

        if not gov_domains.empty and filter_df is not None:
            # apply additional filtering if provided
            gov_domains = gov_domains[gov_domains.isin(filter_df[ filter_df['Domain type'] == 'Federal - Executive' ]['Domain name'])]

        if not gov_domains.empty:
            print(f"{os.path.basename(filepath)} .gov")
            for domain in gov_domains:
                print(f"  {domain}")
            print()  # blank line between files
        
        continue ## unnecesary, but allows for adding a breakpoint for debugging

if __name__ == '__main__':
    df=pd.read_csv("data/federal-domains.csv")
    
    find_gov_domains(data_dir='top.gov/data', filter_df=df)
    
    print ("Done!")
