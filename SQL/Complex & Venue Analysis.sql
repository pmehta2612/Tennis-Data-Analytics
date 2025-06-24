-- Complexes API
-- Complex and Venue Table SQL Queries
-- 1. List all venues along with their associated complex name 
select v.venue_id as Venue_ID, v.venue_name as Venue_Name, c.complex_name as Complex_Name
from venues v
join complexes c
on v.complex_id = c.complex_id;

-- 2. Count the number of venues in each complex 
select c.complex_name as Complex_Name, count(v.venue_id) as Total_Venues
from venues v
join complexes c
on v.complex_id = c.complex_id
group by c.complex_name;

-- 3. Get details of venues in a specific country (e.g., Chile)
select *
from venues
where country_name = 'Chile'; 
-- 4. Identify all venues and their timezones 
select venue_name as Venue_Name, timezone as TimeZone
from venues;
-- 5. Find complexes that have more than one venue 
select c.complex_name, count(v.venue_id) as Venue_Count
from complexes c
join venues v
on c.complex_id = v.complex_id
group by c.complex_name
having count(v.venue_id) > 1;

-- 6. List venues grouped by country 
select country_name, GROUP_CONCAT(venue_name SEPARATOR ', ') AS venues
from venues
group by country_name;

-- 7. Find all venues for a specific complex (e.g., Nacional)
select v.venue_id as Venue_ID, v.venue_name as Venue_Name, v.city_name as City, v.country_name as Country
from venues v
join complexes c
on v.complex_id = c.complex_id
where c.complex_name = 'Nacional';

