## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string`
- `--idimage string`
- `--idfile string`

### Answer:

I used podman for this, and I don't have docker installed; but looking at the [docs file](https://github.com/docker/docs/blob/1f1a8de5fe3ac2d3f3357333fc7d26d59235e17e/_data/buildx/docker_buildx_build.yaml#L187) I'm guessing it's iidfile 


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- 1
- 6
- 3
- 7

### Answer

Running the following:

podman run -it --entrypoint=sh python:3.9

I had the following output:

| Package |  Version |
|---------|----------|
| pip     |   22.0.4 |
| setuptools | 58.1.0 |
| wheel   |   0.40.0 |

And so it would seem the answer is 3.

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20689
- 20530
- 17630
- 21090

### Answer

After adjusting my script to allow csv downloads, I used the following query for this:

```sql
select COUNT (*)
from yellow_taxi_data
where
	lpep_pickup_datetime >= '2019-01-15 00:00:00'
and
	lpep_pickup_datetime <= '2019-01-15 23:59:59'
and
	lpep_dropoff_datetime >= '2019-01-15 00:00:00'
and
	lpep_dropoff_datetime <= '2019-01-15 23:59:59'
```

and the count shows 20530.

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15
- 2019-01-10

I am attempting to answer this as; in total, which day had the largest total distance travelled?

The query I am using is:

```sql
select SUM(trip_distance)
from yellow_taxi_data
where
	lpep_pickup_datetime >=  '2019-01-10 00:00:00'
and
	lpep_pickup_datetime <= '2019-01-10 23:59:59'
and
	lpep_dropoff_datetime >= '2019-01-10 00:00:00'
and
	lpep_dropoff_datetime <= '2019-01-10 23:59:59'
```

- 18th: 75330.6
- 28th: 73335.3
- 15th: 74179
- 10th: 78572

According to this calculation, the date with the most trips would be the **10th**.

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254
- 2: 1282 ; 3: 274


I adjusted the query from above slightly as it seemed this question expects only journeys which has a start time and finish time both on the 1st; no cross journey days.

```sql

select *
from yellow_taxi_data
where
	passenger_count=3
and
(
	(
			lpep_pickup_datetime >=  '2019-01-01 00:00:01'
		and
			lpep_pickup_datetime <= '2019-01-01 23:59:59'
	) or (
			lpep_dropoff_datetime >= '2019-01-01 00:00:01'
		and
			lpep_dropoff_datetime <= '2019-01-01 23:59:59'
		)
	)
```

The answer for this was 2: 1282, 3: 254


## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza

### Answer

I used the following query for this:

```sql
select
	ytd.tip_amount,
	tz_pu.zone as "Pickup zone",
	tz_do.zone as "Dropoff zone"
from
	yellow_taxi_data ytd
join
	taxi_zone tz_pu
on
	ytd."PULocationID" = tz_pu.location_id
join
	taxi_zone tz_do
on
	ytd."DOLocationID" = tz_do.location_id
where
	tz_pu.zone = 'Astoria'
order by
	tip_amount desc
```

Then, looking at the top result, there was a tip of $88 from Astoria to Long Island City/Queens Plaza


## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 30 January (Monday), 22:00 CET


## Solution

See here: https://www.youtube.com/watch?v=KIh_9tZiroA