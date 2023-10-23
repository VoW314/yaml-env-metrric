import pandas as pd
import plotly.express as px
from hardness_class import *

#grade = hardness("test.yaml")
#grade = grade.one_count(grade.topology)

grade = hardness("test.yaml")

original_top = grade.original_top()
# Calculate scores and store them in a separate variable
scored_matrix = grade.score()
final_grade = grade.average_grade()


#converted these to csv for easier analysis
df = pd.DataFrame(original_top)
df.to_csv('original_top.csv')

df = pd.DataFrame(scored_matrix)
df.to_csv('scored_matrix.csv')