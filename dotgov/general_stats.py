import sys
import pandas as pd

def to_markdown(data):
    def format_series(series, title):
        md = f"### {title}\n\n"
        md += series.to_markdown()
        md += "\n\n"
        return md

    md_output = "# General Statistics\n\n"
    md_output += "## Summary Statistics\n\n"
    md_output += f"**Total Entries:** `{data['Total Entries']}`\n"
    md_output += f"**Single Domain Agencies:** `{len(data['Agency Counts - Single Domain'])}`\n\n"
    md_output += format_series(data['Type Counts'], "Branch Counts")
    
    md_output += "## Top Domain Holders\n\n"
    top_quartile_threshold = data['Agency Counts - Top 10 Domain Holders'].quantile(0.75)
    top_quartile_agencies = data['Agency Counts - Top 10 Domain Holders'][data['Agency Counts - Top 10 Domain Holders'] > top_quartile_threshold]
    md_output += format_series(top_quartile_agencies, f"Agency Counts - Top Quartile Domain Holders `>{top_quartile_threshold}`")
    
    md_output += "## Top State Statistics\n\n"
    md_output += format_series(data['State Counts'], "State Counts")
    
    md_add = missing_states(aggregate_stats)
    if md_add:
        md_output += "### State Strangeness\n\n"
        md_output += md_add

    return(md_output)

def missing_states(data, md_output=""):
    # List of all US states
    all_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
    }
    states_with_domains = set(data['State Counts'].index)
    
    not_in_states_list = states_with_domains - all_states
    if not_in_states_list:
        md_output += "#### Sites not listed in the states list\n\n"
        
        md_output += "| State | Site |\n"
        md_output += "|------:|-----:|\n"
        for state in not_in_states_list:
            sites = data['data'][ data['data']['State'] == state]['Domain name'].tolist()
            for site in sites:
                md_output += f"| {state} | {site} |\n"
        md_output += "\n"

    states_missing_domains = all_states - states_with_domains
    if states_missing_domains:
        md_output += "#### States Missing Domain Names\n"
        md_output += "[" + ", ".join(sorted(states_missing_domains)) + "]" 
    
    return md_output

if __name__ == "__main__":
    FILE = sys.argv[1] if len(sys.argv) > 1 else 'data/federal-domains.csv'
    df = pd.read_csv(FILE)

    # Aggregate statistics
    total_entries = len(df)

    # Grouping by domain type
    domain_type_counts = df['Domain type'].value_counts()

    # Grouping by state
    state_counts = df['State'].value_counts()

    # Grouping by agency
    agency_counts = df['Agency'].value_counts()

    # Filter to get only the entries with a count of 1
    agency_singletons = agency_counts[agency_counts == 1]

    aggregate_stats = {
        "data": df,
        "Total Entries": total_entries,
        "Type Counts": domain_type_counts,
        "State Counts": state_counts,
        "Agency Counts - Top 10 Domain Holders": agency_counts,
        "Agency Counts - Single Domain": agency_singletons
    }

    print( to_markdown(aggregate_stats) )

