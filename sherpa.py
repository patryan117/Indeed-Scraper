import requests
import datetime
import inspect
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import json
from bson import json_util

from pymongo import MongoClient

class Sherpa:

    def __init__ (self):

        job_df = None
        company_df = None



    def scrape_by_job_title(self,
                            searched_job_title="data engineer",
                            job_location="Boston, MA",
                            num_pages=2,
                            skip_sponsored = True,
                            posts_per_page = 50,
                            full_time_only = True,
                            exact_matching = True,
                            max_date_limiter = 1,
                            job_type_constraint = "full_time",

                            exclude_staffing_agencies = True,
                            distance_range = "exact",
                            ):

                            # hypothetically you could decend through salary ranges to obtain indeed's salary estimates


        # instancialize
        self.main_df = pd.DataFrame()
        self.search_title = searched_job_title
        self.skip_sponsored = skip_sponsored




        # TODO refactor with f{} and incorporate additional parameters
        print("\nSearching for '" + searched_job_title + "' jobs in the '" + job_location + "' area...\n")
        # print(inspect.signature(self.scrape_by_job_title()))


        formatted_job_title = searched_job_title.replace(" ", "+")
        formatted_job_location = job_location.replace(" ", "+")\
            .replace(",", "%2C")


        job_page_soup_list = []

        for page in range(num_pages):  # number of pages to be scraped

            retrieval_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            counter = page * 10  # counter to increment the searches displayed per page (double check)
            url = "https://www.indeed.com/jobs?q=" + str(formatted_job_title) + "&l=" + str(formatted_job_location) + "&start=" + str(counter)
            print("\nSearching Page: " + "(" + str(page + 1) + ")" + "\n" + url + "\n")

            # url = "https://www.indeed.com/jobs?as_and=data+scientist&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=0&l=&fromage=1&limit=50&sort=&psf=advsrch"



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


            for div in soup.find_all(name="div", attrs={"class": "row"}):
                for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                    base_url = (a["href"])
                    post_url = ("http://indeed.com" + str(base_url))
                    post_url_list.append(post_url)

            retrival_date_list = []
            for x in range(len(job_title_list)):
                retrival_date_list.append(retrieval_date)


            searched_job_title_list = []
            for x in range(len(job_title_list)):
                searched_job_title_list.append(searched_job_title)


            temp = {
                'Searched_Job_Title': searched_job_title_list,
                'Job_Title': job_title_list,
                'Company': company_name_list,
                'Location' : location_list,
                'Salary' : salary_list,
                "Post_Date" : post_date_text_list,
                'Post_URL' : post_url_list,
                'Retrival_Date' : retrival_date_list
                }

            self.temp_df = pd.DataFrame(data=temp)
            self.main_df =  self.main_df.append(self.temp_df)


        print(self.main_df.shape)


        if self.skip_sponsored:
            print('Removing "Sponsored" Posts...')
            self.main_df = self.main_df.loc[self.main_df['Post_Date'] != "Sponsored"]
            print(self.main_df)


        def scrape_description(url):

            try:
                post_page = requests.get(url)
                job_soup = BeautifulSoup(post_page.text, "html.parser")
                job_description = job_soup.find(name="div", attrs={
                    "class": "jobsearch-JobComponent-description icl-u-xs-mt--md"})
                job_description = str(job_description.get_text())
                print(job_description)
                job_description = job_description.replace("\n", " ")
                return job_description

            except:
                print(" ERROR PARSING JOB DESCRIPTION \n")
                return None


        #  apply scrape_description to url column and remove all posts that do not have a reachable description
        self.main_df["Description"] = self.main_df["Post_URL"].apply(scrape_description)
        self.main_df = self.main_df.loc[self.main_df['Post_Date'] != None]





    def save_df_as_csv(self, location=None, name ="sherpa_output.csv"):
        self.main_df.to_csv(name, index=False)



    def df_to_json(self, location = None, name = "sherpa_output.json"):
        out_json=self.main_df.to_json(orient='records')
        print(out_json)
        return (out_json)


    def save_df_as_json(self, location = None, name = "sherpa_output.json"):
        with open(name, 'w') as file:
            json.dump(self.df_to_json(), file)


    def dump_to_mongo(self, ):
        client = MongoClient('localhost', 27017)
        db = client['sherpa']
        posts = db['posts']
        print(posts.find_one({}))
        data = json_util.loads(self.save_df_as_json().read())



#########################################################
# IMPLEMENTATION                                        #
#########################################################

x = Sherpa()
x.scrape_by_job_title()   # scrapes search query parameters from indeed to pd dataframe
x.save_df_as_json()           # converts current pd dataframe to locally saved json file

# working
# x.save_df_as_csv()         # converts current pd dataframe  to locally saved csv file

#TODO
# x.dump_to_mongo(db_name, collection_name, database_location)     #exports to database (requires all enhanced analytics bools to be True)
# x.descriptions_to_tf_idf()  # identifies the most "significant" words in the descriptions corpus (saves instance object array)

