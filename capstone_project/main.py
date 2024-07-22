import streamlit as st #type: ignore
import pandas as pd #type: ignore
import numpy as np #type: ignore
import matplotlib.pyplot as plt #type: ignore

df = pd.read_csv("data/quarterly_canada_population.csv")
df.set_index('Quarter', inplace = True)

def parse_quarter(quarter_str):
    quarter, year = quarter_str.split()
    quarter = int(quarter[1])
    year = int(year)

    return quarter, year

st.title("Population of Canada")
st.markdown("Source table can be found [here](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)")

with st.expander("See full data table"):
    st.dataframe(df)

with st.form("key"):
    col1, col2, col3 = st.columns(3)

    col1.write("Choose a starting date")
    start_quarter = col1.selectbox("Quarter", options = ["Q1", "Q2", "Q3", "Q4"], index = 2)
    start_slider = col1.slider("Year", min_value = 1991, max_value = 2023)

    col2.write("Choose an end date")
    end_quarter = col2.selectbox("Quarter", key = 2, options = ["Q1", "Q2", "Q3", "Q4"], index = 0)
    end_slider = col2.slider("Year", key = 3, min_value = 1991, max_value = 2023, value = 2023)

    col3.write("Choose a location")
    location = col3.selectbox("Choose a location", options = df.columns.to_list(), index = 0)    

    Analyze = st.form_submit_button("Analyze")


key_start = (f"{start_quarter} {start_slider}")
key_end = (f"{end_quarter} {end_slider}")

if key_start not in df.index or key_end not in df.index:
    st.error("No data available. Check your quarter and year selection.")
    st.stop()


if ((parse_quarter(key_start)[1] > parse_quarter(key_end)[1]) or
    ((parse_quarter(key_start)[1] == parse_quarter(key_end)[1]) and
        (parse_quarter(key_start)[0] >= parse_quarter(key_end)[0]))):
    st.error("Start date cannot be greater than end date")
    st.stop()

tab1, tab2 = st.tabs(["Population change","Compare"])

with tab1:
    tab1.subheader(f"Population change from {key_start} to {key_end}")

    col1, col2 = st.columns(2)

    col1.metric(label = key_start, value = df.loc[key_start][location])

    delta = 100*(((df.loc[key_end][location] - df.loc[key_start][location]).item())/(df.loc[key_start][location].item()))
    col1.metric(label = key_end, value = df.loc[key_end][location], delta = str(round(delta,2)) + "%")

    fig, ax = plt.subplots()
    ax.plot(df.loc[key_start:key_end].index, df.loc[key_start:key_end, location])
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")

    x_ticks = [df.loc[key_start:key_end].index[0], df.loc[key_start:key_end].index[-1]]
    ax.set_xticks(x_ticks)
    fig.autofmt_xdate()

    col2.pyplot(fig)

with tab2:
    st.subheader("Compare with other locations")

    multiselect = st.multiselect("Choose other locations", options = df.columns.to_list(), default = location)


    fig, ax = plt.subplots()
    for countries in multiselect:
        ax.plot(df.loc[key_start:key_end].index, df.loc[key_start:key_end, countries])
    
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")

    x_ticks = [df.loc[key_start:key_end].index[0], df.loc[key_start:key_end].index[-1]]
    ax.set_xticks(x_ticks)
    fig.autofmt_xdate()

    st.pyplot(fig)
    


