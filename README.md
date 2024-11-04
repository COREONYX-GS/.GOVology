# .GOVology

![.GOVology Logo](static/.govology-logo.png)

Studying Data from the US Government's .gov Domain Registry

Utilizing [the data available](https://get.gov/about/data/) for the .GOV registry as well as [TTS' Site Scanning Program](https://digital.gov/guides/site-scanning/) I've started taking a look at some of the forms and functions that seem to be represented in the data.

Note, this is not my operational repository which has some other ad-hoc analysis that is waiting to be finalized before publishing but I wanted to share the baseline automation for others who might find it interesting.

### Methodology
Right now there's a fairly simple set of automation that (1) downloads the .GOV domain data via GitHub (per the Program's recommendation) and (2) TTS' Site Scanning Data.

Note Site Scanning Data is used more for _ad hoc_ analysis at this time. The .GOV registry data has been useful to see additions, deletions, and updates in near(er) realtime.


### References:
    * **List of National Monuments**: https://geojango.com/pages/list-of-national-monuments
    * **TTS Site Scanning Analysis**: https://github.com/CivicActions/site-evaluation-tools/blob/main/digital.gov-scan-upload.js.md
        - [Direct Link to Spreadsheet](https://docs.google.com/spreadsheets/d/1CsXAzCzghYYwXzGCcrJqrsWpr5f7MbID2Qw6vQvi3sQ/edit?gid=497600811#gid=497600811)