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
        - Visualizations and aggregate calculations should be pursued on the front end



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







































































"""



def main():

    job_title = "data scientist"
    job_location = "NC"
    data = scrape(job_title=job_title, job_location=job_location, num_pages=2)
    df = pd.DataFrame(data,
                      columns=['Job Title', 'Company', "Salary", "Location", 'Post Date', 'Post URL', 'Post Text',
                               'Skills', 'Retrial Date'])

    df = remove_duplicate_rows(df)
    cum_dict = dict_col_to_cum_dict(df, 7)
    dict_to_freq_bar_chart(cum_dict, 15, len(df), job_title)
    print(df)


def dict_to_freq_bar_chart(dic, limit=15, posts=1, job_title="'Job Title"):
    dic_len = len(dic)
    dic = sorted(dic.items(), key=operator.itemgetter(1))
    dic = OrderedDict((tuple(dic)))
    items = list(dic.items())
    skills = []
    skill_count = []
    for x in range(dic_len):
        skills.append(items[x][0])
        skill_count.append(items[x][1])

    skill_count = skill_count[limit:None]
    skills = skills[limit:None]
    skill_freq_count = []

    for y in skill_count:
        skill_freq_count.append(y / posts)

    data = [go.Bar(
        x=skill_freq_count,
        y=skills,
        orientation='h'
    )]

    layout = go.Layout(
        title='Keyword Frequency for ' + job_title + ' Job Posts:',
        autosize=True,  # change to True to manually set sizing parameters
        xaxis=dict(range=[0, 1]),
        # width=500,
        # height=500,
        margin=go.Margin(l=150, r=50, b=100, t=100, pad=4)
    )

    plotly.offline.plot({"data": data, "layout":layout})





def dict_col_to_cum_dict(dict, column_num=7):
    rows = len(dict)
    dict = dict.as_matrix(columns=None)
    keys = list(dict[0][7].keys())
    cum_dict = list_to_dict(keys)
    for x in range(rows):
        if dict[x][column_num] != 0:
            for y in keys:
                if dict[x][column_num][y] == 1:
                    cum_dict[y] += 1
    return (cum_dict)


def remove_empty_rows(df):
    df = df.dropna(subset=['Skills'], inplace=True)
    return df


def remove_duplicate_rows(df):
    df = df.drop_duplicates(subset=['Post Text'], keep=False)
    return df


def export_as_csv(df):
    df = pd.DataFrame(df)
    df.to_csv("jobs_matrix.csv")


def col_dict_to_horz_bar_chart(dict, colum_num=7):
    keys = list(
        dict[0][colum_num].keys())  # extract the keys from a the first row (assumes that all rows hold the same keys)
    cum_dict = list_to_dict(keys)  # cumulative dictionary
    skills_array = []
    count_array = []
    job_count = 0
    for x in range(0, 5000):  # DEF MORE COLUMNS THAN WE ACTUALLY NEED, IS THERE SOME WAY TO MAKE THIS DYNAMIC?
        if dict[x][colum_num] != 0:
            job_count += 1
            for y in keys:  # if the job_title column is not empty
                if dict[x][colum_num][y] == 1:  # if dictionary for a word is 1 (aka yes)
                    cum_dict[y] += 1  # increment the cumulative dictionary

    for x in cum_dict:
        skills_array.append(x)
        count_array.append(cum_dict[x] / job_count)

    y_pos = np.arange(len(skills_array))
    plt.barh(y_pos, count_array, align='center', alpha=0.5)
    plt.yticks(y_pos, skills_array)
    plt.xlim(0, 1)
    plt.xlabel("Frequency")
    plt.ylabel('Keywords')
    plt.title('Keyword Frequency per Job Search')
    plt.tight_layout()
    plt.show()
    return (cum_dict)


def list_to_dict(target_list):  # Creates an dictionary for counting, with each pair as key:0
    target_list = list({str(target_list[x].lower()) for x in range(len(target_list))})
    return {target_list[x]: 0 for x in range(len(target_list))}


def incr_dict(dict, target_text):
    for x in dict.keys():
        if x in target_text:
            dict[x] += 1
    return (dict)


def column(matrix, i):
    return [row[i] for row in matrix]


skills_list = [" Python "," AWS" , ' sql ', " hadoop ", " R ", " C# ", " SAS ", "C++", "Java ", "Matlab", "Hive", " Excel ",
               "Perl", " noSQL ", " JavaScript ", " HBase ", " Tableau ", " Scala ", " machine learning ", " Tensor Flow ",
               " deep learning ", " ML ", " PHP ", " Visual Basic ", " css ", " SAS ", "Octave", " aws ", " pig ", "numpy",
               " Objective C ", " raspberry pi ", " natural language processing "
               ]

global list_spot
global matrix_counter


def scrape(job_title="data analyst", job_location="Boston, MA", num_pages=1):

    start_time = time.time()
    print("\nSearching for '" + job_title + "' jobs in the '" + job_location + "' area...\n")

    w, h = 9, 6000;
    # global job_data_matrix
    job_data_matrix = [[np.nan for x in range(w)] for y in range(h)]
    list_spot = 0
    matrix_counter = 0
    job_page_soup_list = []
    job_title = job_title.replace(" ", "+")
    job_location = job_location.replace(" ", "+")
    job_location = job_location.replace(",", "%2C")

    for x in range(num_pages):  # number of pages to be scraped

        counter = x * 10  # counter to increment the searches displayed per page (double check)
        url = "https://www.indeed.com/jobs?q=" + str(job_title) + "&l=" + str(job_location) + "&start=" + str(counter)
        print("\nSearching Page: " + "(" + str(x + 1) + ")" + "\n" + url + "\n")

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        job_page_soup_list.append(soup)
        # print(soup.prettify())

        jobs = []
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            try:
                for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                    jobs.append(a["title"])
            except:
                jobs.append("")

        dates = []
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            try:
                for a in div.find(name="span", attrs={"class": "date"}):
                    dates.append(a)
            except:
                dates.append("Sponsored")

        companies = []
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            company = div.find_all(name="span", attrs={"class": "company"})
            if len(company) > 0:
                for b in company:
                    companies.append(b.text.strip())
            else:
                sec_try = div.find_all(name="span", attrs={"class": "result - link - source"})
                for span in sec_try:
                    companies.append(span.text.strip())

        post_urls = []
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                base_url = (a["href"])
                post_urls.append("http://indeed.com" + str(base_url))


        locations = []
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            try:
                spans = soup.find_all(name="span", attrs={"class": "location"})
                for span in spans:
                    locations.append(span.text)
            except:
                locations.append("N/A")


        salaries = []
        for td in soup.find_all(name="td", attrs={"class": "snip"}):
            try:
                for snip in soup.find_all(name="span", attrs={"class": "no-wrap"}):
                    if "date" in snip.text:
                        salaries.append("No Salary Provided")
            except:
                try:
                    div_two = div.find(name="div", attrs={"class": "sjcl"})
                    div_three = div_two.find("div")
                    salaries.append(div_three.text.strip())
                except:
                    salaries.append("No Salary Provided")

        list_spot += matrix_counter
        matrix_counter = 0


        for x in range((len(jobs))):

            job_data_matrix[x + list_spot][0] = jobs[x]
            job_data_matrix[x + list_spot][1] = companies[x]
            job_data_matrix[x + list_spot][2] = salaries[x]
            job_data_matrix[x + list_spot][3] = locations[x]
            job_data_matrix[x + list_spot][4] = dates[x]
            job_data_matrix[x + list_spot][5] = post_urls[x]


            target_url = job_data_matrix[x + list_spot][5]

            try:
                post_page = requests.get(target_url)
                job_soup = BeautifulSoup(post_page.text, "html.parser")
                job_description = job_soup.find(name="div", attrs={"class": "jobsearch-JobComponent-description icl-u-xs-mt--md"})
                job_description = str(job_description.get_text().lower())

            except:
                print("x:" + str(x) + "  list_spot:" + str(list_spot) + " matrix_counter: " + str(matrix_counter))
                print(" ERROR PARSING JOB DESCRIPTION \n")
                job_description = "N/A"

            job_description = job_description.replace(",", " ")
            job_description = job_description.replace(".", " ")
            job_description = job_description.replace("\n", " ")


            job_data_matrix[x + list_spot][6] = job_description

            data_science_skills_dict = list_to_dict(skills_list)


            job_data_matrix[x + list_spot][7] = incr_dict(data_science_skills_dict, job_description)

            job_data_matrix[x + list_spot][8] = datetime.datetime.now()





            print("\nJob Title: " + job_data_matrix[x + list_spot][0] + "\t" + "Company: " +
                  job_data_matrix[x + list_spot][1] + "\t" + "Location: " + job_data_matrix[x + list_spot][
                      3] + "\t" + " Date: " + job_data_matrix[x + list_spot][4])
            print(job_description)
            print(job_data_matrix[x + list_spot][7])



            matrix_counter += 1


    return (job_data_matrix)


#####################################################

if __name__ == '__main__':
    main()











  # Graveyard
###################################################




#
# def dict_to_bar(dict, limit=15):
#     dict_len = len(dict)
#     dict = sorted(dict.items(), key=operator.itemgetter(1))
#     dict = OrderedDict((tuple(dict)))
#     items = list(dict.items())
#     skills = []
#     skill_count = []
#
#     for x in range(dict_len):
#         skills.append(items[x][0])
#         skill_count.append(items[x][1])
#
#     skill_count = skill_count[limit:None]
#     skills = skills[limit:None]
#
#     print(skills)
#     print(skill_count)
#
#     data = [go.Bar(
#         x=skill_count,
#         y=skills,
#         orientation='h'
#     )]
#
#     layout = go.Layout(
#         autosize=False,
#         width=500,
#         height=500,
#         margin=go.Margin(
#             l=150,
#             r=50,
#             b=100,
#             t=100,
#             pad=4
#         ),
#     )
#
#
#     plotly.offline.plot({"data": data, "layout":layout})


"""

