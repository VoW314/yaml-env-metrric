import pandas as pd
from hardness_class import *

#visualizations
import plotly.express as px

#CODE ACTUAL
grade = hardness("test.yaml")

original_top = grade.original_top()
matrix_1 = grade.return_matrix()
# Calculate scores and store them in a separate variable
scored_matrix = grade.score()
final_grade, area = grade.average_grade()

print("FINAL GRADE:")
print(final_grade, "from area:", area)
#converted these to csv for easier analysis
df = pd.DataFrame(original_top)
df.to_csv('original_top.csv')

df = pd.DataFrame(scored_matrix)
df.to_csv('scored_matrix.csv')

#uncomment below if you want to create a heatmap. 
#otherwise I kept images in the visuals_oct28 folder

'''
#create visual aid using a plotly heatmap
print("Please be patient. Generating a heatmap...")
print("At a later time I will try to create the expandable info to include the .yaml info on the cells")
#original heatmap of topology
fig = px.imshow(original_top,text_auto=True, aspect="auto", title="Original Topology")
fig.show()

figF = px.imshow(scored_matrix,text_auto=True, aspect="auto", title="Scored Topology")
figF.show()
'''