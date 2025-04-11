import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load your Excel file
matches = pd.read_excel('1 dataset1_test.xlsx')

# Rename columns for clarity
Records = pd.DataFrame(matches)
Records.columns = ['Batsman', 'Runs', 'Minute', 'Ballfaced', 'fours', 'sixes', 'StrikeRate', 'Position', 'DismissalAt', 'Innings']

# Streamlit Title
st.title("Cricket Match Analysis: Batsman Performance")

# Dropdown to select batsman
batsman_choice = st.selectbox("Select Batsman", [1, 2, 3, 4, 5, 6])

# Filter the selected batsman data
batsman_data = Records[Records.Batsman == batsman_choice]

# Display basic stats for the selected batsman
st.subheader(f"Batsman {batsman_choice}: Overview")
st.write(f"Total Matches Played: {batsman_data.shape[0]}")
st.write(f"Total Runs: {batsman_data['Runs'].sum()}")
st.write(f"Average Runs: {batsman_data['Runs'].mean():.2f}")
st.write(f"Highest Score: {batsman_data['Runs'].max()}")
st.write(f"Strike Rate: {batsman_data['StrikeRate'].mean():.2f}")

# Plot Runs of Batsman
fig, ax = plt.subplots(figsize=(10, 7))
batsman_data['Runs'].plot(kind='bar', ax=ax, color='skyblue')
ax.set_title(f"Batsman {batsman_choice}: Runs in Each Match")
ax.set_xlabel("Match Number")
ax.set_ylabel("Runs")
st.pyplot(fig)

# Plot Average Runs
fig, ax = plt.subplots(figsize=(10, 7))
batsman_data['Runs'].expanding().mean().plot(ax=ax, color='green', label='Running Average')
ax.set_title(f"Batsman {batsman_choice}: Running Average of Runs")
ax.set_xlabel("Match Number")
ax.set_ylabel("Runs")
ax.legend()
st.pyplot(fig)

# Plot Runs from Boundaries (Fours and Sixes)
runBysixFour = batsman_data[['fours', 'sixes', 'Runs']].sum()
runBysixFour['totalRunFromBoundary'] = runBysixFour['fours'] * 4 + runBysixFour['sixes'] * 6
runBysixFour['runByFour'] = runBysixFour['fours'] * 4
runBysixFour['runBysix'] = runBysixFour['sixes'] * 6

st.subheader(f"Batsman {batsman_choice}: Runs by Boundary")
st.write(runBysixFour)

fig, ax = plt.subplots(figsize=(10, 7))
runBysixFour[['runByFour', 'runBysix']].plot(kind='bar', ax=ax, color=['blue', 'orange'])
ax.set_title(f"Runs from Boundaries (Fours & Sixes) for Batsman {batsman_choice}")
ax.set_ylabel("Runs")
st.pyplot(fig)

# Plot Dismissal Types
dismissal_counts = batsman_data['DismissalAt'].value_counts()

fig, ax = plt.subplots(figsize=(10, 7))
ax.pie(dismissal_counts, labels=dismissal_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set3'))
ax.axis('equal')
ax.set_title(f"Batsman {batsman_choice}: Dismissal Type Distribution")
st.pyplot(fig)

# Plot Strike Rate vs Runs
fig, ax = plt.subplots(figsize=(10, 7))
sns.scatterplot(x="Runs", y="StrikeRate", data=batsman_data, ax=ax, color='purple')
ax.set_title(f"Batsman {batsman_choice}: Strike Rate vs Runs")
ax.set_xlabel("Runs")
ax.set_ylabel("Strike Rate")
st.pyplot(fig)

# Plot Runs at Positions 3 vs 4
batsman_pos_3 = batsman_data[batsman_data['Position'] == 3]
batsman_pos_4 = batsman_data[batsman_data['Position'] == 4]

fig, ax = plt.subplots(figsize=(10, 7))
ax.plot(batsman_pos_3.index, batsman_pos_3['Runs'], label='Position 3', color='red', linestyle='-', marker='o')
ax.plot(batsman_pos_4.index, batsman_pos_4['Runs'], label='Position 4', color='green', linestyle='-', marker='o')
ax.set_xlabel("Match Index")
ax.set_ylabel("Runs")
ax.set_title(f"Batsman {batsman_choice}: Runs at Positions 3 and 4")
ax.legend()
st.pyplot(fig)

# Pie Chart for Contribution Breakdown (Fours, Sixes, Others)
fours_runs = batsman_data['fours'].sum() * 4
sixes_runs = batsman_data['sixes'].sum() * 6
total_runs = batsman_data['Runs'].sum()
others_runs = total_runs - (fours_runs + sixes_runs)

labels = ['Fours', 'Sixes', 'Others']
sizes = [fours_runs, sixes_runs, others_runs]

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set2'))
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title(f"Batsman {batsman_choice}: Run Contribution Breakdown")
st.pyplot(fig)

# Swarm plot of Strike Rate vs Runs for Dismissal Types
fig, ax = plt.subplots(figsize=(10, 7))
sns.swarmplot(x="DismissalAt", y="StrikeRate", data=batsman_data, ax=ax)
ax.set_xlabel("Dismissal Type")
ax.set_ylabel("Strike Rate")
ax.set_title(f"Batsman {batsman_choice}: Strike Rate by Dismissal Type")
st.pyplot(fig)
