import pandas as pd

if __name__ == "__main__":

    # Load the CSV file containing federal domains
    federal_domains_df = pd.read_csv('data/federal-domains.csv')
    cisa_domains = set(federal_domains_df['Domain name'].str.lower().str.strip())

    # Load the Excel file and the specified sheet, extracting the 'target_url_domain' column
    #excel_df = pd.read_excel("data/GSA TTS's Site Scanning Program.xlsx", sheet_name='2024-06-02')
    #tts_domains = set(excel_df['target_url_domain'].str.lower().str.strip())

    scanning_df = pd.read_csv('data/tts-weekly-snapshot-all.csv')
    tts_domains = set(scanning_df['target_url_domain'].str.lower().str.strip())
    
    # Find domains unique to each file
    unique_to_tts = tts_domains - cisa_domains
    unique_to_cisa = cisa_domains - tts_domains

    # Output results
    print(f"{ len(unique_to_tts) } Domains unique to TTS's Site Scanning Program:")
    for domain in unique_to_tts:
        # if not ".mil" in domain: print(domain)
        print(domain)

    print(f"{ len(unique_to_cisa) } Domains unique to the CISA .gov export:")
    for domain in unique_to_cisa:
        print(domain)

    print("\n\ndone")
