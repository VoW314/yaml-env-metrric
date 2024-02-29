#Author: Shreyas Bera

import pandas as pd
from unpack import * 
from grade import * 


#create a table
from rich import * 
from rich.console import Console
from rich.table import Table

#visualizations
import plotly.express as px


#CODE ACTUAL

#Test different vanilla files to prove it works
grade_med = grade("medium.yaml")
grade_med_multi = grade("medium_multi.yaml")
grade_tiny = grade("tiny.yaml")

grade_tiny.exploitable_services()

#hosts = grade.host_table()
#print(hosts) #this array actually doesn't hold anything of value
#grade.top_tree()


