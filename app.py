import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc 

# Loading the dataset
df = pd.read_csv('KaggleV2-May-2016.csv')

# EDA: Exploratory Data Analysis
print("Info: ")
print(df.info())

print(f"The shape of the data: {df.shape}")

print("Description: ")
print(df.describe())

print(f"Null = {df.isnull().sum()}")

print(f"Duplicates = {df.duplicated().sum()}")

print("First 5 rows: ")
print(df.head())

# Remove unrealistic ages
df = df[(df['Age'] >= 0) & (df['Age'] <= 100)] 

# Encoding categorical variables
label_encoder = LabelEncoder()
df['No-show'] = label_encoder.fit_transform(df['No-show'])
df['Gender'] = label_encoder.fit_transform(df['Gender'])

# Convert date columns to datetime
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])

# Feature engineering
df['GapDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
df['AppointmentDayOfWeek'] = df['AppointmentDay'].dt.day_name()
df['AppointmentMonth'] = df['AppointmentDay'].dt.month
df['AppointmentYear'] = df['AppointmentDay'].dt.year

df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 19, 35, 60, 100],
                        labels=['0-19', '20-35', '36-60', '60+'])
df['GapGroup'] = pd.cut(df['GapDays'], bins=[-1, 0, 2, 5, 10, 30, 100],
                        labels=['0', '1-2', '3-5', '6-10', '11-30', '30+'])
df['ConditionCount'] = df[['Hipertension', 'Diabetes', 'Alcoholism', 'Handcap']].sum(axis=1)

days_order = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Chart Functions With Plotly
def make_fig1(dff):
    grouped = dff.groupby('AppointmentDayOfWeek', observed=False)[['No-show']].sum().join(
        dff.groupby('AppointmentDayOfWeek', observed=False).size().rename('Appointments')
    ).reindex(days_order, fill_value=0)
    return px.bar(
        grouped, x=grouped.index, y=['Appointments', 'No-show'],
        title='Appointments & No-shows by Day',
        barmode='group',
        labels={'x': 'Day of the Week', 'y': 'Number of Appointments'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

def make_fig2(dff):
    grouped = dff.groupby('AppointmentMonth', observed=False)[['No-show']].sum().join(
        dff.groupby('AppointmentMonth', observed=False).size().rename('Appointments')
    ).sort_index()
    return px.bar(
        grouped, x=grouped.index, y=['Appointments', 'No-show'],
        title='Appointments & No-shows by Month',
        barmode='group',
        labels={'x': 'Month', 'y': 'Number of Appointments'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

def make_fig3(dff):
    grouped = dff.groupby('AppointmentYear', observed=False)[['No-show']].sum().join(
        dff.groupby('AppointmentYear', observed=False).size().rename('Appointments')
    ).sort_index()
    return px.bar(
        grouped, x=grouped.index, y=['Appointments', 'No-show'],
        title='Appointments & No-shows by Year',
        barmode='group',
        labels={'x': 'Year', 'y': 'Number of Appointments'},
        color_discrete_sequence=px.colors.qualitative.Bold
    )

def make_fig4(dff):
    counts = dff['No-show'].value_counts()
    counts.index = counts.index.map({0: 'Show-up', 1: 'No-show'})
    return px.pie(
        counts, values=counts.values, names=counts.index,
        title='No-show vs. Show-up Rates',
        color_discrete_sequence=px.colors.qualitative.Set3
    )

def make_fig5(dff):
    age_gender = dff.groupby(['AgeGroup', 'Gender'], observed=False)['No-show'].sum().unstack()
    age_gender.columns = age_gender.columns.map({0: 'Female', 1: 'Male'})
    return px.bar(
        age_gender, x=age_gender.index, y=age_gender.columns,
        title='No-show by Age Group',
        barmode='group',
        labels={'x': 'Age Group', 'y': 'No-show Count'},
        color_discrete_sequence=['#ff69b4', '#1f77b4']
    )

def make_fig6(dff):
    top_neigh = dff.groupby('Neighbourhood', observed=False)['No-show'].sum().sort_values(ascending=False).head(10)
    return px.bar(
        top_neigh, x=top_neigh.index, y=top_neigh.values,
        title='Top 10 No-show by Neighborhood',
        labels={'x': 'Neighborhood', 'y': 'No-show Count'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

def make_fig7(dff):
    conditions = ['Hipertension', 'Diabetes', 'Alcoholism', 'Handcap']
    counts = {c: dff[dff[c] == 1]['No-show'].sum() for c in conditions}
    return px.bar(
        pd.Series(counts), x=list(counts.keys()), y=list(counts.values()),
        title='No-show by Chronic Conditions',
        labels={'x': 'Condition', 'y': 'No-show Count'},
        color_discrete_sequence=px.colors.qualitative.Prism
    )

def make_fig8(dff):
    gap_counts = dff.groupby('GapGroup', observed=False)['No-show'].sum()
    return px.bar(
        gap_counts, x=gap_counts.index, y=gap_counts.values,
        title='No-show by Gap Days',
        labels={'x': 'Gap Days Group', 'y': 'No-show Count'},
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

def make_fig9(dff):
    sms_counts = dff.groupby('SMS_received', observed=False)['No-show'].sum()
    sms_counts.index = sms_counts.index.map({0: "No SMS", 1: "SMS Sent"})
    return px.bar(
        sms_counts, x=sms_counts.index, y=sms_counts.values,
        title='No-show by SMS Received',
        labels={'x': 'SMS Received', 'y': 'No-show Count'},
        color_discrete_sequence=px.colors.qualitative.Safe
    )

def make_fig10(dff):
    pivot_heat = dff.pivot_table(index='AgeGroup', columns='AppointmentDayOfWeek',
                                values='No-show', aggfunc='mean', fill_value=0)
    pivot_heat = pivot_heat.reindex(columns=days_order)
    return px.imshow(
        pivot_heat.values,
        x=pivot_heat.columns,
        y=pivot_heat.index.astype(str),
        title='No-show Rate by Day of Week & Age Group',
        labels=dict(x='Day of Week', y='Age Group', color='No-show Rate'),
        color_continuous_scale='Turbo'
    )

fig_makers = [make_fig1, make_fig2, make_fig3, make_fig4, make_fig5,
              make_fig6, make_fig7, make_fig8, make_fig9, make_fig10]

# Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  

filters_row = dbc.Row([
    dbc.Col([dbc.Label("Day"),
        dcc.Dropdown(id="Day-filter",
            options=[{"label": y, "value": y} for y in days_order],
            clearable=True)], md=3),
    dbc.Col([dbc.Label("Neighborhood"),
        dcc.Dropdown(id="neigh-filter",
            options=[{"label": n, "value": n} for n in sorted(df['Neighbourhood'].unique())],
            clearable=True)], md=3),
    dbc.Col([dbc.Label("Age Group"),
        dcc.Dropdown(id="age-filter",
            options=[{"label": str(a), "value": a} for a in df['AgeGroup'].cat.categories],
            clearable=True)], md=3),
    dbc.Col([dbc.Label("Gap Days Group"),
        dcc.Dropdown(id="gap-filter",
            options=[{"label": str(g), "value": g} for g in df['GapGroup'].cat.categories],
            clearable=True)], md=3),
], className="mb-4")

graph_components = [dcc.Graph(id=f"fig{i+1}") for i in range(len(fig_makers))]

app.layout = dbc.Container([
    html.H1("Medical Appointments — No-show Analysis", className="text-center mb-4", style={"margin": "20px"}),
    html.P(f"Data range: {df['AppointmentDay'].min().date()} — {df['AppointmentDay'].max().date()}",
           className="text-center text-muted"),
    html.Div(id="kpi-cards"),
    html.Hr(),
    filters_row,
    html.Hr(),
    dbc.Row([dbc.Col(graph_components[i], md=6) for i in range(2)]),
    dbc.Row([dbc.Col(graph_components[i], md=6) for i in range(2, 4)]),
    dbc.Row([dbc.Col(graph_components[i], md=6) for i in range(4, 6)]),
    dbc.Row([dbc.Col(graph_components[i], md=6) for i in range(6, 8)]),
    dbc.Row([dbc.Col(graph_components[i], md=6) for i in range(8, 10)])
], fluid=True)

@app.callback(
    [Output("kpi-cards", "children")] + 
    [Output(f"fig{i+1}", "figure") for i in range(len(fig_makers))],
    [Input("Day-filter", "value"),
     Input("neigh-filter", "value"),
     Input("age-filter", "value"),
     Input("gap-filter", "value")]
)
def update_dashboard(day, neigh, age, gap):
    dff = df.copy()

    if day: dff = dff[dff['AppointmentDayOfWeek'] == day] 
    if neigh: dff = dff[dff['Neighbourhood'] == neigh]
    if age:   dff = dff[dff['AgeGroup'] == age]
    if gap:   dff = dff[dff['GapGroup'] == gap]

    if dff.empty:
        empty_kpi = dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([html.H6("Total Appointments"), html.H4("0", className="text-primary")])), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.H6("Total No-shows"), html.H4("0", className="text-danger")])), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.H6("No-show Rate"), html.H4("0%", className="text-warning")])), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([html.H6("Avg Gap Days"), html.H4("0", className="text-success")])), md=3),
        ], className="mb-4")
        empty_figs = [px.scatter(title="No Data Available") for _ in fig_makers]
        return [empty_kpi] + empty_figs

    total_appointments = len(dff)
    total_noshow = int(dff['No-show'].sum())
    noshow_rate = (total_noshow / total_appointments * 100) if total_appointments else 0
    average_gap_days = dff['GapDays'].mean() if not dff.empty else 0

    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Total Appointments"), html.H4(f"{total_appointments:,}", className="text-primary")])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Total No-shows"), html.H4(f"{total_noshow:,}", className="text-danger")])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("No-show Rate"), html.H4(f"{noshow_rate:.2f}%", className="text-warning")])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Avg Gap Days"), html.H4(f"{average_gap_days:.2f}", className="text-success")])), md=3),
    ], className="mb-4")

    return [kpi_cards] + [maker(dff) for maker in fig_makers]

if __name__ == '__main__':
    app.run(debug=True, port=8060)
