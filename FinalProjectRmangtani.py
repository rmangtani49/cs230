"""
Class: CS230--Section 1
Name: Rohit Mangtani
Description: (Final Project - Skycraper Dataset)
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
# Importing packages for use
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# getdata function reads the csv file into a data frame, renames columns for later use within streamlit and drops unused columns; returns the data frame
def getdata():
    df = pd.read_csv('Skyscrapers2021.csv')
    df = df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})
    df = df.drop(["Link", "FUNCTION"], axis=1)
    return df

# creates a list of names for the dropdown list, for later use in main function to call certain functions
droplist = ['Graph by Build Year', 'Distribute by Building Material', 'Map the Skycrapers by City', 'Display a Pivot Table and Graph of Average Floors Per City']
st.title("Skyscraper Analysis")

# pivot table function that drops columns not used in pivot table and graphs a bar plot using seaborn
def pivottable(data):
    z = data.drop(["latitude", "longitude", "COMPLETION", "RANK"], axis=1)
    x = pd.pivot_table(z, index=["CITY"])
    sns.barplot(x="NAME", y="FLOORS", data=z).set(xlabel="", xticklabels=[])
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    return x

# completionbar function that sorts completion in ascending order, then takes values based on the select box and filters specific years
def completionbar(data, selection_year=1931):
    df = data.sort_values(by=["COMPLETION"], ascending=True)
    completions = df['COMPLETION'].values.tolist()
    dict = {}
    for value in completions:
        if value not in dict:
            if value >= selection_year:
                dict[value] = 1
        else:
            dict[value] += 1
    y_val = dict.values()
    x_years = dict.keys()
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(x_years, y_val)
    plt.xlabel("Years")
    plt.ylabel("Number of Buildings")
    return plt

# map function that takes in the dataframe and will display all the skyscrapers and only show specified locations
def map(data):
    newlist = list(data['CITY'])
    finallist = []
    for i in newlist:
        if i not in finallist:
            finallist.append(i)
    options = st.sidebar.selectbox("Select a City", finallist)
    latlon = st.sidebar.checkbox("Click to toggle zoom into the selected city")
    if latlon:
        df1 = pd.DataFrame(data[data['CITY'] == options])
        df2 = pd.DataFrame(df1, columns=['latitude', 'longitude'])
        st.map(df2)
    else:
        df2 = pd.DataFrame(data, columns=['latitude', 'longitude'])
        st.map(df2)

# pie chart that shows the distribution of the buildings based on the construction material
def pie(data):
    materials = data['MATERIAL'].values.tolist()
    dict = {}
    x = []
    y = []
    materials.sort()
    materials = [material.capitalize() for material in materials]
    for value in materials:
        if value not in dict:
            dict[value] = 1
        else:
            dict[value] += 1
    for i, j in dict.items():
        x.append(i)
        y.append(j)
    plt.pie(y, autopct='%1.2f%%', shadow=True)
    plt.legend(x)
    return plt

# main function with no return that executes each part of the code based on an if else statement
def main():
    option = st.selectbox("Select an option below", droplist)
    if option == "Graph by Build Year":
        st.title("Graph of Build Year with Slider")
        yearslider = getdata()['COMPLETION'].values.tolist()
        x = st.slider("Enter Your Desired Start Year", min_value=min(yearslider), max_value=max(yearslider))
        x = int(x)
        st.pyplot(completionbar(getdata(), x))
    elif option == "Distribute by Building Material":
        st.title("Pie Chart of Building Material Distribution")
        df = getdata()
        st.pyplot(pie(df))
    elif option == "Map the Skycrapers by City":
        st.title("Map of Skycrapers by City")
        df = getdata()
        map(df)
    elif option == "Display a Pivot Table and Graph of Average Floors Per City":
        st.title("Pivot Table and Graph of Average Floors Per City")
        st.dataframe(pivottable(getdata()))
    st.write("Made by Rohit Mangtani")


# main function call
main()
