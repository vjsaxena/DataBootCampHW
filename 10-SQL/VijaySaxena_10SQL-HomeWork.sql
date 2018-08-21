#Select the database
use sakila;

#Describe table 'actor'
describe actor;

#-----------------------------------------------------------------------------------------------------------------------------------------------------
# 1a. Display the first and last names of all actors from the table `actor`.
select  first_name,last_name from actor;

# 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column `Actor Name`.
select  upper(concat((first_name)," ",last_name)) as "Actor Name" from actor;

# 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." 
#        What is one query would you use to obtain this information?
select actor_id, first_name, last_name from actor where first_name ='Joe';

# 2b. Find all actors whose last name contain the letters `GEN`:
select * from actor where upper(last_name) like '%GEN%';

# 2c. Find all actors whose last names contain the letters `LI`. This time, order the rows by last name and first name, in that order:
select * from actor where upper(last_name) like '%LI%' order by last_name, first_name;

# 2d. Using `IN`, display the `country_id` and `country` columns of the following countries: Afghanistan, Bangladesh, and China:
select * from country where country in ('Afghanistan','Bangladesh','China');

#3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, 
#       so create a column in the table `actor` named `description` and use the data type `BLOB` (Make sure to research
#       the type `BLOB`, as the difference between it and `VARCHAR` are significant).
alter table actor add ( description blob  );

# 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the `description` column.
alter table actor drop description;

#4a. List the last names of actors, as well as how many actors have that last name.
select last_name, count(*) as "Actor Count" from actor group by last_name;

#4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
select last_name, count(*) as "Actor Count" from actor group by last_name having count(*) >=2;

# 4c. The actor `HARPO WILLIAMS` was accidentally entered in the `actor` table as `GROUCHO WILLIAMS`. Write a query to fix the record.
select * from actor  where first_name ="GROUCHO" and last_name = "WILLIAMS";
update  actor
	set first_name="HARPO"
    where first_name ="GROUCHO" and last_name = "WILLIAMS";
 select * from actor  where first_name ="HARPO" and last_name = "WILLIAMS";   
    

#4d. Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. It turns out that `GROUCHO` was the 
#      correct name after all! In a single query, if the first name of the actor is currently `HARPO`, change it to `GROUCHO`.
 select * from actor  where first_name ="HARPO";   
 SET SQL_SAFE_UPDATES = 0;
 update  actor
	set first_name="GROUCHO"  where first_name ="HARPO" ;
    
select * from actor  where first_name ="GROUCHO" ;
select * from actor  where first_name ="GROUCHO" and last_name = "WILLIAMS";

#5a. You cannot locate the schema of the `address` table. Which query would you use to re-create it?

#Hint: <https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html>
#desc address
CREATE TABLE address (
  address_id 	smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  address 		varchar(50) NOT NULL,
  address2 		varchar(50) DEFAULT NULL,
  district 			varchar(20) NOT NULL,
  city_id 			smallint(5) unsigned NOT NULL,
  postal_code 	varchar(10) DEFAULT NULL,
  phone 			varchar(20) NOT NULL,
  location 			geometry NOT NULL,
  last_update 	timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (address_id),
  KEY (city_id),
  SPATIAL KEY (location),
  CONSTRAINT  FOREIGN KEY (city_id) REFERENCES city (city_id) ON UPDATE CASCADE
) ;

# 6a. Use `JOIN` to display the first and last names, as well as the address, of each staff member. Use the tables `staff` and `address`:

select s.first_name, s.last_name, a.address, a.district, a.city_id, a.postal_code
from staff as s  
	join address as a 
    on (s.address_id=a.address_id);


#6b. Use `JOIN` to display the total amount rung up by each staff member in August of 2005. Use tables `staff` and `payment`.

select s.first_name, s.last_name, sum(p.amount)
from staff as s
	join payment as p
    on (s.staff_id=p.staff_id)
group by s.first_name, s.last_name;

# 6c. List each film and the number of actors who are listed for that film. Use tables `film_actor` and `film`. Use inner join.
select f.title, count(a.actor_id)
from film as f
   inner join film_actor as a
   on (f.film_id=a.film_id)
   group by f.title;
   
# 6d. How many copies of the film `Hunchback Impossible` exist in the inventory system?
select count(*) as "No of Copies"
 from inventory  as i
	inner join film as f
    on (i.film_id=f.film_id)
    where f.title="Hunchback Impossible";
    
select f.title, count(*) as "No of Copies"
 from inventory  as i
	inner join film as f
    on (i.film_id=f.film_id)
    where f.title="Hunchback Impossible";

#6e. Using the tables `payment` and `customer` and the `JOIN` command, list the total paid by each customer.
#       List the customers alphabetically by last name:

select c.first_name," ", c.last_name,  sum(p.amount) as "Total Amount Paid"
from customer as c
  join payment as p
 on (c.customer_id=p.customer_id)
 group by c.customer_id,c.first_name, c.last_name
 order by c.last_name;


#```
#	![Total amount paid](Images/total_payment.png)
#```

#7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, 
#        films starting with the letters `K` and `Q` have also soared in popularity. Use subqueries to display the titles of 
#        movies starting with the letters `K` and `Q` whose language is English.

select title,language_id 
	from film 
    where substr(title,1,1) in ("K","Q") 
		and language_id = (select language_id from language where name="English");


#7b. Use subqueries to display all actors who appear in the film `Alone Trip`.
select a.first_name, a.last_name 
from actor as a
  join film_actor as f
  on (a.actor_id= f.actor_id)
  where f.film_id =(select film_id from film where title="Alone Trip")
  order by a.last_name;

# 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all 
#	     Canadian customers. Use joins to retrieve this information.
select c.first_name, c.last_name, c.email ,a.address , ct.city, co.country
from customer as c
	join address as a on (c.address_id = a.address_id)
    join city  as ct on (a.city_id = ct.city_id)
    join country as co on (ct.country_id =co.country_id)
    where co.country="Canada";

select c.first_name, c.last_name, c.email ,a.address , ct.city
from customer as c
	join address as a on (c.address_id = a.address_id)
    join city  as ct on (a.city_id = ct.city_id)
   where ct.country_id =(select country_id from country where country="Canada");


# 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. 
#		 Identify all movies categorized as family films.
select f.title, c.name as "Category"
from  film as f
	join film_category as fc on (f.film_id =fc.film_id)
    join category as c on (fc.category_id=c.category_id)
    where c.name = 'Family';
    #where c.name in ('Family','Drama');
    

#7e. Display the most frequently rented movies in descending order.
SELECT f.title, count(r.rental_id)
FROM rental as r 
	JOIN inventory as i on (r.inventory_id= i.inventory_id)
    JOIN film as f on (i.film_id = f.film_id)
    group by f.title
    order by count(r.rental_id) desc;



# 7f. Write a query to display how much business, in dollars, each store brought in.
select distinct (store_id) from inventory;
select * from store;

select  i.store_id, a.address,a.district, sum(p.amount) as "Total Business in '$'s"
#r.rental_id, r.inventory_id, p.payment_id, p.amount , i.store_id
from rental as r
    join payment as p on (r.rental_id = p.rental_id)
	join inventory as i on (r.inventory_id = i.inventory_id)
    join store as s on (i.store_id = s.store_id)
    join address as a on (s.address_id=a.address_id)
    group by i.store_id,a.address, a.district;

# 7g. Write a query to display for each store its store ID, city, and country.
select s.store_id,  c.city, co.country 
	#a.address, a.district,
    from store as s 
      join address as a on (s.address_id=a.address_id)
      join city as c on (a.city_id = c.city_id)
      join country as co on (c.country_id = co.country_id);
    
#7h. List the top five genres in gross revenue in descending order. 
#	(**Hint**: you may need to use the following tables: category, film_category, inventory, payment, and rental.)


select   c.name as "Genre" ,sum(p.amount) as "Gross Revenue"
#r.rental_id, r.inventory_id, p.payment_id, p.amount , i.store_id
from rental as r
    join payment as p on (r.rental_id = p.rental_id)
	join inventory as i on (r.inventory_id = i.inventory_id)
    join film_category as fc on (i.film_id = fc.film_id)
    join category as c on (fc.category_id=c.category_id)
    group by (c.name)
    order by sum(amount) desc
    limit 5;
    

# 8a. In your new role as an executive, you would like to have an easy way of viewing the 
#		Top five genres by gross revenue. Use the solution from the problem above to create a 
#		view. If you haven't solved 7h, you can substitute another query to create a view.

create view top_earning_genres as 
select   c.name as "Genre" ,sum(p.amount) as "Gross Revenue"
#r.rental_id, r.inventory_id, p.payment_id, p.amount , i.store_id
from rental as r
    join payment as p on (r.rental_id = p.rental_id)
	join inventory as i on (r.inventory_id = i.inventory_id)
    join film_category as fc on (i.film_id = fc.film_id)
    join category as c on (fc.category_id=c.category_id)
    group by (c.name)
    order by sum(amount) desc
    limit 5;
    
# 8b. How would you display the view that you created in 8a?

##### Describe view to see view description (list of columns etc)
desc top_earning_genres;

##### Display content of the view (execute query on the view)
select * from top_earning_genres;

# 8c. You find that you no longer need the view `top_five_genres`. Write a query to delete it.
drop view top_earning_genres;


