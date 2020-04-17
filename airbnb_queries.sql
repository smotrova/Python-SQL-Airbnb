-- how many records in a table
select count(*) as nrows from airbnb_search_details;

-- how many unique records in a table
select distinct count(*) as nrows from airbnb_search_details;

-- Find out the searches made by the people who search for apartments where they will be the sole person staying.
-- Table: airbnb_search_details

select count(id) from airbnb_search_details
where accommodates=1 and beds=1;

-- Find 50 searches for apartments in New York City which are in the Harlem neighborhood.
-- Table: airbnb_search_details

select * from airbnb_search_details
where city = 'NYC' and neighbourhood = 'Harlem'
limit 50;

-- Find all searches where the number of bedrooms is equal to the number of bathrooms.
-- Table: airbnb_search_details

select * from airbnb_search_details
where bathrooms = bedrooms;

-- Find Los Angeles neighborhoods for which searches exist.
-- Table: airbnb_search_details

select distinct neighbourhood from airbnb_search_details
where city='LA'
order by neighbourhood;

-- Make a pivot table which shows the number of searches per city and room type. Rows are different cities while columns are different room types:
-- Table: airbnb_search_details

select distinct room_type, count(*) as quantity from airbnb_search_details
group by room_type;

select
       count(case when room_type = 'Entire home/apt' then room_type end) as entire_property,
       count(case when room_type = 'Private room' then room_type end) as privat_room,
       count(case when room_type = 'Shared room' then room_type end) as shared_room
from airbnb_search_details;

select city, room_type, count(*) as quantity from airbnb_search_details
group by city, room_type;

select city,
       count(case when room_type = 'Entire home/apt' then room_type end) as entire_property,
       count(case when room_type = 'Private room' then room_type end) as privat_room,
       count(case when room_type = 'Shared room' then room_type end) as shared_room
from airbnb_search_details
group by city;

-- Find all searches where the `host_response_rate` column is missing data.
-- Table: airbnb_search_details

select distinct host_response_rate from airbnb_search_details;

select * from airbnb_search_details
where host_response_rate = '';

-- Find all searches for San Francisco with flexible cancellation policies and which have a review score value. Ordered by the review score from highest to lowest.
-- Table: airbnb_search_details

select * from airbnb_search_details
where city = 'SF' and cancellation_policy = 'flexible'
order by review_scores_rating desc, id desc;

-- Find all houses and villas which have internet access but no wireless internet access.
-- Table: airbnb_search_details

select * from airbnb_search_details
where (amenities not like '%Wireless Internet%') and 
    (amenities like '%Internet%') and
    property_type in ('Villa','House');
    
-- Find the price of the cheapest property for every city.
-- Table: airbnb_search_details

select city, min(log_price) from airbnb_search_details
group by city;

-- Find all neighbourhoods present in this dataset.
-- Table: airbnb_search_details

select distinct neighbourhood from airbnb_search_details;

-- Find the search for each city which has the highest number of amenities. Estimate the number of amenities as the number of characters in the `amenities` column.
-- Table: airbnb_search_details

select city, max(amenities_number) from (
select city, length(amenities) as amenities_number from airbnb_search_details)
group by city
order by 2 desc;

-- Find the price of the most expensive beach properties for each city.

SELECT
    city,
    MAX(log_price)
FROM airbnb_search_details
WHERE description LIKE '%beach%'
GROUP BY city;

-- Find the average number of beds in neighbourhoods in which no property has less than 3 beds.
-- Table: airbnb_search_details

select neighbourhood, avg(beds) from airbnb_search_details
group by neighbourhood
having min(beds) > 3;

-- It is time for your vacation. You need to chose which city to visit. You don't have much money so you decide to stay in a shared room, but you want to share the room with as little people as possible. You devise a score which tells you the average number of persons accomodated by the shared room over the average number of beds available for each city and order the choice of cities by that score. 

-- Table: airbnb_search_details

select city, avg(accommodates)/AVG(beds) from airbnb_search_details
where room_type='Shared room'
group by city
order by crowdness_ratio asc;

-- Find all neighbourhoods where there are properties which have no cleaning fees and have parking space.
-- Table: airbnb_search_details
select distinct neighbourhood from airbnb_search_details
where (amenities like '%parking%') and (cleaning_fee = 'FALSE');


-- How many hosts are verified by AirBnB staff? How many aren't?
-- Table: airbnb_search_details

select distinct host_identity_verified from airbnb_search_details;

select 
    count(case when host_identity_verified = 't' then host_identity_verified end) as verified,
    count(case when host_identity_verified = 'f' then host_identity_verified end) as not_verified,
    count(case when host_identity_verified = '' then host_identity_verified end) as no_information
from airbnb_search_details;

select host_identity_verified, count(host_identity_verified) from airbnb_search_details
group by host_identity_verified; 

-- Find the first 5 entries by joining search details and contacts datasets.
-- Tables: airbnb_contacts, airbnb_searches

select * from airbnb_searches as asd left join airbnb_contacts as ac
on asd.id_user = ac.id_guest and asd.ds_checkin=ac.ds_checkin and asd.ds_checkout=ac.ds_checkout
limit 5;

-- Which gender is more generous in giving positive reviews when considering only guest reviewers?
-- Tables: airbnb_reviews, airbnb_guests

select gender,  
case 
    when review_score > 5 then 'positive'
    when review_score <= 5 then 'negative'
end as review,
count(review_score) from (
    select * from
    airbnb_reviews as r left join airbnb_guests as g
    on r.from_user = g.guest_id
    where r.from_type='guest')
group by gender, review;

-- Each guest reviews multiple hosts. What is the top rated hosts' nationality for each guest reviewer?
-- Tables: airbnb_reviews, airbnb_hosts

select from_user, nationality from (
    select * from
    airbnb_reviews as r left join airbnb_hosts as h
    on r.to_user=host_id
    )
where to_type='host' and review_score = 10
group by from_user, nationality;

-- How many hosts have apartments in countries of which they are not citizens?
-- Tables: airbnb_hosts, airbnb_apartments

select count(*) as hosts from (
    select * from airbnb.airbnb_apartments as a inner join airbnb_hosts as h
    on a.host_id=h.host_id
    )
where country <> nationality;

-- Each host reviews multiple guests. What is the average age of guests reviewed by each host?
-- Tables: airbnb_reviews, airbnb_guests

select from_user, avg(age)as average_age from (
    select * from 
        airbnb_reviews as r join airbnb_guests as g
        on r.to_user=g.guest_id
   where from_type='host'
)

group by from_user;

-- Make a pivot table that shows the total number of searches for each room type based on the city. Output should have 4 columns that include the name of the city, apartment count, private room count, and shared room count.
-- Table: airbnb_search_details

select city,
    count(case when room_type='Entire home/apt' then room_type end) as 'Entire home/apt',
    count(case when room_type='Private room' then room_type end) as 'Private room',
    count(case when room_type='Shared room' then room_type end) as 'Shared room'
from airbnb_search_details
group by city;
    
-- Find neighborhoods where you can sleep on a real bed in a villa with beach access while paying the minimum price possible. 
-- Table: airbnb_search_details

select log_price, neighbourhood from airbnb_search_details
where (bed_type = 'Real Bed') and (description like '% beach %') and (property_type='Villa') and log_price in (
    select min(log_price) from airbnb_search_details
    where (log_price > 0) and (bed_type = 'Real Bed') and (description like '% beach %') and (property_type='Villa'));
    
-- Find the number of searches made by each user and present the result with their corresponding user id.
-- Table: airbnb_searches
select id_user, count(id_user) from  airbnb_searches
group by id_user;

-- Display the number of times a user performed a search which led to a successful booking and the number of times a user performed a search but did not lead to a booking. The output should have a column named action with values 'does not book' and 'books' as well as a 2nd column named average_searches with the average number of searches per action. Consider that the booking did not happen if the booking date is null.
-- Tables: airbnb_searches, airbnb_contacts

select id_user, 
case
    when ts_booking_at is NULL then 'does not book'
    when ts_booking_at is not NULL then 'books'
end as actions, avg(n_searches) as average_searches from(
    select * from airbnb_searches as asd left join airbnb_contacts as ac
    on asd.id_user = ac.id_guest and asd.ds_checkin=ac.ds_checkin and asd.ds_checkout=ac.ds_checkout
    )
group by id_user, actions;


-- How many unique users have performed a search?
-- Table: airbnb_searches
select count(*) as number_of_users from (
    select distinct id_user from airbnb_searches
    );
    
-- Find how many the number of different property types in the dataset.    
-- Table: airbnb_searches

select count(*) from
    (select distinct room_types_cleaned from (
        select filter_room_types, 
        case 
             when filter_room_types like ',%' then ltrim(filter_room_types,',')
             when filter_room_types not like ',%' then filter_room_types
        end as room_types_cleaned from airbnb_searches)
    );