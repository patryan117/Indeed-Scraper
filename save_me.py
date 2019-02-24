import matplotlib.pyplot as plt
import requests
import operator
import datetime
from bs4 import BeautifulSoup
from collections import OrderedDict
import pandas as pd
import time
import numpy as np
import plotly
import plotly.offline
import plotly.graph_objs as go




class Sherpa:

    """A basic web scraper to extract and store daily job posts for a specific job title:
        - Recovers primary fields job title, company, location and job description
        - Adds advanced fields (exact location, FIPS code, skill-phrases)
        - Scrape should default to the entire united states and jobs posted within 1 day (location="united_states)), (window=1)
    """


    def __init__ (self):

        job_df = None
        company_df = None




    # Current scraper:
    #TODO dig up mapping program to translate address text to ZIP code.
    #TODO figure out how to solve "end of page" issue:
        #i) detect repeated entries
        #2) parse the # of pages and run until the end of page is reached
        #3) set filter to only scrape new pages


    # Additional scraping module:
    #TODO add scrape_by_company_name method


    # Database injection script:
    #TODO create a seperate program that can run in the "Task Scheduler" (importing sherpa as a library)
    #TODO add a random delay period to avoid being blacklisted

    # TODO database

    # Big questions:
    # Does it make more sense to identify skills in the scraping script, or should it be done in the database afterwards?
    # Do we need a primary key for the job database?
        #1) Numbered based on insertion order (probabbly tough to initiate in sql)
        #2) Time series related metric (time that url was retrieved)
        #3) Post URL (probably unique)
        #4) No way to form lists
    # Realistically, if we're pulling on a daily basis, and only selecting new dates, we minimize scraping and know the post date exactly.  (should there be a setting for only_new_posts = True)

    #TODO: Backburner:
        # flesh out keyword's and technical backgrounds
        # parse out degrees (masters, bachelors, PhD) and subject (computer science, finance)
        # Parse out minimum experience required

    #TODO:




    def scrape_by_job_title(self, searched_job_title="data analyst", job_location="Boston, MA", num_pages=2):

        self.search_title = searched_job_title
        self.main_df = pd.DataFrame()  # Col names are inherited from the temp df via appending

        print("\nSearching for '" + searched_job_title + "' jobs in the '" + job_location + "' area...\n")

        formatted_job_title = searched_job_title.replace(" ", "+")
        formatted_job_location = job_location.replace(" ", "+")\
            .replace(",", "%2C")


        job_page_soup_list = []

        for page in range(num_pages):  # number of pages to be scraped

            retrieval_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            counter = page * 10  # counter to increment the searches displayed per page (double check)
            url = "https://www.indeed.com/jobs?q=" + str(formatted_job_title) + "&l=" + str(formatted_job_location) + "&start=" + str(counter)
            print("\nSearching Page: " + "(" + str(page + 1) + ")" + "\n" + url + "\n")

            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            job_page_soup_list.append(soup)


            job_title_list = []
            for div in soup.find_all(name="div", attrs={"class": "row"}):
                try:
                    for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                        job_title_list.append(a["title"])
                except:
                    job_title_list.append("")


            company_name_list = []
            for div in soup.find_all(name="div", attrs={"class": "row"}):
                company = div.find_all(name="span", attrs={"class": "company"})
                if len(company) > 0:
                    for b in company:
                        company_name_list.append(b.text.strip())
                else:
                    sec_try = div.find_all(name="span", attrs={"class": "result - link - source"})
                    for span in sec_try:
                        company_name_list.append(span.text.strip())


            # note sponsored posts have a div for location and non sponsored posts have a span
            location_list = []
            for div in soup.find_all(name="div", attrs={"class": "row"}):
                try:
                    spans = div.find_all(attrs={"class": "location"})
                    for span in spans:
                        location_list.append(span.text.strip())
                except:
                    location_list.append("N/A")


            salary_list = []
            for td in soup.find_all(name="td", attrs={"class": "snip"}):
                try:
                    for snip in soup.find_all(name="span", attrs={"class": "no-wrap"}):
                        if "date" in snip.text:
                            salary_list.append("No Salary Provided")
                except:
                    try:
                        div_two = div.find(name="div", attrs={"class": "sjcl"})
                        div_three = div_two.find("div")
                        salary_list.append(div_three.text.strip())
                    except:
                        salary_list.append("No Salary Provided")


            post_date_text_list = []
            for div in soup.find_all(name="div", attrs={"class": "row"}):
                try:
                    for a in div.find(name="span", attrs={"class": "date"}):
                        post_date_text_list.append(a)
                except:
                    post_date_text_list.append("Sponsored")



            post_url_list = []
            job_description_list = []

            for div in soup.find_all(name="div", attrs={"class": "row"}):
                for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                    base_url = (a["href"])
                    post_url = ("http://indeed.com" + str(base_url))
                    post_url_list.append(post_url)

                    try:
                        post_page = requests.get(post_url)
                        job_soup = BeautifulSoup(post_page.text, "html.parser")
                        job_description = job_soup.find(name="div", attrs={
                            "class": "jobsearch-JobComponent-description icl-u-xs-mt--md"})
                        job_description = str(job_description.get_text().lower())
                        job_description = job_description.replace("\n", " ")
                        job_description_list.append(job_description)

                    except:

                        print(" ERROR PARSING JOB DESCRIPTION \n")
                        job_description_list.append("N/A")



            retrival_date_list = []
            for x in range(len(job_title_list)):
                retrival_date_list.append(retrieval_date)


            searched_job_title_list = []
            for x in range(len(job_title_list)):
                searched_job_title_list.append(searched_job_title)


            temp = {
                'Searched Job Title': searched_job_title_list,
                'Job_Title': job_title_list,
                'Company': company_name_list,
                'Location' : location_list,
                'Salary' : salary_list,
                "Post_Date_Text" : post_date_text_list,
                'Post_URL' : post_url_list,
                'Job_Description' : job_description_list,
                'Retrival_Date_List' : retrival_date_list
                }

            self.temp_job_df = pd.DataFrame(data=temp)


            self.main_df.append(self.temp_job_df)

        print(self.temp_job_df)





#########################################################
# IMPLEMENTATION                                        #
#########################################################

x = Sherpa()
x.scrape_by_job_title()
print(x.temp_job_df)





























































