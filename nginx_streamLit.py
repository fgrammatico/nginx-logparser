import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Get the current working directory
current_dir = os.getcwd()

# Construct the path to the CSV file
csv_file_path = os.path.join(current_dir, 'combined_data.csv')

# Load the data
data = pd.read_csv(csv_file_path)

# Convert timestamps to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%Y%m%d%H%M%S')

# Filter out problematic connections
problematic_connections = data[data['Status'] != 200]

# Streamlit app
st.title('Nginx Log Analysis')

# Aggregate data for most troublesome connections
troublesome_connections = problematic_connections.groupby(['SourceIP', 'UpstreamIP', 'ErrorDescription']).size().reset_index(name='FailCount')
top_troublesome_connections = troublesome_connections.sort_values(by='FailCount', ascending=False).head(10)

# Bar chart for most troublesome connections
st.write('Most Troublesome Connections')
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_troublesome_connections, x='FailCount', y='SourceIP', hue='UpstreamIP', dodge=False, ax=ax3)
ax3.set_xlabel('Number of Fails')
ax3.set_ylabel('Source IP')
ax3.set_title('Top 10 Most Troublesome Connections')
st.pyplot(fig3)

st.write('Problematic Connections Analysis')
# Display the problematic connections data
st.dataframe(problematic_connections)

# Count the occurrences of problematic connections per IP address
ip_counts = problematic_connections['SourceIP'].value_counts()

# Plot the data
st.bar_chart(ip_counts)

# Show affected IPs during the period
st.write('Affected IPs during the period:')
st.dataframe(problematic_connections[['SourceIP', 'Timestamp', 'ErrorDescription']].drop_duplicates())

# Plot the problematic connections over time
st.write('Problematic Connections Over Time')
fig, ax = plt.subplots(figsize=(10, 6))
problematic_connections.set_index('Timestamp', inplace=True)
daily_counts = problematic_connections.resample('D').size()
daily_counts.plot(ax=ax, color='blue', marker='o', linestyle='-')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Problematic Connections')
ax.set_title('Problematic Connections Over Time')
ax.grid(True)

# Set x-axis limits based on the actual data
min_date = problematic_connections.index.min()
max_date = problematic_connections.index.max()
ax.set_xlim([min_date, max_date])
ax.set_ylim([0, daily_counts.max() + 1])
st.pyplot(fig)

# Function to get the most common reason for an IP
def get_most_common_reason(ip):
    reasons = problematic_connections[problematic_connections['SourceIP'] == ip]['ErrorDescription']
    return reasons.mode()[0] if not reasons.mode().empty else 'Unknown'

# Pie chart for most problematic SourceIP's
st.write('Most Problematic SourceIP\'s')
source_ip_counts = problematic_connections['SourceIP'].value_counts().head(10)
source_ip_labels = [f"{ip}\nfailed={count} times\nreason={get_most_common_reason(ip)}" for ip, count in source_ip_counts.items()]

# Generate colors
colors = sns.color_palette('hsv', len(source_ip_counts))

# Display pie chart with legend
fig1, ax1 = plt.subplots(figsize=(10, 6))
wedges, texts, autotexts = ax1.pie(source_ip_counts, labels=None, autopct='%1.1f%%', startangle=90, colors=colors)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Add legend
ax1.legend(wedges, source_ip_labels, title="Source IPs", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

st.pyplot(fig1)

# Pie chart for most problematic UpstreamIP's
st.write('Most Problematic UpstreamIP\'s')
upstream_ip_counts = problematic_connections['UpstreamIP'].value_counts().head(10)
upstream_ip_labels = [f"{ip}\nfailed={count} times\nreason={get_most_common_reason(ip)}" for ip, count in upstream_ip_counts.items()]

# Generate colors
colors = sns.color_palette('hsv', len(upstream_ip_counts))

# Display pie chart with legend
fig2, ax2 = plt.subplots(figsize=(10, 6))
wedges, texts, autotexts = ax2.pie(upstream_ip_counts, labels=None, autopct='%1.1f%%', startangle=90, colors=colors)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Add legend
ax2.legend(wedges, upstream_ip_labels, title="Upstream IPs", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

st.pyplot(fig2)