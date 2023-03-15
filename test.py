import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import csv
import matplotlib.dates as mdates
# Read CSV file
df = pd.read_csv('./analysis/Mar-15-2023.csv')
#print(df)
# Set the X and Y values
print(df)
x = df['time']
y = df['OOS']
z = df['IS']

# Create a line chart
plt.plot(x, y,z)
plt.gcf().autofmt_xdate()

# Add title and labels
plt.title('Example Chart')
plt.xlabel('X-axis label')
plt.ylabel('Y-axis label')
plt.xticks(rotation='vertical', fontsize = 8)
# Display the chart
plt.show()