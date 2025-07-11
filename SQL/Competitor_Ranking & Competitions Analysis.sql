-- Double Competitor Ranking API
-- Competitor Ranking and Competitions SQL Queries
-- 1. Get all competitors with their rank and points.
with cte as (
select c.name as Competitor_Name, cr.points as Points,
dense_rank() over (order by points desc) as `Rank`
from competitor_rankings cr
join competitors c
on cr.competitor_id = c.competitor_id
)
select Competitor_Name, Points, `Rank` 
from cte
order by Points desc, `Rank` desc;

-- 2. Find competitors ranked in the top 5 
with cte as (
select c.name as Competitor_Name, cr.points as Points,
dense_rank() over (order by points desc) as `Rank`
from competitor_rankings cr
join competitors c
on cr.competitor_id = c.competitor_id
)
select Competitor_Name, Points, `Rank` 
from cte
where `Rank` <= 5
order by Points desc, `Rank` desc;

-- 3. List competitors with no rank movement (stable rank) 
select c.name as Competitor_Name, cr.movement as Movement,
row_number() over(order by c.name) as Row_Num
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
where country != "Neutral"
group by country
order by Competitor_Count desc;

-- 6. Find competitors with the highest points in the current week
select c.name as Competitor_Name, cr.points as Points
from competitors c
join competitor_rankings cr
on c.competitor_id = cr.competitor_id
where cr.points in (
select max(points) from competitor_rankings
);
