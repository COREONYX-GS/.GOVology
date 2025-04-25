import os
import glob
import pandas as pd

def find_bottom_gov_domains(top_df, filter_df):

    # find all entries containing '.gov'
    mask = top_df['domain'].astype(str).str.contains(r'\.gov$', regex=True, na=False)
    top_gov_domains = top_df.loc[mask, 'domain']

    bottom_gov_domains = filter_df[~filter_df['Domain name'].isin(top_gov_domains)]
    bottom_gov_domains = bottom_gov_domains[ bottom_gov_domains['Domain type'] == 'Federal - Executive' ]
    bottom_gov_domains = bottom_gov_domains.sort_values(by='Domain name', ascending=True)

    return bottom_gov_domains

if __name__ == '__main__':
    TOP_FILENAME = "top.gov/data/cloudflare-radar_top-1000000-domains_20250414-20250421.csv"
    filter_df=pd.read_csv("data/federal-domains.csv")
    top_df=pd.read_csv(TOP_FILENAME)

    bottom_gov_domains = find_bottom_gov_domains(top_df, filter_df=filter_df)

    if not bottom_gov_domains.empty:
        print(f"{TOP_FILENAME}")
    
        for domain in bottom_gov_domains['Domain name']:
            print(f"  {domain}")
        print()  # blank line between files
    
    print ("Done!")
