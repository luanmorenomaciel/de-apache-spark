### Data Engineer with Spark 3.0 [Challenge] ~ Use case

#### Company:

He at AllServicesYouCanGet, we are a group of small companies, this way our CEO David Fachini discuss with the CDO Adilson Cesar to better deliver data to c-level and other levels inside the group, Adilson hire One Way Solution to start do development the pipelines, showing to him what we can do using Spark, after a meeting between Adilson and Luan One Way Solution CEO, One Way Solution will get samples of data from:

* Financial [banks, subscription, credit cards]
* Entertainment [Music, movies and rating]
* Sales [devices, restaurant foods/desserts, beer, coffee, vehicles]
* small business [restaurants, other companies]

Saying this we have some business rules for each of these small companies:

###### Financial

All data related to subscriptions of rent vehicles, services (Movie and Music streaming), we need to understand more about this data.
* related subscription with services as rent vehicles and Entertainment using column user_id
* bring insights such as how many subscription we have for each services, what are the most higher services
* bring new insights, based on data show new insights for the c-levels

###### Entertainment

Data is coming from our apps such as OneWayFy (Music app) and OneWayFlix (Movie streaming), we need to related data to see what music and movies are better rated and see which one are not, the idea to cross this information and decide which one we gonna keep in the platforms.

* related data from music and movies with rating creating two pipelines one for music and another for movies
* bring insights such as how many users consume a specific music and movie.
* bring new insights, based on data show new insights for the c-levels

###### Sales

One of the main business, we have supply some of companies for automobile, devices, restaurants and supermarkets industry, our main products are: beer, coffee, vehicles and food, we need to now informations about our buyers.

* related theses items with users file, use the column user_id to bring this information
* bring insights such as how many buyers for each products to find the most sold.
* bring new insights, based on data show new insights for the c-levels.


###### Small business

In this area we gonna see which of our customer attend for each restaurant and which company the look for most.

* related data from restaurant and company with users creating two pipelines one for restaurant and another for movies
* related the restaurant with ratings data to find what is the most rated restaurant.
* bring insights such as the best company and the most rated restaurant to find the most sold.
* bring new insights, based on data show new insights for the c-levels.

During the meetings, Adilson show concern about data lake, they are building a data lake and they want One Way as partner to help them out, so now we have our data we have to create a data lake to receive, process and read enrichment data.
We have to think how data is going to be ingest, processing and deliver to the customer, don't forget to analyze datasources understand what you can do, using the data, we are waiting a high performance deliver for us to extract everything from our data.
