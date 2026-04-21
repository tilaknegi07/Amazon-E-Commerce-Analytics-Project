-- A. SCHEMA & DATA LOAD
select * from customers 
limit 10

-- B. BASIC REVENUE AGGREGATIONS
-- B1. Overall revenue snapshot
select 
count(*) as Total_order,
round(sum(price)::numeric,2) as gross_revanu,
round(sum(final_price)::numeric,2) as net_revamu,
round(avg(final_price)::numeric,2) as Average_order_value,
round(min(final_price)::numeric,2) as min_order_value,
round(max(final_price)::numeric,2) as max_order_value,
round(sum(price-final_price)::numeric,2) as total_discount_given,
round(avg(discount)::numeric,2) as avg_discount_given,
round(sum(price-final_price)::numeric/sum(price)::numeric*100,2) as overall_discount_per
from customers

-- B2. Returned vs non-returned revenue split

select is_returned,
count(*) as orders,
round(sum(final_price)::numeric,2) as revanu,
round(avg(final_price)::numeric,2) as avg_order_value,
round(sum(final_price)::numeric/(select sum(final_price)::numeric from customers)*100,2) as revanu_per
from customers
group by is_returned

-- C. REVENUE BY CATEGORY & SUBCATEGORY
-- C1. Revenue by category — sorted by net revenue
select category,
count(*) as orders,
round(sum(price)::numeric,2) as net_revanu,
ROUND(SUM(final_price)::numeric, 2)   AS net_revenue,
ROUND(AVG(final_price)::numeric, 2)   AS avg_order_value,
ROUND(AVG(discount)::numeric, 2)   AS avg_discount_pct,
ROUND(SUM(final_price)::numeric* 100.0/ (SELECT SUM(final_price)::numeric FROM customers), 2) AS revenue_share_pct
from customers
group by category

-- C3. Category revenue — returned vs kept (net realised revenue)

select 
category,
count(*) as total_orders,
sum(case when is_returned='FALSE' then 1 else 0 end) as Kept_order,
round(sum(case when is_returned='FALSE' 
		  then final_price else 0 end)::numeric,2) as  realised_revenue,
round(sum(case when is_returned='True'
		 then final_price else 0 end )::numeric,2) as returned_revanue,
ROUND(SUM(CASE WHEN is_returned = 'TRUE'
                   THEN final_price ELSE 0 END)::numeric * 100.0
          / NULLIF(SUM(final_price)::numeric, 0), 2)   AS return_revenue_pct
FROM customers
GROUP BY category
ORDER BY realised_revenue DESC;

-- E. BRAND REVENUE PERFORMANCE
select 
brand,
count(*) as Orders,
ROUND(SUM(final_price)::numeric,2)          AS net_revenue,
ROUND(AVG(final_price)::numeric ,2)         AS avg_order_value,
ROUND(AVG(discount)::numeric,2)            AS avg_discount_pct,
ROUND(AVG(rating)::numeric,2)              AS avg_rating,
SUM(CASE WHEN is_returned = 'TRUE' THEN 1 ELSE 0 END)::numeric AS returns
FROM customers
GROUP BY brand
ORDER BY net_revenue DESC;

-- F. REVENUE RANKING — WINDOW FUNCTIONS
--F. REVENUE RANKING — WINDOW FUNCTIONS

select 
category,
round(sum(final_price)::numeric,2) as net_revanu, 
rank() over(ORDER BY SUM(final_price) DESC) AS revenue_rank,
dense_rank() over(ORDER BY SUM(final_price) DESC) AS dense_rank
from customers 
group by category
order by revenue_rank

-- F2. Running total of revenue ordered by purchase date

select 
purchase_date,
product_id,
category,
round(final_price::numeric,2) as  order_revanu,
round(sum(final_price::numeric )
	  over(order by purchase_date
		   rows between unbounded preceding  and current row)
	  ,2) 
	  as running_total_revanu
from customers
order by purchase_date

-- F4. Revenue percentile — customer value tiers
select 
price_bucket,
count(*) as order_count,
round(sum(final_price)::numeric,2) as order_value
from customers
group by price_bucket

-- G. CITY / LOCATION REVENUE
-- G1. Revenue by city
select 
location  as city,
count(*) as orders,
round(sum(final_price)::numeric,2) as net_revanue,
round(avg(final_price)::numeric, 2) as  avg_order_value,
round(sum(final_price)::numeric*100.0/
	  (select sum(final_price)::numeric from customers),2) as revenu_share_per,
sum(case when is_returned = 'true' then 1 else 0 end) as returns
from customers
group by location 
order by net_revanue   desc

-- G2. Top category per city (using subquery)
select  
 city,
 category,
 category_revanu
 from(
 select location as city,
	 category,
	 round(sum(final_price)::numeric ,2)  as category_revanu,
	 rank() over( partition by location order by sum(final_price) desc ) as rnk 
		   from  customers 
		   group by location, category) ranked 
	  where rnk=1	

--SELLER REVENUE CONTRIBUTION
--Seller revenue & performance

select 
seller_id,
round(avg(final_price)::numeric,2) as seller_aov,
round( (select avg(final_price)::numeric from customers ),2)  as overall_aov   ,
round(avg(final_price)::numeric -(select avg(final_price)::numeric from customers),2) as aov_vs_avg
from customers 
group by seller_id
having avg(final_price) > (select avg(final_price) from customers )
order by seller_aov desc



-- Revenue at risk by delivery status
 select delivery_status, 
 count(*) as orders,
 round(sum(final_price)::numeric,2) as revanu ,
 sum( case when is_returned = 'true' then 1 else 0 end ) as already_returned
 from customers 
 group by  delivery_status 
 order by revanu desc 








 
 