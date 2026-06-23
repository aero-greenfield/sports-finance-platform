# main notes:


what im building:

a longitudinal dataset of how prices move and how books disagree. 
the project is the accumulation of snapshots of upcoming fight every few hours. 

[ a tool to reduce the houses edge]

" building an automated pipeline that snapshots MMA fights odds from a bunch of bookmakers every few hours, so i can track how the betting lines move and disagree in the days before a fight. "




# golden question: how do MMA betting lines move and disagree across bookmakers in teh day before a fight?



* important questions that come with project:

1. line movement (open--> fight night). tracking each fighers implied probablity across the week, and see how a fighers probability drifted over the week


    --> if a line is steadily dfirifint one direction, you can place the bet before it moves further to lock the better number. which consistently lets you get a better price than the eventaul closing line. 


2. cross-book dispersion + best line:  you can find which book offers the best price for each figher, and how far apart the books are. this is called "line shopping" and it always has a signal (book never perfectly agree)


    --> if the same bet pays different amounts at different books, you can make more for the same bet. 

    --> when books diverege a lot, one is probably slow to update. if a sharp, and fast moving book has shifted but a soft book hasent, the soft books stale price may be exploitable. {EXTREME CASE} for this would be arbitrage- betting both sides across two books for guaranteed profit when their combited implied probability dips below 100%. 

    --> compute consensus implied  probability across all books, then see if a book deviates, a book sitting well of consensus is either holding a stale line or knows somehting. 

3. vig per bookmaker: average each books overround on MMA. ex: "book A runs a 7% margin, while book B runs a 4%"

    --> books that have fatter margins skim more off every bet. betting at consistently low-vig books means less of your money goes to the house before the fight even happens. 

4. closing line calibration (STRETCH): the odds api has a "scores" endpoint, by joining the closing odds to who actually won, you can ask if favorites win at rates that their odds imply. 

    -

* what im not doing: 
    - predicitng fight outcomes -- odds already have market predicitons, were looking at the market not the fights. 

    - its not about arbitrage, while arbs in two outcome MMA markets are rare, youll mainly find none. must frame it as dispersion and best-line (which is always present), and let arb-detection be a "and  occasionally we catch a near- arb" bonus if it appears. 

    ( arb :  when a handful of books have odds where you can place a dispersion of bets that allows you to have a guaranteed profit)

--> tool  detects historical arbs, not live actionable ones. the goal of the project is to find market-efficiency reseults: builiding a instrument that quantifies how rarely free money exisits. 


# Architecture notes:

* Bronze:   the raw landing of data, the exact API response, stored an untouched. one row pear fight per pull, the full JSON game object in a JSONB column, with sport_key, event_id, and ingested_at. at this layer there is no parsing or cleaning, the ruls is to store faithfully and pull borad, so you can always re-run downstream logic against the original data without re-hitting the API and burning quota. the ingest_at is what turns a stack of identical looking pulls into a time series. 


* Silver: cleaned and flattened. here I will explode the nested structure (game --> bookmaker --> market --> outcome) into flat rows: one row per fight, bookmakers, fighers, and snapshop. prices get cast into real numbers, timestamps into real datetimes, duplicate pulls get deduped, and you compute implied probability (1 / price) as a column. the output is one trustworth, granular table -- "ad snapshot T, book Y priced fighter X at P, implied prob Q". data is clean but not yet aggregated. this is where the dbt models do most of the work. 

* GOLD: analysis ready answers. aggregations shaped to answer one question each and feed one dashbaord: your three tables: 1. cross-book comparison, 2. line-movement time series, 3. per-book vig. Each one rolls silvers clean rows up into exactl the shape Metabase needs. 




# Stack notes:


* Airflow -- widly used service that allows you to create and orchestrate complex data pipelines. 

- intro to data orchestration:

- how a DAG is build/Airflow under the hood:

- setting up a local env:

- how DAGS are scheduled



* Docker compose/ Docker--

- compose networking:

- Image vs. container

- docker-compose.yml:

- Service name = hostname:

- Ports (5432:5432):

- Volumes: 


# GENERAL PROJECT NOTES:

- the API only gives snapshots of data. they hide the history behind a paywall, so the base of the project is creating one myself
    this is where airflow comes into play, schedules pulls, going to the bronze layer (raw accumulation of data)

- quote math: with MMA h2h us -- > 1 credit/call every 3 hours ~ 240/month, comfortably under the 500 free tier cap. worth recording so you dont accidentally widen markets/regions and blow it. 

implied probability and vig:

- a markets implied prob is [ 1 / price]. ex: a fighter at 1.6 implies 62.5% and another fighters is 2.3 which is 43.5%. add these two together and you get over 100%, this excess is the bookmarkers margin (the vig).






















# GENERAL PROJECT NOTES:


    the API only gives snapshots of data. they hide the history behind a paywall, so the base of the project is creating one myself


    this is where airflow comes into play, schedules pulls, going to the bronze layer (raw accumulation of data)

implied probability and vig:

- a markets implied prob is [ 1 / price]. ex: a fighter at 1.6 implies 62.5% and another fighters is 2.3 which is 43.5%. add these two together and you get over 100%, this excess is the bookmarkers margin (the vig).













# phase 1 of project: 

    goal: to get data-- i want the API to return data, airflow to run locally and runs an empty DAG. 

    notes:

    - a HTTPS successful status code is 200. so use this to check for success. 
        - other codes: 401(bad key), 422(bad params), 429(rate-limited)

    - we want to body to be JSON that we can parse, a python/list/dict. 

    - we should be able to pull a field out of it (some type of info) for a success. 

    - when using "odds' at the end of the url for specific sport data, you must define a region in the params. or else it will give you a 422 error. 



    python requests:
    - using the requests.get(), you must make sure your params match the specific API's param list. you must look through their docs and match their convention. 


* Airflow via Astro CLI. 
    - scaffold the project 
        - this creates project files: a dags folder for the DAGS, plugins, requirements file, packages file for OS level packages, and a dockerfile. (also generates a example DAG that can be used for syntax reference)

    - 