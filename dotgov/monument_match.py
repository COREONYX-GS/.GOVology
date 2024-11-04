import pandas as pd
from fuzzywuzzy import fuzz, process

monuments_file_path = 'data/US National Monuments.xlsx'

monuments_xlsx = pd.ExcelFile(monuments_file_path)
monuments_df_full = monuments_xlsx.parse('Sheet1')

federal_domains_df = pd.read_csv('data/federal-domains.csv')

matches = []

for monument in monuments_df_full['Monument Name']:
    ## Note: returns a tuple with [0] as the best matched domain, [1] as it's score and [2] as the index of the matched domain in the federal_domains_df
    m1 = process.extractOne(monument, federal_domains_df['Domain name'], scorer=fuzz.partial_ratio, score_cutoff=40)
    m2 = process.extractOne(monument, federal_domains_df['Domain name'], scorer=fuzz.token_set_ratio, score_cutoff=40)

    matches.append({
        'Monument Name': monument,
        'Partial_Domain': m1[0],
        'Partial_Score': m1[1],
        'Token_Domain': m2[0],
        'Token_Score': m2[1]
    })

# Convert matches to DataFrame for easier inspection and display
monument_domain_matches_df = pd.DataFrame(matches)

# Display the matches to the user
# tools.display_dataframe_to_user(name="Monument Domain Names", dataframe=monument_domain_matches_df)

print(monument_domain_matches_df)
# Save the matches to a CSV file
monument_domain_matches_df.to_excel('data/monument_domain_matches.xlsx', index=False)