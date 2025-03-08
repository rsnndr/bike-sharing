import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='whitegrid')

# Menyiapkan data day_df
df = pd.read_csv(r"D:\SUBMISSION_ANALISIS_DATA\data\day.csv")
df.head()

# Mengubah nama judul kolom
df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# Mengubah nilai variabel season
def find_season(season):
    season_string = {1: 'Fall', 2:'Spring', 3:'Summer', 4:'Winter'}
    return season_string.get(season)
season_list = []

for season in df['season']:
    season = find_season(season)
    season_list.append(season)
df['season'] = season_list

# Menyiapkan day_df
def create_day_df(df):
    day_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return day_df

# Menyiapkan casual_df
def create_casual_df(df):
    casual_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_df

# Menyiapkan registered_df
def create_registered_df(df):
    registered_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_df
    
# Menyiapkan registered_df
def create_registered_df(df):
    registered_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return registered_df

# Menyiapkan weekday_df
def create_weekday_df(df):
    weekday_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_df

# Menyiapkan workingday_df
def create_workingday_df(df):
    workingday_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_df

# Menyiapkan holiday_df
def create_holiday_df(df):
    holiday_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_df

# Membuat komponen filter
min_date = pd.to_datetime(df['dateday']).dt.date.min()
max_date = pd.to_datetime(df['dateday']).dt.date.max()
 
with st.sidebar:
    st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fpixabay.com%2Fid%2Fimages%2Fsearch%2Fkartun%2520sepeda%2F&psig=AOvVaw0mq35Vm98V0FirFP0JPE3V&ust=1741520996307000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCICPxrW1-osDFQAAAAAdAAAAABAE")
    
# Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['dateday'] >= str(start_date)) & 
                (df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
day_df = create_day_df(main_df)
casual_df = create_casual_df(main_df)
registered_df = create_registered_df(main_df)
weekday_df = create_weekday_df(main_df)
workingday_df = create_workingday_df(main_df)
holiday_df = create_holiday_df(main_df)

# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Bike Sharing Dashboard 🚲')

# Membuat jumlah penyewaan berdasarkan season
st.subheader('Seasonly')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=registered_df,
    label='Registered',
    color='#7FFFD4',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=registered_df,
    label='Casual',
    color='#A52A2A',
    ax=ax
)

for index, row in registered_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan weekday, workingday dan holiday
st.subheader('Weekday, Workingday, and Holiday')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))

colors = ["#72BCD4", "#DEB887"]
color = ['#7FFF00', '#00008B']
warna = ['#A52A2A', '#8B0000', '#E6E6FA', '#808000', '#F0E68C', '#DC143C', '#006400']

# Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_df,
    palette=colors,
    ax=axes[0])

for index, row in enumerate(workingday_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Working Day')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
sns.barplot(
  x='holiday',
  y='count',
  data=holiday_df,
  palette=color,
  ax=axes[1])

for index, row in enumerate(holiday_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan weekday
sns.barplot(
  x='weekday',
  y='count',
  data=weekday_df,
  palette=warna,
  ax=axes[2])

for index, row in enumerate(weekday_df['count']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright (c) Risna Dwi Indriani 2025')
