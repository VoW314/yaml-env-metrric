
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
grade= grade("test.yaml")
hosts = grade.unpack_hosts()

#print(hosts) #this array actually doesn't hold anything of value
grade.top_tree()


