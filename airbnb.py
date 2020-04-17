''' AirBnB '''

import pandas as pd
import numpy as np

airbnb = pd.read_csv('./data/airbnb_search_details.csv')

# =============================================================================
# Find out the searches made by the people who search for apartments 
# where they will be the sole person staying.
# =============================================================================
airbnb.loc[(airbnb.accommodates==1)&(airbnb.beds==1), 'id']

# =============================================================================
# Find 50 searches for apartments in New York City which are 
# in the Harlem neighborhood.
# =============================================================================
airbnb[(airbnb.city =='NYC') & (airbnb.neighbourhood == 'Harlem')][:50]

# =============================================================================
# Find all searches where the number of bedrooms is equal 
# to the number of bathrooms.
# =============================================================================
airbnb[airbnb.bedrooms == airbnb.bathrooms]

# =============================================================================
# Find Los Angeles neighborhoods for which searches exist.
# =============================================================================
airbnb.loc[airbnb.city == 'LA', 'neighbourhood'].sort_values().unique()

# =============================================================================
# Make a pivot table which shows the number of searches per city 
# and room type. Rows are different cities 
# while columns are different room types
# =============================================================================
pd.crosstab(index = airbnb.city, columns = airbnb.room_type)

# =============================================================================
# Find all searches where the `host_response_rate` 
# column is missing data.
# =============================================================================
airbnb[airbnb.host_response_rate.isna()]

# =============================================================================
# Find all searches for San Francisco with 
# flexible cancellation policies and which have a review score value. 
# Ordered by the review score from highest to lowest.
# 
# =============================================================================
f = (airbnb.city == 'SF') & (airbnb.cancellation_policy == 'flexible')
airbnb[f].sort_values(by=['review_scores_rating', 'id'], ascending=False, axis=0)


# =============================================================================
# Find all houses and villas which have internet access 
# but no wireless internet access.
# =============================================================================
f = airbnb.amenities.apply(lambda x: 'Wireless Internet' not in x 
                           and 'Internet' in x) 

h = (airbnb.property_type == "House") | (airbnb.property_type == "Villa") 

airbnb[f&h]

# =============================================================================
# Find the price of the cheapest property for every city.
# =============================================================================
airbnb.groupby('city')['log_price'].min()

# =============================================================================
# Find all neighbourhoods present in this dataset.
# =============================================================================
airbnb.neighbourhood.unique()

# =============================================================================
# Find the search for each city which has the highest number of amenities.
# Estimate the number of amenities as the number of characters 
# in the `amenities` column.
# =============================================================================
airbnb['amenities_len'] = airbnb.amenities.apply(len)
airbnb.groupby(airbnb.city)['amenities_len'].max().sort_values(ascending=False)

# =============================================================================
# Fix the `host_since` column using string processing to be a valid DATE.
# =============================================================================
airbnb.loc[:, 'host_since'] = pd.to_datetime(airbnb.host_since)

# =============================================================================
# Find the price of the most expensive beach properties for each city.
# =============================================================================
f = airbnb.description.str.lower().apply(lambda x: 'beach' in x)
airbnb[f].groupby('city')['log_price'].max()

# =============================================================================
# Find the average number of beds in neighbourhoods in which
# no property has less than 3 beds.
# =============================================================================

# find min number of beds per neighbourhood
df = airbnb.groupby(['neighbourhood'])['beds'].min()

# find neighbourhoods in which no property has less yhan 3 beds
nbrhd = df[df>3].index

# filter for neighbourhoods
f = airbnb.neighbourhood.apply(lambda x: x in nbrhd)

# choose properties for selected neighbourhood
airbnb[f].groupby(['neighbourhood'])['beds'].mean()

# =============================================================================
# It is time for your vacation. You need to chose which city to visit. 
# You don't have much money so you decide to stay in a shared room, 
# but you want to share the room with as little people as possible. 
# You devise a score which tells you the average number of persons 
# accomodated by the shared room over the average number of beds 
# available for each city and order the choice of cities by that score. 
# =============================================================================
df = airbnb[airbnb.room_type == 'Shared room'].groupby(['city'])[['accommodates', 'beds']].mean()
(df.accommodates/df.beds).sort_values(ascending=True)

# =============================================================================
# Find all neighbourhoods where there are properties which 
# have no cleaning fees and have parking space.
# =============================================================================
f = (airbnb.amenities.str.contains('parking', case=False, regex=False)) & (airbnb.cleaning_fee == False)
airbnb.loc[f, 'neighbourhood'].unique()

# =============================================================================
# How many hosts are verified by AirBnB staff? How many aren't?
# =============================================================================
airbnb.host_identity_verified.value_counts(dropna=False)

# =============================================================================
# Find the number of different property types in the dataset.    
# =============================================================================
airbnb.property_type.unique().shape




# =============================================================================
# Load more tabels
# =============================================================================
searches = pd.read_csv('./data/airbnb_searches.csv')
contacts = pd.read_csv('./data/airbnb_contacts.csv')
reviews = pd.read_csv('./data/airbnb_reviews.csv')
guests = pd.read_csv('./data/airbnb_guests.csv')
hosts = pd.read_csv('./data/airbnb_hosts.csv')
apartments = pd.read_csv('./data/airbnb_apartments.csv')

# =============================================================================
# -- Find the first 5 entries by joining search details and contacts datasets.
# -- Tables: airbnb_contacts, airbnb_searches
# =============================================================================
searches.merge(contacts, how='left', 
                         left_on=['id_user','ds_checkin','ds_checkout'], 
                         right_on=['id_guest','ds_checkin','ds_checkout']).iloc[0:5, :]

# =============================================================================
# -- Which gender is more generous in giving positive reviews when considering only guest reviewers?
# -- Tables: airbnb_reviews, airbnb_guests
# =============================================================================
df = reviews.merge(guests, left_on='from_user', right_on='guest_id', how='left')
df=df[df.from_type=='guest']

df.loc[:, 'review'] = df['review_score'].apply(lambda x: 'positive' if x>5 else 'negative')
df.groupby(['gender', 'review'])['review_score'].count()

# =============================================================================
# -- Each guest reviews multiple hosts. What is the top rated hosts' nationality
# for each guest reviewer?
# -- Tables: airbnb_reviews, airbnb_hosts
# =============================================================================

# subsettig guest reviews
df = reviews[reviews.to_type=='host'].merge(hosts, left_on='to_user', right_on='host_id', how='left')

# top rated hosts
top_hosts = df[df.review_score==df.review_score.max()]

# top rated hosts' nationality for each reviewer
top_hosts.groupby(['from_user', 'review_score'])['nationality'].unique().apply(lambda x: ', '.join(x))

# =============================================================================
# How many hosts have apartments in countries of which they are not citizens?
# Tables: airbnb_hosts, airbnb_apartments
# =============================================================================
df = apartments.merge(hosts, on='host_id')
(df.nationality != df.country).sum()

# =============================================================================
# Each host reviews multiple guests. What is the average age of guests reviewed by each host?
# Tables: airbnb_reviews, airbnb_guests
# =============================================================================
df=reviews.merge(guests, left_on='to_user', right_on='guest_id', how='inner')
df[df.from_type=='host'].groupby('from_user')['age'].mean()
    
# =============================================================================
# Make a pivot table that shows the total number of searches for each room type
# based on the city. Output should have 4 columns that include 
#the name of the city, apartment count, private room count, and shared room count.
# Table: airbnb_search_details
# =============================================================================
pd.pivot_table(airbnb, values=['id'], 
               columns=['room_type'], 
               index=['city'], 
               aggfunc='count').reset_index()

# =============================================================================
# Find neighborhoods where you can sleep on a real bed in a villa with beach 
# access while paying the minimum price possible. 
# Table: airbnb_search_details
# =============================================================================
f = (airbnb.log_price>0) & \
    (airbnb.bed_type=='Real Bed') & \
    (airbnb.property_type=='Villa') & \
    (airbnb.description.apply(lambda x: 'beach' in x.lower()))

df = airbnb[f]
df.loc[df.log_price==df.log_price.min(), 'neighbourhood']

# =============================================================================
# Find the number of searches made by each user and present 
# the result with their corresponding user id.
# Table: airbnb_searches
# =============================================================================
searches.groupby('id_user')['id_user'].count().reset_index()

# =============================================================================
# Display the number of times a user performed a search which led to 
# a successful booking and the number of times a user performed a search 
# but did not lead to a booking. The output should have a column named action 
# with values 'does not book' and 'books' as well as a 2nd column named 
# average_searches with the average number of searches per action. 
# Consider that the booking did not happen if the booking date is null.
# Tables: airbnb_searches, airbnb_contacts
# =============================================================================

# join two tables
df=searches.merge(contacts, how='left',
                              left_on=['id_user','ds_checkin','ds_checkout'], 
                              right_on=['id_guest','ds_checkin','ds_checkout'])
# create a new column that is a categorical variable containing booking/not booking values
df['action'] = ''
df.loc[df.ts_booking_at.isna(), 'action']='does not book'
df.loc[~df.ts_booking_at.isna(), 'action']='books'

df.groupby(['id_user', 'action'])['n_searches'] \
    .agg(average_searches=('n_searches', 'mean')) \
    .reset_index('action')
    
# =============================================================================
# How many unique users have performed a search?
# Table: airbnb_searches    
# =============================================================================

searches.id_user.unique().shape

# =============================================================================
# Find how many the number of different property types in the dataset.    
# Table: airbnb_searches
# =============================================================================

searches.filter_room_types.str.lstrip(to_strip=',').unique().shape[0]