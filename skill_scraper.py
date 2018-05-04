import matplotlib.pyplot as plt
plt.rcdefaults()
import requests
import plotly
import operator
import operator
# from fake_useragent import UserAgent
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='patryan117', api_key='sU5DfakuvEH0BEVqQE5e')
import matplotlib.ticker as mtick
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
from collections import OrderedDict


# pandas dataframe printing settings

np.set_printoptions(threshold=np.inf)
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)




#todo wrap as a class, so that you can pass df.name to plotly to add title

# also i dont know how the link scraped is actually dead?  ( its gotta work if its scraping the text correctly)


def main():
    data = scrape(job_title="data scientist", job_location = "Boston, MA", num_pages = 10)
    df = pd.DataFrame(data, columns=['Job Title', 'Company', "Salary", "Location", 'Date Posted', 'Post URL', 'Post Text', 'Skills'])
    df = remove_duplicate_rows(df)
    print(df)
    cum_dict = dict_col_to_cum_dict(df,7)
    print(cum_dict)
    something = dict_to_freq_bar(cum_dict,10,len(df))

    for x in range(len(df)):
        print(df.iloc[x,6], '/n')



def dict_to_freq_bar(dic, limit=20, posts=1):
    dic_len = len(dic)
    dic = sorted(dic.items(), key=operator.itemgetter(1))
    dic = OrderedDict((tuple(dic)))
    items = list(dic.items())
    skills = []
    skill_count = []

    for x in range(dic_len):
        skills.append(items[x][0])
        skill_count.append(items[x][1])

    skill_count=skill_count[limit:None]  #TODO first, the limit doesnt work at all, but if removed we loose all titles... idk bruh
    skills=skills[limit:None]
    print(skill_count)
    skill_freq_count = []

    for y in (skill_count):
        skill_freq_count.append(y/posts)



    print(skills)
    print(skill_freq_count)

    data = [go.Bar(
        x=skill_freq_count,
        y=skills,
        orientation='h'
    )]

    layout = go.Layout(
        autosize=False,
        width=500,
        height=500,
        margin=go.Margin(
            l=150,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        xaxis=dict(range=[0, 1]
        )
    )


    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='size-margins')




def dict_to_bar(dict, limit=10):
    dict_len = len(dict)
    dict = sorted(dict.items(), key=operator.itemgetter(1))
    dict = OrderedDict((tuple(dict)))
    items = list(dict.items())
    skills = []
    skill_count = []

    for x in range(dict_len):
        skills.append(items[x][0])
        skill_count.append(items[x][1])

    skill_count=skill_count[limit:None]
    skills=skills[limit:None]

    print(skills)
    print(skill_count)

    data = [go.Bar(
        x=skill_count,
        y=skills,
        orientation='h'
    )]

    layout = go.Layout(
        autosize=False,
        width=500,
        height=500,
        margin=go.Margin(
            l=150,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        # paper_bgcolor='#7f7f7f',
        # plot_bgcolor='#c7c7c7'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='size-margins')





def make_salary_donut_chart(dict, limit = 10):
    skills = list((dict.keys()))[0:limit]
    skill_count = list((dict.values()))[0:limit]

    fig = {
        "data": [
            {
                "values": skill_count,
                "labels": skills,
                "text": skills,
                 "showlegend": False,
                'textposition': 'outside',
                "textfont" : {
                "size":10,
                },
                "name": "",
                "hoverinfo": "label+percent+name",
                "hole": .7,
                "type": "pie"
            },
            ],
        "layout": {
            "autosize" : True,
            "width" : 200,
            "height" : 200,
            "title": "",
            "annotations": [
                {
                    "font": {
                        "size": 15
                    },
                    "showarrow": False,
                    "text": "Salaries",
                },
            ]
        }
    }

    # return plotly.offline.plot(fig, output_type="div", include_plotlyjs=False)
    py.plot(fig, filename='donut')


def dict_col_to_cum_dict(dict, column_num = 7):
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
    keys = list(dict[0][colum_num].keys())    # extract the keys from a the first row (assumes that all rows hold the same keys)
    cum_dict = list_to_dict(keys)             # cumulative dictionary
    skills_array = []
    count_array = []
    job_count = 0
    for x in range(0,5000):     # DEF MORE COLUMNS THAN WE ACTUALLY NEED, IS THERE SOME WAY TO MAKE THIS DYNAMIC?
        if dict[x][colum_num] != 0:
            job_count += 1
            for y in keys:                          # if the job_title column is not empty
                if dict[x][colum_num][y] == 1:         # if dictionary for a word is 1 (aka yes)
                    cum_dict[y] += 1                    #increment the cumulative dictionary

    for x in cum_dict:
        skills_array.append(x)
        count_array.append(cum_dict[x]/job_count)

    y_pos = np.arange(len(skills_array))
    plt.barh(y_pos, count_array, align='center', alpha=0.5)
    plt.yticks(y_pos, skills_array)
    plt.xlim(0,1)
    plt.xlabel("Frequency")
    plt.ylabel('Keywords')
    plt.title('Keyword Frequency per Job Search')
    plt.tight_layout()
    plt.show()
    return(cum_dict)





def list_to_dict(target_list):    # Creates an dictionary for counting, with each pair as key:0
    target_list = list({ str(target_list[x].lower())for x in range(len(target_list))})
    return {target_list[x] : 0 for x in range(len(target_list))}


def incr_dict(dict, target_text):
    for x in dict.keys():
        if x in target_text:
            dict[x] += 1
    return(dict)


def column(matrix, i):
    return [row[i] for row in matrix]

# Strings need to be buffered before and after with spaces (otherwise "excel" will throw errors for "ecellent", or as a verb)
# alternatively could have facilitate using a loop to add before and after the target string


skills_list = [" Python ", ' sql ', " hadoop ", " R ", " C# ", " SAS ", "C++", "Java ", "Matlab", "Hive", " Excel ", "Perl",
               " noSQL ", " JavaScript ", " HBase ", " Tableau ", " Scala ", " machine learning ",  " Tensor Flow ", " deep learning ",
               " ML ", " PHP ", " Visual Basic ", " css ", " SAS ", "Octave", " aws ", " pig ", "numpy", "Objective C"]

# frameworks_list = ["hadoop", "spark", "aws", "hive", "nosql", "cassandra", "mysql",
                   # "mysql", "hbase", "pig", "mongodb", "git", "elasticsearch", "numpy",
                   # "tensorflow", "scipy", "hadoop" ]

# academics_list = [" PhD ", " Bachelor's ", " Bachelors ", " Master's ", "Masters", "publications", "Journal", "statistics",
#                   "Mathematics", ]




global list_spot
global matrix_counter


def scrape(job_title="data analyst", job_location = "Boston, MA", num_pages = 1):


    start_time = time.time()

    print("\nSearching for '" + job_title + "' jobs in the '" + job_location + "' area...\n")


    w, h =8, 6000;
    global job_data_matrix                                                   # Define a matrix of enough rows to hold all scraped job posts
    job_data_matrix = [[np.nan for x in range(w)] for y in range(h)]
    list_spot = 0
    matrix_counter = 0
    job_page_soup_list = []


    job_title = job_title.replace(" ", "+")   # format the job title so that it can be directly inserted into the indeed url
    job_location = job_location.replace(" ", "+")    # format the job location so that it can be inserted into the indeed url
    job_location = job_location.replace(",", "%2C")




    for x in range(num_pages):           # number of pages to be scraped

        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

        counter = x * 10
        url = "https://www.indeed.com/jobs?q=" + str(job_title) + "&l=" + str(job_location) + "&start=" + str(counter)
        print("\nSearching URL: " + "(" +str(x+1)+ ")" + "\n" + url + "\n")


        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")    # read the various components of the page, rather than as one long string.
        job_page_soup_list.append(soup)
       # print(soup.prettify())                            #printing soup in a more structured tree format that makes for easier reading

        jobs = []
        for div in soup.find_all(name="div", attrs={"class":"row"}):
          for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])

        dates = []
        for div in soup.find_all(name="div", attrs={"class":"row"}):
            try:
                for a in div.find(name="span", attrs= {"class":"date"}):
                    dates.append(a)
            except:
                dates.append("Sponsored")


        companies = []
        for div in soup.find_all(name="div", attrs={"class":"row"}):
            company = div.find_all(name="span", attrs = {"class":"company"})
            if len(company) > 0:
                for b in company:
                    companies.append(b.text.strip())
            else:
                sec_try = div.find_all(name="span", attrs = {"class":"result - link - source"})
                for span in sec_try:
                    companies.append(span.text.strip())


        post_urls=[]
        for div in soup.find_all(name="div", attrs={"class": "row"}):
            for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                base_url = (a["href"])
                post_urls.append("http://indeed.com"+str(base_url))


        locations = []
        spans = soup.find_all(name="span", attrs={"class" : "location"})
        for span in spans:
            locations.append(span.text)


        salaries = []
        for td in soup.find_all(name="td", attrs={"class" : "snip"}):           #TODO figure out how to only grab the "snip" elements in the job posts
            try:                                                                # Its gonna be pretty tricky, since not all posts seem to have this category (might need to be removed entirely)
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
            target_url = job_data_matrix[x+list_spot][5]


            try:
                target_url
                post_page = requests.get(target_url)
                job_soup = BeautifulSoup(post_page.text, "html.parser")

                job_soup = job_soup.find(name="span", attrs={"id": "job_summary"})
                job_soup = job_soup.get_text().lower()

            except:
                print("x:" + str(x) + "  list_spot:" + str(list_spot) + " matrix_counter: " + str(matrix_counter))
                print(" URL ERROR!!! \n")
                continue

            job_soup = job_soup.replace(",", " ")
            job_soup = job_soup.replace(".", " ")
            job_soup = job_soup.replace(";", " ")
            job_data_matrix[x +list_spot][6] = job_soup

            data_science_skills_dict = list_to_dict(skills_list)
            job_data_matrix[x+list_spot][7] = incr_dict(data_science_skills_dict, job_soup)

            print ( "\nJob Title: " + job_data_matrix[x + list_spot][0] + "\t" + "Company: " + job_data_matrix[x + list_spot][1] + "\t"+ "Location: " + job_data_matrix[x + list_spot][3] + "\t" + " Date: "  + job_data_matrix[x + list_spot][4] )
            print(str(job_data_matrix[x+ list_spot][7]))
            matrix_counter += 1




    elapsed_time = time.time() - start_time



    return(job_data_matrix)





# print(np.matrix(returned_job_matrix))

# df = pd.DataFrame(returned_job_matrix)
# df.to_csv("jobs_matrix.csv")


if __name__ == '__main__':
    main()