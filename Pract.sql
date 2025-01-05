show databases;
use employee;
show tables;

select * from sales;

select max( profit) from sales;
select distinct profit from sales order by profit desc limit 3;


select max(profit ) as third_pro from sales where profit <(select max(profit ) from sales where profit<(select max(profit ) from sales));


select max(profit) from sales where profit <(

-- Imagine that you have table named students with columns name and score. 
-- Fetch the names of the top 5 students according to their score.

select name, score from student order by score desc limit 3;



-- # find the emp records from emp table where dep data science and salary >50000

select * from employee where department="Data Science" and salary >=50000;
select * from employee where department='Data Science' and salary>50000;