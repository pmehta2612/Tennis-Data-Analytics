-- Competitions API
-- Categories and Competitions Table SQL Queries
-- 1. List all competitions along with their category name
select c.competition_id AS Competition_ID, c.competition_name AS Competition_Name, cat.category_name AS Category
from Competitions c
join Categories cat 
on c.category_id = cat.category_id;
    
-- 2. Count the number of competitions in each category
select cat.category_name AS Category, COUNT(*) AS Total_Competitions
from Competitions c
join Categories cat 
on c.category_id = cat.category_id
group by cat.category_name;

-- 3. Find all competitions of type 'doubles'
select competition_id AS Competition_ID, competition_name AS Competition_Name, type AS Type
from Competitions
where type = 'doubles';

-- 4. Get competitions that belong to a specific category (e.g., ITF Men) 
select c.competition_id AS Competition_ID, c.competition_name AS Competition_Name, cat.category_name As Category
from Competitions c
join Categories cat
on c.category_id = cat.category_id
where cat.category_name = 'ITF Men';

-- 5. Identify parent competitions and their sub-competitions 
select parent.competition_name AS Parent_Competition, child.competition_name AS Sub_Competition
from Competitions child
join Competitions parent 
on child.parent_id = parent.competition_id;

-- 6. Analyze the distribution of competition types by category 
select cat.category_name AS Category, c.type As Type, COUNT(*) AS Competition_Count
from Competitions c
join Categories cat 
on c.category_id = cat.category_id
group by cat.category_name, c.type;

-- 7. List all competitions with no parent (top-level competitions) 
select competition_id As Competition_ID, competition_name AS Competition_Name
from Competitions
where parent_id IS NULL;

