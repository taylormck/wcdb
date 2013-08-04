--Crises that took place between 12 am and 12 pm
select id, name 
  from crises_crisis
  where hour(time) >= 0
  and hour(time) < 12;

-- Number of crises involving Obama
select count(*)
  from crises_crisis_people 
  inner join crises_crisis;

-- Crises that occurred in the summer. (Assume "summer" is the months June, July, and August)
select id, name
  from crises_crisis
  where month(date) = 6
    or month(date) = 7
    or month(date) = 8;

-- Crises whose kind value contains the word "shooting"
select id, name
  from crises_crisis
  where instr(kind, 'shooting') > 0;


-- Crises that took place in Texas (Location data should contain "Texas" or "TX")
select c.id, c.name
  from crises_crisislisttype as clt 
  inner join crises_crisis as c
    on c.id = clt.owner_id
  where context = 'LO'
    and (instr(text, 'Texas')
    or instr(text, 'TX'));