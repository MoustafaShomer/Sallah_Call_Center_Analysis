import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------Import the data--------------------
feb = pd.read_csv("C:/Users/workstation/OneDrive/Desktop/Sallah Project/Feb.csv")

march = pd.read_csv("C:/Users/workstation/OneDrive/Desktop/Sallah Project/Mar.csv")

april = pd.read_csv("C:/Users/workstation/OneDrive/Desktop/Sallah Project/Apr.csv")

# Combine the three CSV sheets (February, March, and April) into one consolidated dataset
df = pd.concat([feb, march, april], ignore_index=True)

# -------------------------Data Cleaning----------------------

# clean the data by removing the white space from column names and replace spaces with (_)
df.columns = [
    str(i).strip().lower().replace(" ", "_").replace("-", "_") for i in df.columns
]

# check for any missing values or Nulls
print("\nThe missing values per column:\n", df.isna().sum())

# check for duplicated values
print("\nThe Duplicated values:\n", df.duplicated().sum())

# convert the date column data type from object to DateTime data type
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# -----detect outliers in the data frame------
def detect_outliers(df):
    outlier_summary = {}
    #loop throug numeric data only
    for col in df.select_dtypes(include=['int64','float64']).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

         #extract oultiers per column 
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        outlier_summary[col] = {
            "num_outliers": len(outliers),
            "percent_outliers": round(len(outliers) / len(df) * 100, 0)
        }

    return outlier_summary

#extract all  outliers and print them
outlier_report = detect_outliers(df)

for col, stats in outlier_report.items():
    print(f"The outliers in [ {col} ] column are {stats['num_outliers']} with percent of {stats['percent_outliers']}%")
    
#------------------------Handling the outliers --------------------------

def handle_outlier(df):
    new_df = df.copy()
    
    for col in new_df.select_dtypes(include=['float64', 'int64']).columns:
        Q1 = new_df[col].quantile(0.25)
        Q3 = new_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # replace outlier values with upper bound or lower bound
        new_df.loc[new_df[col] > upper_bound, col] = round(upper_bound, 0)
        new_df.loc[new_df[col] < lower_bound, col] = round(lower_bound, 0)

    return new_df

df = handle_outlier(df)

# Now the data is cleaned and will be saved as one new file at the same path
df.to_csv("C:/Users/workstation/OneDrive/Desktop/Sallah Project/final_cleaned_data.csv", index=False)

# ---------------------- Descriptive Analysis----------------------

# The total number of Forecasted Calls, Calls Offered, and Calls Handled across the three months
total_forcast_calls = df["forecasted_calls"].sum()
total_calls_offered = df["calls_offered"].sum()
total_Calls_Handled = df["calls_handled"].sum()
# print the above values
print(f"The total Forecasted Calls : {total_forcast_calls:,}")
print(f"The total Calls Offered : {total_calls_offered:,}")
print(f"The total Calls Handled : {total_Calls_Handled:,}")


# Which month had the highest call abandonment rate, and by how much compared to the others?

# add new column for month name to groub with it
df["month_name"] = df["date"].dt.month_name()

# group the abondened calls by month name to get the rate
Month_abondon_calls = df.groupby("month_name")["calls_abandon"].sum()

# group the offerd calls by month name to get the rate
Month_offerd_calls = df.groupby("month_name")["calls_offered"].sum()

# Month abondoned rate
Month_abondoned_rate = (Month_abondon_calls / Month_offerd_calls) * 100

# print the highst month using id max,and the highest rate using the max function
highest_rate = Month_abondoned_rate.max()
highest_month = Month_abondoned_rate.idxmax()

print(
    f"The month had the highest call abandonment rate is : {highest_month} with rate{highest_rate: .2f}%"
)

# and by how much compared to the others?
for month, rate in Month_abondoned_rate.items():
    if month != highest_month:
        diff = highest_rate - rate
        print(f"{highest_month} is higher than {month} by {diff:.2f}")

# Who are the top three agents with the highest Answer Time?
top3_agents = df.groupby("agent_name")["answer_time"].mean().nlargest(3)

print("The top three agents with the highest answer time are : \n")
for name, value in top3_agents.items():
    print(f"{name} with answer time(in seconds) {value:,}")
#-----------------------Performance Insights----------------------------
# - Calculate the average ASA (Average Speed of Answer) for each month and identify trends.

# arrange month order
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

asa_trend = df.groupby('month_name')['asa'].mean().reindex(month_order)
print(asa_trend)

# present the trend of (ASA) visually
asa_trend.plot(kind= 'line', marker = 'o')
plt.title('Average Speed of Answer (ASA) per Month')
plt.xlabel('Month')
plt.ylabel('(ASA) per Month in (seconds)')
plt.show()

##-- Analyze the relationship between Calls Offered and Calls Handled. Is the team meeting the demand:
df['handled_ratio'] = df['calls_handled']/ df['calls_offered']

if (df['handled_ratio'] > 0.95).all():
    print("All the days we have call handled ratio greater than %95 of offered called: team is meeting the demand.")
else:
    no_of_days = (df['handled_ratio'] <= 0.95).sum()
    print(f"There are {no_of_days} days with call handled ratio less than %95 of offered called. Check details:")
    print(df[df['handled_ratio'] <= 0.95])
    
#- Which agent handled the most calls within the threshold, and how does it compare to others?
handled_threshold = df.groupby('agent_name')['calls_handled_with_in_thrshold'].sum()
top_agent = handled_threshold.idxmax()

#and how does it compare to others
comparison = handled_threshold / handled_threshold.max() * 100

print(f"Top Agent is : {top_agent}")
print("\nComparison (% of Top Agent):")
print(comparison.sort_values(ascending=False))  
    
    