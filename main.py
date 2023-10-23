import pandas
import plotly.express as px
from hardness_class import *

#grade = hardness("test.yaml")
#grade = grade.one_count(grade.topology)

grade = hardness("test.yaml")

# Calculate scores and store them in a separate variable
scored_matrix = grade.score()
final_grade = grade.average_grade()

print(scored_matrix)
print(final_grade)