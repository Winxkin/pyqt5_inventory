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
e = df['Avalible']

# Create a line chart
fig, (ax1, ax2, ax3)  = plt.subplots(3, 1)
ax1.plot(x,y)
ax3.plot(x, z)
ax2.plot(x, e)



# Add title and labels
ax1.set_title('Example Chart')
ax1.set_xlabel('X-axis label')
ax1.set_ylabel('Y-axis label')
ax1.tick_params(axis='x', rotation=90, labelsize=8)

ax2.set_title('Example Chart')
ax2.set_xlabel('X-axis label')
ax2.set_ylabel('Y-axis label')
ax2.tick_params(axis='x', rotation=90, labelsize=8)

ax3.set_title('Example Chart')
ax3.set_xlabel('X-axis label')
ax3.set_ylabel('Y-axis label')
ax3.tick_params(axis='x', rotation=90, labelsize=8)

# Display the chart
plt.show()