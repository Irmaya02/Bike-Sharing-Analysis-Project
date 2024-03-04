import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
# sns.st(style='dark')

# Load cleaned data
hour_df = pd.read_csv("https://raw.githubusercontent.com/Irmaya02/Bike-Sharing-Analysis-Project/main/Dashboard/bike_hour_clean.csv")
datetime_columns = ["dateday"]
hour_df.sort_values(by="dateday", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date = hour_df["dateday"].min()
max_date = hour_df["dateday"].max()

with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://github.com/Irmaya02/Bike-Sharing-Analysis-Project/blob/main/Dashboard/bike.png?raw=true" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )

    start_date, end_date = st.date_input(
        label="Date Range",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["dateday"] >= str(start_date)) & 
                (hour_df["dateday"] <= str(end_date))]

st.header("Bike-Sharing Dashboard :sparkles:")
st.markdown("#### Bicycle Rental")

col1, col2 = st.columns(2)

with col1:
    total_transaction = hour_df['count'].count()
    st.metric("Total Transaction", value=total_transaction)

with col2:
    total_rent = hour_df['count'].sum() 
    st.metric("Total Bikes Rented", value=total_rent)

# Definisikan fungsi untuk customer type
def customer_type(hour_df):
    total_casual = hour_df["casual"].sum()
    total_registered = hour_df["registered"].sum()

    labels = ["Casual", "Registered"]
    sizes = [total_casual, total_registered]
    colors = ["#7C94A5", "#16355F"]

    # Plot Pie Chart
    plt.figure(figsize=(6, 4))
    plt.pie(sizes, labels=labels, colors=colors, autopct="%1.2f%%")
    plt.title("Bike-Sharing Distribution by Customer Type")
    plt.axis("equal")

    # Tampilkan pie chart menggunakan Streamlit
    st.pyplot(plt)

def distribution_customer(hour_df):
    # Columns to plot
    columns = ["casual", "registered", "count"]

    # Create a figure with 3 subplots, each representing a bar chart for one of the columns
    fig, ax = plt.subplots(1, 3, figsize=(20, 5))  

    # Loop through each subplot and plot the bar chart
    for i, column in enumerate(columns):
        sns.barplot(x="month", y=column, data=hour_df, ax=ax[i], estimator=sum, ci=None, color="#16355F")  
        ax[i].set_title(column)
        ax[i].set_xlabel("Month")
        ax[i].set_ylabel("Total Count")
        ax[i].set_xticklabels(ax[i].get_xticklabels(), rotation=45)
    
    # Display the plot using Streamlit
    st.pyplot(fig)

def bike_sharing_perHour(hour_df):
    # Menghitung jumlah pelanggan pada setiap jam
    hourly_counts = hour_df.groupby('hour')['count'].sum().reset_index()

    # Plot barplot
    colors = ["#16355F"]
    plt.figure(figsize=(10, 6))
    sns.barplot(x="hour", y="count", data=hourly_counts, palette=colors)
    plt.plot(hourly_counts["hour"], hourly_counts["count"], color="#7C94A5", marker="o", linestyle="-")
    plt.title("Bike-Sharing Distribution per Hour in a Day")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Bike Rental Count")
    plt.grid(True, axis="y")

    # Tampilkan grafik menggunakan Streamlit
    st.pyplot(plt)

def by_workingday_and_holiday(hour_df):
    # Group data by 'workingday' and 'year', and aggregate the 'count' column by sum
    working_counts = hour_df.groupby(by=["workingday", "year"]).agg({"count": "sum"}).reset_index()

    # Group data by 'holiday' and 'year', and aggregate the 'count' column by sum
    holiday_counts = hour_df.groupby(by=["holiday", "year"]).agg({"count": "sum"}).reset_index()

    # Set up the figure and axis
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Specify the colors for the bars
    colors = ["#7C94A5", "#16355F"]

    # Plot the barplot for workingday
    sns.barplot(data=working_counts, x="workingday", y="count", hue="year", palette=colors, ax=axes[0])
    axes[0].set_ylabel("Bike Rental Count")
    axes[0].set_xlabel("Workingday")
    axes[0].set_title("Bike-Sharing Distribution by Workingday")
    axes[0].legend(title="Year", loc="upper right")  

    # Plot the barplot for holiday
    sns.barplot(data=holiday_counts, x="holiday", y="count", hue="year", palette=colors, ax=axes[1])
    axes[1].set_ylabel("Bike Rental Count")
    axes[1].set_xlabel("Holiday")
    axes[1].set_title("Bike-Sharing Distribution by Holiday")
    axes[1].legend(title="Year", loc="upper right")  

    plt.tight_layout()

    # Tampilkan grafik menggunakan Streamlit
    st.pyplot(fig)

def rfm_analysis_registered(hour_df):
    # Group data by "registered" and calculate RFM metrics
    rfm_df = hour_df.groupby(by="registered", as_index=False).agg({
        "id_data": "count",  # Frequency
        "count": "max",      # Monetary
        "dateday": lambda x: (pd.Timestamp.now() - x.max()).days  # Recency
    })
    rfm_df.columns = ["registered", "frequency", "monetary", "recency"]
    
    # Create subplots
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    # Specify colors for the barplots
    colors = ["#16355F", "#16355F", "#16355F", "#16355F", "#16355F"]

    # Plot barplot for Recency
    sns.barplot(y="recency", x="registered", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis ='x', labelsize=15)

    # Plot barplot for Frequency
    sns.barplot(y="frequency", x="registered", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)

    # Plot barplot for Monetary
    sns.barplot(y="monetary", x="registered", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title("By Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)

    # Set main title
    plt.suptitle("Best Customer Based on RFM Parameters (Registered)", fontsize=20)

    # Display the plot using Streamlit
    st.pyplot(fig)

def rfm_analysis_casual(hour_df):
    # Group data by "casual" and calculate RFM metrics
    rfm_df = hour_df.groupby(by="casual", as_index=False).agg({
        "id_data": "count",  # Frequency
        "count": "max",      # Monetary
        "dateday": lambda x: (pd.Timestamp.now() - x.max()).days  # Recency
    })
    rfm_df.columns = ["casual", "frequency", "monetary", "recency"]
    
    # Create subplots
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

    # Specify colors for the barplots
    colors = ["#16355F", "#16355F", "#16355F", "#16355F", "#16355F"]

    # Plot barplot for Recency
    sns.barplot(y="recency", x="casual", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis ='x', labelsize=15)

    # Plot barplot for Frequency
    sns.barplot(y="frequency", x="casual", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15)

    # Plot barplot for Monetary
    sns.barplot(y="monetary", x="casual", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title("By Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15)

    # Set main title
    plt.suptitle("Best Customer Based on RFM Parameters (Casual)", fontsize=20)

    # Display the plot using Streamlit
    st.pyplot(fig)


def bike_sharing_trend(hour_df):
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Ubah tipe data kolom 'month' menjadi kategori dengan urutan yang diinginkan
    hour_df['month'] = pd.Categorical(hour_df['month'], categories=month_names, ordered=True)

    # Buat pivot table untuk tahun 2011 dan 2012
    pivot_2011 = hour_df[hour_df["year"] == 2011].pivot_table(index='month', values='count', aggfunc='sum')
    pivot_2012 = hour_df[hour_df["year"] == 2012].pivot_table(index='month', values='count', aggfunc='sum')

    # Sort index agar bulan terurut secara kronologis
    pivot_2011 = pivot_2011.reindex(month_names)
    pivot_2012 = pivot_2012.reindex(month_names)

    # Line Chart
    plt.figure(figsize=(10, 5))
    plt.plot(pivot_2012.index, pivot_2012.values, marker="o", linestyle="-", color="#16355F", label="2012")
    plt.plot(pivot_2011.index, pivot_2011.values, marker="o", linestyle="-", color="#7C94A5", label="2011")
    plt.xlabel("Month")
    plt.ylabel("Total Count")
    plt.title("Trend of Bike-Sharing Rental")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

    # Tampilkan grafik menggunakan Streamlit
    st.pyplot(plt)

# Panggil fungsi untuk menampilkan grafik
st.subheader("Bike-Sharing Distribution by Customer Type")
customer_type(hour_df)
st.markdown("##### Distribution Customer")
distribution_customer(hour_df)

st.subheader("Bike-Sharing Distribution per Hour in a Day")
bike_sharing_perHour(hour_df)

st.subheader("Bike-Sharing Distribution by Workingday & Holiday")
by_workingday_and_holiday(hour_df)

st.subheader("Trend of Bike-Sharing Rental")
bike_sharing_trend(hour_df)

st.subheader("RFM Analysis")
st.markdown("##### Registered")
rfm_analysis_registered(hour_df)
st.markdown("##### Casual")
rfm_analysis_casual(hour_df)

st.caption("Copyright © Irmaya Salsabila 2024")