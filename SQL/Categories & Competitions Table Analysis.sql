-- Competitions API
-- Categories and Competitions Table SQL Queries
-- 1. List all competitions along with their category name
SELECT 
    c.competition_id AS Competition_ID,
    c.competition_name AS Competition_Name,
    cat.category_name AS Category
FROM 
    Competitions c
JOIN 
    Categories cat 
    ON c.category_id = cat.category_id;
    
-- 2. Count the number of competitions in each category
SELECT 
    cat.category_name AS Category,
    COUNT(*) AS Total_Competitions
FROM 
    Competitions c
JOIN 
    Categories cat 
    ON c.category_id = cat.category_id
GROUP BY 
    cat.category_name;

-- 3. Find all competitions of type 'doubles'
SELECT 
    competition_id AS Competition_ID,
    competition_name AS Competition_Name,
    type AS Type
FROM 
    Competitions
WHERE 
    type = 'doubles';

-- 4. Get competitions that belong to a specific category (e.g., ITF Men) 
SELECT 
    c.competition_id AS Competition_ID,
    c.competition_name AS Competition_Name,
    cat.category_name As Category
FROM 
    Competitions c
JOIN 
    Categories cat
    ON c.category_id = cat.category_id
WHERE 
    cat.category_name = 'ITF Men';

-- 5. Identify parent competitions and their sub-competitions 
SELECT 
    parent.competition_name AS Parent_Competition,
    child.competition_name AS Sub_Competition
FROM 
    Competitions child
JOIN 
    Competitions parent 
    ON child.parent_id = parent.competition_id;

-- 6. Analyze the distribution of competition types by category 
SELECT 
    cat.category_name AS Category,
    c.type As Type,
    COUNT(*) AS Competition_Count
FROM 
    Competitions c
JOIN 
    Categories cat 
    ON c.category_id = cat.category_id
GROUP BY 
    cat.category_name, c.type;

-- 7. List all competitions with no parent (top-level competitions) 
SELECT 
    competition_id As Competition_ID,
    competition_name AS Competition_Name
FROM 
    Competitions
WHERE 
    parent_id IS NULL;

