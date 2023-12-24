
import pandas as pd
from dfs_class import * #deep search first
from grade_class import * 


#create a table
from rich import * 
from rich.console import Console
from rich.table import Table

#visualizations
import plotly.express as px


#CODE ACTUAL
grade= grade("test.yaml")
hosts = grade.unpack_hosts()
print(hosts)

