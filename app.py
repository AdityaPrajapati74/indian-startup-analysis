import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
df=pd.read_csv("new.csv")
df1=pd.read_csv("real2.csv")
st.set_page_config(layout="wide",page_title="Startup Analysis")

# cleaning data
df['date'] = pd.to_datetime(df['date'], errors='coerce')

df1['Industry Vertical'] = df1['Industry Vertical'].replace(
    {
    "eCommerce": "E-Commerce",
    "FinTech": "Fin-Tech",
    "ECommerce": "E-Commerce",
    "E-commerce": "E-Commerce",
    "Ecommerce": "E-Commerce",
    "":"", },regex=True)

df['InvestmentnType'] = df['InvestmentnType'].replace({
    'Private Equity Round': 'Private Equity',
    'Seed Round': 'Seed Funding',
    'Seed/ Angel Funding': 'Seed / Angel Funding'
})
df1['InvestmentnType'] = df1['InvestmentnType'].replace({
    'Private Equity Round': 'Private Equity',
    'Seed Round': 'Seed Funding',
    'Seed/ Angel Funding': 'Seed / Angel Funding'
})
# Clean Cities
df1['City  Location'] = df1['City  Location'].replace('Bengaluru', 'Bangalore')

# Clean Investment Types (remove extra spaces and handle newlines)
df1['InvestmentnType'] = df1['InvestmentnType'].replace({
    r"Seed\\nFunding": "Seed Funding",
    'Seed / Angel Funding': 'Seed/Angel Funding',
    'Seed/ Angel Funding': 'Seed/Angel Funding',
},regex=True)

df1["investor name"]=df1["investor name"].astype(str)
df5=df1.assign(investor_name = df1["investor name"].str.split(r',| and ')).explode("investor_name")




def startup_recomm(name):
    sta=df1[df["startup name"].str.contains(name)]["SubVertical"]
    recom=df1[df1["SubVertical"].isin(sta)]["startup name"].head()
    return recom




def recommended(name):

    comp_industry=df[df["Investor Name"].str.contains(name)]["Industry Vertical"].value_counts().index

    recom=df[df["Industry Vertical"].isin(comp_industry)]["Investor Name"].head()
    return recom



def load_overall():
    st.title("Overall Analysis")
    col1,col2,col3,col4=st.columns(4)
    #total invested money
    with col1:
        total=round(df1["Rupees in crore"].sum())
        st.metric("Total Invested Money",str(total) + 'Cr')


    #higest investment
    with col2:
        highest=df.groupby("startup name")["Rupees in crore"].max().sort_values(ascending=False).head(1).values[0]
        comp=df.groupby("startup name")["Rupees in crore"].max().sort_values(ascending=False).head(1).index
        st.metric(" Maximum Funding",str(highest) +'Cr' ,delta=str(comp[0]))

    #number of startup
    with col3:
        star=df1["startup name"].unique().size
        st.metric("Total Startup",str(star))
    #mean investments:
    with col4:
        avg=round(df1.groupby("startup name")["Rupees in crore"].sum().mean())
        st.metric("Mean Investment",str(avg)+"Cr")
    st.subheader("MoM startup  (Total funding and Number of startup) ")
    mom_option=st.selectbox("Mom",["Amount Invested","Total Startup Invested"])
    if mom_option=="Amount Invested":
        temp = round(df.groupby(["year", "month"])["Rupees in crore"].sum(), 2).reset_index()
        temp["date_dt"] = pd.to_datetime(temp["year"].astype(str) + "-" + temp['month'].astype(str)+"-01")
        temp = temp.sort_values('date_dt')
        st.line_chart(temp.set_index('date_dt')['Rupees in crore'])
    else:
        temp = df.groupby(["year", "month"])["startup name"].count().reset_index()
        temp=temp.rename(columns={"startup name":"No_of_startup"})
        temp['date_dt'] = pd.to_datetime(temp['year'].astype(str) + '-' + temp['month'].astype(str)+"-01")
        temp = temp.sort_values('date_dt')
        chart_data = temp.set_index('date_dt')[['No_of_startup']]
        st.line_chart(chart_data)

    st.subheader("Sector Analysis(Top-20)")
    sector_option=st.selectbox("Startup",["Startup Sector","Startup Niche (by Count)","Startup Niche (by Amount)"])
    if sector_option=="Startup Sector":
        temp = df1['Industry Vertical'].value_counts().head(20).sort_values()
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(temp.index, temp.values, color='#87CEEB')  # barh = horizontal bars
        ax.set_xlabel('Number of Startups')
        ax.set_title('Top 20 Startup Sectors')
        st.pyplot(fig)
    elif sector_option=="Startup Niche (by Count)":
        temp = df['SubVertical'].value_counts().head(20).sort_values()
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(temp.index, temp.values, color='#87CEEB')  # barh = horizontal bars
        ax.set_xlabel('Number of Startups')
        ax.set_title('Top 20 Startup Sectors')
        st.pyplot(fig)

    else:
        temp = df.groupby("SubVertical")["Rupees in crore"].sum().sort_values(ascending=False).head(20)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(temp.index, temp.values, color='#87CEEB')
        ax.set_xlabel('Total Amount (Rupees in Crore')
        ax.set_title('Top 20 Sectors by Investment Amount')
        st.pyplot(fig)
    col5,col6=st.columns(2)
    with col5:
        st.subheader("Top 5 City with Most Investments")
        city=round(df1.groupby("City  Location")["Rupees in crore"].sum().sort_values(ascending=False).head())
        st.dataframe(city)
    with col6:
        st.subheader("Top 5 Investment Type")
        typ=df1["InvestmentnType"].value_counts().head()
        st.dataframe(typ)
    st.header("Top Funded Startups (Year-wise)")
    option_year=st.selectbox("year",["2015","2016","2018","2019","2020"])
    df1['year'] = df1["year"].astype(str)
    year=round(df1[df1["year"].str.contains(option_year)].groupby("startup name")["Rupees in crore"].sum().sort_values(ascending=False).head(3))
    st.dataframe(year)

    st.subheader("Top 5 Investors by Capital")
    invest=round(df.groupby("Investor Name")["Rupees in crore"].sum().sort_values(ascending=False).head())
    st.dataframe(invest)



def load_startup(name):

    st.title(name)
    col1,col2,col3,col4=st.columns(4)
    with col1:
        total=round(new_df[new_df["startup name"].str.contains(name)].groupby("startup name")["Rupees in crore"].sum().sort_values(ascending=False).values[0],2)
        st.metric("Total Funding",str(total)+"Cr")
    with col2:
        highest=round(new_df[new_df["startup name"].str.contains(name)]["Rupees in crore"].sort_values(ascending=False).head(1).values[0],2)
        st.metric("Highest Investment",str(highest)+"Cr")
    with col3:
        city=new_df[new_df["startup name"].str.contains(name)]["City  Location"].sort_values(ascending=False).head(1).values[0]
        st.metric("City", str(city))
    with col4:
        typ=new_df[new_df["startup name"].str.contains(name)]["InvestmentnType"].sort_values(ascending=False).head(1).values[0]
        st.metric("Investment Type", typ)
    st.subheader("Investor Detail")
    investor_type=df5[df5["startup name"].str.contains(name)][["date", "InvestmentnType", "investor_name"]]
    st.dataframe(investor_type)

    st.subheader("YoY Investment:-")
    amount=df1[df1["startup name"].str.contains(name)].groupby("year")["Rupees in crore"].sum()
    fig, ax = plt.subplots()
    amount.plot(kind='line', marker='o', color='#87CEEB', ax=ax)
    ax.set_title(f"Annual Funding Trajectory:{name}", fontsize=13)
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Amount (Rupees in Crore)")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)
    st.subheader("Similar Startup:-")
    st.dataframe(startup_recomm(name))

def load_investor(name):
    st.title(name)
    last_5 = df[df["Investor Name"].str.contains(name, na=False)][
        ["date", "startup name", "Industry Vertical", "City  Location", "InvestmentnType", "Rupees in crore"]].head()
    st.subheader("Most Recent Investements:-")
    st.dataframe(last_5)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Biggest Investments:-")
        top = df[df['Investor Name'].str.contains(name)].groupby("startup name")["Rupees in crore"].sum().sort_values(
            ascending=False).head()
        st.dataframe(top)
        fig, ax = plt.subplots()
        ax.bar(top.index, top.values)
        st.pyplot(fig)


        st.subheader("Investment Type:-")
        invtype=df[df["Investor Name"].str.contains(name)].groupby("InvestmentnType").count()["startup name"]
        fig, ax = plt.subplots(figsize=(5, 6))
        ax.barh(invtype.index, invtype.values, color='skyblue')
        ax.set_title('Investment Type')
        ax.invert_yaxis()
        st.pyplot(fig)


    with col2:
        st.subheader("Most Invested Startup Segment:-")
        df_copy = df.dropna(subset=["SubVertical", "Rupees in crore"])
        col=df_copy[df_copy["Investor Name"].str.contains(name)].groupby("SubVertical")["Rupees in crore"].sum().sort_values(ascending=False).head()
        st.dataframe(col)
        fig, ax = plt.subplots(figsize=(5, 6))
        ax.barh(col.index, col.values, color='skyblue')
        ax.set_xlabel('Rupees in crore')
        ax.set_ylabel('Startup Segment')
        ax.set_title('Top Startup Segments')
        ax.invert_yaxis()
        st.pyplot(fig)
        st.subheader("Regional Investment Distribution:-")
        cit = df[df["Investor Name"].str.contains(name, na=False)].groupby("City  Location")[
            "date"].count().sort_values(ascending=False).head(10)
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(cit.index, cit.values, color='salmon')
        ax.set_xlabel('Number of Investments')
        ax.set_ylabel('City')
        ax.invert_yaxis()
        st.pyplot(fig)

    st.subheader(" Year On Year Investments:-")
    year_series = df[df["Investor Name"].str.contains(name)].groupby('year')["Rupees in crore"].sum()
    fig, ax = plt.subplots()
    ax.plot(year_series.index.astype(str), year_series.values, marker='o', linestyle='-', color='teal')

    ax.set_xlabel("Year")
    ax.set_ylabel("Amount of Investments")
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

    st.subheader("Similar Investors:-")
    st.dataframe(recommended(name))

st.sidebar.title("Investor Analysis")
option=st.sidebar.selectbox("Select one",["Overall Analysis","Startup Analysis","Investor Analysis"])

if option=="Overall Analysis":
        load_overall()
elif option=="Startup Analysis":
    clean_data = st.checkbox("Show Only Disclosed Investments",help="Check this to remove startups with 'undisclosed' (0) funding values ")
    if clean_data:
        new_df = df1[(df1["Rupees in crore"] != 0) & (df1["City  Location"]!="Undisclosed")].copy()
    else:
        new_df = df1
    startup_name=st.sidebar.selectbox("Startup Name",sorted(new_df["startup name"].unique().tolist()))
    bt1=st.sidebar.button("Startup Detail")
    if bt1:
        load_startup(startup_name)
else:
    investor_name = st.sidebar.selectbox("Investor Name", sorted(set(df["Investor Name"].str.split(",").sum())))
    bt2 = st.sidebar.button("Investor Detail")
    clean=st.checkbox("Clean View (Hide Missing value of Startup segment)",value=True)
    if bt2 or clean:
        load_investor(investor_name)




