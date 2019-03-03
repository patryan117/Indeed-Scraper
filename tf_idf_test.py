

import pandas as pd
import re

df = pd.read_csv("sherpa_output.csv")

descriptions = list(df["Description"])


# TODO intergrate regex to replace urls (@^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*$@i)
descriptions = [x.lower() for x in descriptions]
descriptions = [x.replace("!", " ") for x in descriptions]
descriptions = [x.replace(".", " ") for x in descriptions]
descriptions = [x.replace(",", " ") for x in descriptions]
descriptions = [x.replace("\n", " ") for x in descriptions]
descriptions = [x.replace("?", " ") for x in descriptions]
descriptions = [x.replace("'", " ") for x in descriptions]
descriptions = [x.replace("  ", " ") for x in descriptions]




print(descriptions)

