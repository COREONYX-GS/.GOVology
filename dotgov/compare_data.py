import os
import sys
import pandas as pd

PREV_FILE = os.getenv("PREV_FILE", "data/previous_federal-domains.csv")
CURR_FILE = os.getenv("CURR_FILE", "data/current_federal-domains.csv")

# Load the current and previous versions of the file
current_df = pd.read_csv(CURR_FILE)
previous_df = pd.read_csv(PREV_FILE)

# Identify the differences
added_domains = current_df[~current_df['Domain name'].isin(previous_df['Domain name'])]
deleted_domains = previous_df[~previous_df['Domain name'].isin(current_df['Domain name'])]

if not added_domains.empty:
    print(f"### Added Domains (**{len(added_domains)}**):")
    print(added_domains.to_markdown(index=False))

if not deleted_domains.empty:
    print(f"### Deleted Domains (**{len(deleted_domains)}**):")
    print(deleted_domains.to_markdown(index=False))
