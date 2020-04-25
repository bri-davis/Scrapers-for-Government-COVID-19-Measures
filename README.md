# Scrapers for Government COVID-19 Measures

## Overview
This collection of web scrapers collects the information pertaining to government COVID-19-related emergency orders and stores them in CSV files.

## Design Details
### Implementation
This collection of web scrapers uses the BeautifulSoup 4 and requests libraries in order to collect the text from each state in the New England region of the United States. After collecting the text, there are generally 3 elements of information that are scraped. These elements are:

1. Date, or the day that the measure was passed by the government.
2. Description, or the supplied summary of the measure.
3. PDF Link, or the source to the primary text the order.

These elements of information were available and scraped for all 6 of the states in the New England region. The csv files contain these attributes in their columns and the emergency orders in their rows, sorted from most recent to least recent date. Sometimes, more information was available. For example, Vermont and Massachusetts offered Press Release article links and Guidance links. I included these in their respective csv files.
### Pre-processing
In order to ensure consistency between files, the dates and descriptions had to be pre-processed. The dates were written in a variety of forms in the webpages. Using the datetime library, all of these dates were rewritten into mm/dd/yyyy format. 

The descriptions generally needed more intricate processes to extract only the supplied text summaries for the government orders. A common theme across all of the government websites was inconsistent formatting, across both html tabs and the text within. 

The inconsistent html tabs made me innovate solutions that rely less on positioning of tabs in the contents, and cater more to the relative structure of the contents. This approach is perhaps more robust to inconsistencies, but could still break if contents are rearranged. 

The text was cleaned and pre-processed on a case-by-case basis. For example, the regex library was used for scraping Connecticut's website to eliminate excess spaces in the text. Many of the websites also needed their descriptions to be split to only include the description-associated text. For example, I was able to split off any text not related to the emergency order by looking for rare characters such as colons or parentheses, and breaking the text there. This will generally work, unless the website places one of these characters in the body of a summary.
### Testing
By visual inspection, I verified that the scripts are collecting most of the desired data from the websites.
### Requirements
The provided collection of scripts are written in Python 3 and uses the BeautifulSoup 4, requests, datetime, csv, and regex libraries. 

## How to Run
Run the scrapers by running the bash-script on the command-line as follows:

```bash run_scrapers.sh```

Look for the output in the /Outputs folder. I provided data up until Saturday, April 25, 2020 in there already.

## Future Considerations

To anyone interested in going forward with this project, I would recommend the following tasks:

1. Implement a PDF to text translator for the PDFs linked in the csv outputs. Store the text in a new column in the csvs
2. Create web scraping scripts for government measures taken by the other 44 states.
