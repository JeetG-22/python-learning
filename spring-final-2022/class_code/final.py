import requests
import pathlib, csv

URL='https://api.nytimes.com/svc/search/v2/articlesearch.json'
API_KEY='d3ks2vLPz3dCARaV6xhKpie5g8GdPXd7'

china_taiwan_keywords = 'China'
israel_pal_keywords = 'Israel'

facet_fields = 'pub_month'

#6-month time intervals for the year 2023
"""
Reasoning: NYT API was skipping months in 2023 even when there were articles posted
6-month intervals gave back properly returned articles counts for each month
"""
time_intervals = [('20230101', '20230630'), ('20230701', '20231231')]

# Count of articles per month for China/Taiwan
china_taiwan_article_counts = {}

# Count of articles per month for Israel/Palestine
israel_pal_article_counts = {}

for begin_date, end_date in time_intervals: 
    # Define query parameters for each conflict
    china_taiwan_params = {
        'q': china_taiwan_keywords,
        'fq': 'document_type:("article") AND (Taiwan OR Philippines OR Japan OR Strait) AND body:("conflict", "tension", "negotiation", "violence", "war")',
        'begin_date': begin_date,
        'end_date': end_date,
        'facet_fields': facet_fields,
        'facet': 'true',
        'api-key': API_KEY
    }
            
    israel_pal_params = {
        'q': israel_pal_keywords,
        'fq': 'document_type:("article") AND (Hamas OR Palestine OR Gaza) AND body:("conflict", "tension", "negotiation", "violence", "war")',
        'begin_date': begin_date,
        'end_date': end_date,
        'facet_fields': facet_fields,
        'facet': 'true',
        'api-key': API_KEY
    }
    # Make API requests for each conflict
    china_taiwan_response = requests.get(URL, params=china_taiwan_params)
    israel_pal_response = requests.get(URL, params=israel_pal_params)

    #Making sure the response objects returned with a successful status code before moving on
    if(china_taiwan_response.status_code == 200 and israel_pal_response.status_code == 200):
        china_taiwan_response = china_taiwan_response.json()
        israel_pal_response = israel_pal_response.json()
    else:
        break
    
    #Parsing the data to store the article counts per month for both conflicts in a dict
    for data in china_taiwan_response['response']['facets']['pub_month']['terms']:
        month = int(data.get('term'))
        count = int(data.get('count'))
        china_taiwan_article_counts[month] = count
            
    for data in israel_pal_response['response']['facets']['pub_month']['terms']:
        month = int(data.get('term'))
        count = int(data.get('count'))
        israel_pal_article_counts[month] = count
    
#Combining the final results into one list of dict
final_results = []
i = 1
while(i <= len(china_taiwan_article_counts)):
    final_results.append({"Month": i, "China/Taiwan Article Count" : china_taiwan_article_counts[i], 
                          "Israel/Palestine Article Count" : israel_pal_article_counts[i], 
                          "Percentage Difference": 
                              str(100 * (israel_pal_article_counts[i] - china_taiwan_article_counts[i])/float(china_taiwan_article_counts[i])) + "%"})
    i = i + 1
    

""" Note:
Percentage Difference is used to compare the number of Israel/Palestine articles in a particular month to the number of 
China/Taiwan to identify trends and patterns:
Postiive percentage indicate Israel/Palestine outnumber China/Taiwan and negative percentages indicate the opposite
The magnitude showcases how much of a difference between the two on a particular month
"""

#Export to CSV
cwd=pathlib.Path.cwd()

output_dir=cwd/"out"

output_dir.mkdir()

output_file=output_dir/"NYT_API_FINAL.csv"

output_file.touch()

with output_file.open(mode='a', encoding='utf-8',newline='') as csv_file:
    writer=csv.DictWriter(csv_file,fieldnames=["Month","China/Taiwan Article Count","Israel/Palestine Article Count", "Percentage Difference"])
    writer.writeheader()
    writer.writerows(final_results)
    
    





        




