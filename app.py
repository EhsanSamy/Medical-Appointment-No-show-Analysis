import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Loading the dataset
df = pd.read_csv('KaggleV2-May-2016.csv')

# EDA: Exploratory Data Analysis
print(df.info())
print(df.shape)
print(df.head())
print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())

# Remove unrealistic ages
df = df[(df['Age'] >= 0) & (df['Age'] <= 100)] 

# Enconding categorical variables
df['No-show'] = df['No-show'].map({'Yes': 1, 'No': 0})  # 1 = no-show, 0 = show
df['Gender'] = df['Gender'].map({'F': 0, 'M': 1}) #0 for Female, 1 for Male

# convert date columns to datetime
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])

# Feature engineering
df['GapDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
df['AppointmentDayOfWeek'] = df['AppointmentDay'].dt.day_name()
df['AppointmentYear'] = df['AppointmentDay'].dt.year
df['AppointmentMonth'] = df['AppointmentDay'].dt.month
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 19, 35, 60, 100], 
                       labels=['0-19', '20-35', '36-60', '60+'])
df['ConditionCount'] = df[['Hipertension', 'Diabetes', 'Alcoholism', 'Handcap']].sum(axis=1)

# visualizations with matplotlib

# Appointments & No-shows by Days
days_order = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
grouped_day = df.groupby('AppointmentDayOfWeek')[['No-show']].sum().join(df.groupby('AppointmentDayOfWeek').size().rename('Appointments')).reindex(days_order,fill_value=0) 
grouped_day.plot(kind='bar', title='Appointments & No-shows by Day', xlabel='Day', ylabel='Count', figsize=(10,6), color=['blue', 'hotpink'])
plt.show()

# By Month
grouped_month = df.groupby('AppointmentMonth')[['No-show']].sum().join(df.groupby('AppointmentMonth').size().rename('Appointments')).sort_index()
grouped_month.plot(kind='bar', title='Appointments & No-shows by Month', xlabel='Month', ylabel='Count', figsize=(10,6), color=['blue', 'hotpink'])
plt.show()

# By Year
grouped_year = df.groupby('AppointmentYear')[['No-show']].sum().join(df.groupby('AppointmentYear').size().rename('Appointments')).sort_index()
grouped_year.plot(kind='bar', title='Appointments & No-shows by Year', xlabel='Year', ylabel='Count', figsize=(10,6), color=['blue', 'hotpink'])
plt.show()

# No-show vs. Show-up (Pie)
no_show_counts = df['No-show'].value_counts()
no_show_counts.plot(kind='pie', labels=['Show', 'No-show'], colors=['blue', 'hotpink'], autopct='%1.1f%%', figsize=(6, 6), title='No-show vs. Show-up Rates')
plt.ylabel('')
plt.show()

# Age and Gender impact
age_gender = df.groupby(['AgeGroup', 'Gender'])['No-show'].sum().unstack()
age_gender.plot(kind='bar', title='No-show Rate by Age Group and Gender', xlabel='Age Group', ylabel='No-show Rate', figsize=(8, 5), color=['blue', 'hotpink'])
plt.legend(['Female', 'Male'])
plt.show()

# Top 10 No-show by Neighborhood (Total, not average)
top_neighborhoods = df.groupby('Neighbourhood')['No-show'].sum().sort_values(ascending=False).head(10)
top_neighborhoods.plot(kind='barh', title='Top 10 No-show by Neighborhood', xlabel='No-show Count', ylabel='Neighbourhood', figsize=(10,5), color=['blue', 'hotpink'])
plt.show()

# No-show by Chronic Condition
conditions = ['Hipertension', 'Diabetes', 'Alcoholism', 'Handcap']
no_show_counts = {}
for condition in conditions:
    no_show_counts[condition] = df[df[condition] == 1]['No-show'].sum()
no_show_counts = pd.Series(no_show_counts)
no_show_counts.plot(kind='bar', title='No-show by Chronic Conditions', xlabel='Condition', ylabel='No-show Count', figsize=(8,5), color=['blue', 'hotpink'])
plt.show()

# No-show by Gap Days
df['GapGroup'] = pd.cut(df['GapDays'], bins=[-1, 0, 2, 5, 10, 30, 100], 
                        labels=['0', '1-2', '3-5', '6-10', '11-30', '30+'])
gap_no_show_rate = df.groupby('GapGroup')['No-show'].sum()
gap_no_show_rate.plot(kind='bar', title='No-show by Gap Days', xlabel='Days between Scheduling and Appointment', ylabel='No-show', figsize=(8,5), color=['blue', 'hotpink'])
plt.show()

# No-Show by SMS
sms_no_show_rate = df.groupby('SMS_received')['No-show'].sum()
sms_no_show_rate.plot(kind='bar', title='No-show Rate by SMS Received', xlabel='SMS Received (0 = No, 1 = Yes)', ylabel='No-show Rate', figsize=(8,5), color=['blue', 'hotpink'])
plt.show()