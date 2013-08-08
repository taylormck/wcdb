-- 1Crises that took place between 12 am and 12 pm
select id, name
  from crises_crisis
  where hour(time) >= 0
  and hour(time) < 12;

-- 2 Number of crises involving Obama
select count(*)
  from crises_crisis_people as cp
  inner join crises_crisis as c
  on cp.crisis_id=c.id
  where cp.person_id='PER_BROBMA';

-- 3Crises that occurred in the summer. (Assume "summer" is the months June, July, and August)
select id, name
  from crises_crisis
  where month(date) = 6
    or month(date) = 7
    or month(date) = 8;

-- 4Crises whose kind value contains the word "shooting"
select id, name
  from crises_crisis
  where instr(kind, 'shooting') > 0;


-- 5 Crises that took place in Texas (Location data should contain "Texas" or "TX")
select c.id, c.name
  from crises_crisislisttype as clt
  inner join crises_crisis as c
    on c.id = clt.owner_id
  where context = 'LO'
    and (instr(text, 'Texas')
    or instr(text, 'TX'));

-- 6 show all crises with a specific type of disaster
select id, name from crises_crisis
  where kind="Natural Disaster";

-- 7 Display crises that occurred after 1990
select id, name
from crises_crisis
where year(date) > 1990;

-- 8 show all organizations with more than three people
select t_id as id, t_name as name
from (
   select o.id as t_id, o.name as t_name, count(*) as num_people
   from crises_organization as o
   inner join crises_organization_people as op
    on o.id=op.organization_id
   group by o.id
) as t
where t.num_people >= 3;

-- 9 people involved in crises that happened in the 21st century
select distinct p.id, p.name
  from crises_person as p
    inner join crises_crisis_people as cp
      on cp.person_id=p.id
    inner join crises_crisis as c
      on c.id=cp.crisis_id
    where year(date)  > 2000;

-- 10 The total number of natural disasters
select count(*) from crises_crisis
  where kind="Natural Disaster";

