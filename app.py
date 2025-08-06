import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# Set the title of the app
st.set_page_config(page_title='Vehicle Data Analysis', layout='wide')
# Add a title to the app
st.title('Vehicle Data Analysis')
# create a text header above the dataframe
st.header('Data viewer') 

# Add a checkbox to filter manufacturers with less than 1000 ads 
show_manuf_1k_ads = st.checkbox('Include manufacturers with less than 1000 ads')
if not show_manuf_1k_ads:
    df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)
# display the dataframe with streamlit
st.dataframe(df)


########## VEHICLE PRICE BY TYPE ###########
st.header('Vehicle price by type')
# create a plotly histogram figure
fig = px.histogram(df, x='price', color='type')
# display the figure with streamlit
st.write(fig)

############ DAYS LISTED BY TYPE #############
st.header('Histogram of `days_listed` vs `type`')
fig = px.histogram(df, x='days_listed', color='type')
st.write(fig)

########## COMPARE DISTRIBUTION OF PAINT_COLOR BY MODEL_YEAR ##########
# Replace NaN in model_year with the median model_year for each model
df['model_year'] = df['model_year'].fillna(
    df.groupby('model')['model_year'].transform('median')
)
# Fill any remaining NaN in model_year with overall median before converting to int
df['model_year'] = df['model_year'].fillna(df['model_year'].median())
df['model_year'] = pd.to_numeric(df['model_year'], errors='coerce').astype(int)

# Change NaN values in paint_color to 'unknown'
df['paint_color'] = df['paint_color'].fillna('unknown')


# create a plotly histogram figure
st.header('Compare distribution OF paint color by year')
# get a list of car manufacturers
colors = sorted(df['paint_color'].unique())
# get user's inputs from a dropdown menu
color_1 = st.selectbox(
                              label='Select Color 1', # title of the select box
                              options=colors, # options listed in the select box
                              index=colors.index('red') # default pre-selected option
                              )
# repeat for the second dropdown menu
color_2 = st.selectbox(
                              label='Select Color 2',
                              options=colors, 
                              index=colors.index('black')
                              )
# filter the dataframe 
mask_filter = (df['paint_color'] == color_1) | (df['paint_color'] == color_2)
df_filtered = df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='model_year',
                      nbins=30,
                      color='paint_color',
                      histnorm=histnorm,
                      barmode='overlay')
# display the figure with streamlit
st.write(fig)