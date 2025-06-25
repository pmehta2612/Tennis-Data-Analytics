-- Double Competitor Ranking API
-- Competitor Ranking and Competitions SQL Queries
-- 1. Get all competitors with their rank and points.
select c.name as Competitor_Name, cr.rank as `Rank`, cr.points as Points
from competitor_rankings cr
join competitors c
on cr.competitor_id = c.competitor_id;

-- 2. Find competitors ranked in the top 5 
select c.name as Competitor_Name, cr.rank as `Rank`, cr.points as Points
from competitor_rankings cr
join competitors c
on cr.competitor_id = c.competitor_id
where cr.rank <= 5
order by cr.rank;

-- 3. List competitors with no rank movement (stable rank) 
select c.name as Competitor_Name, cr.rank as `Rank`, cr.movement as Movement
from competitor_rankings cr
join competitors c
on cr.competitor_id = c.competitor_id
where cr.movement = 0;

-- 4. Get the total points of competitors from a specific country (e.g., Croatia) 
select c.country as Country, sum(cr.points) as Total_Points
from competitors c
join competitor_rankings cr
on c.competitor_id = cr.competitor_id
where c.country = 'Croatia';

-- 5. Count the number of competitors per country 
select country as Country, count(*) as Competitor_Count
from competitors 
group by country;

-- 6. Find competitors with the highest points in the current week
select c.name as Competitor_Name, cr.points as Points
from competitors c
join competitor_rankings cr
on c.competitor_id = cr.competitor_id
where cr.points in (
select max(points) from competitor_rankings
);
