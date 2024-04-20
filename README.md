# DiningCoach API server
#### Last updated : 20 Apr 2024
### DiningCoach, for those who need special meal assistance
<img src="images/DiningCoach App Overview.jpg" alt="DiningCoach App Overview (1000x1400)" width="800" height="1120">


## 1. Project Intro
- **What is this app**
  - This app is a mobile-based platform that allows you to register your disease and eating habits in advance, search for foods that fit your needs, write a food diary, and form a community.
- **Why this app is developed (Pain Point)**
  - It is very inconvenient for people who need special diet therapy to buy and eat food suitable for them. Not only is it hard to buy food sold in supermarkets, it is also difficult to eat food sold in restaurants.
  - Existing diet management apps focus on losing fat, so there are almost no services that help people who need special meal assistance.
- **Who needs this app**
  - Anyone who has just been discharged from the hospital, is about to undergo an examination, or needs consistent diet management due to illness or religious issues can use this service. Some examples are as follows:
    - Patients who need a low-salt diet
    - Patients who need an iodine-restricted diet
    - Patients who cannot eat food containing a lot of fiber
    - Patients who cannot eat starchy food
    - Vegetarians (vegans)
    - Pregnant women
    - Muslims (Halal food), etc.
- **How to use this app**
  - Register your disease or eating habits in advance
  - Tell you what food you can and cannot eat → Scan barcode at the supermarket
  - Keep a food diary recording the food you eat each meal → Take a photo of your meal
  - Share your food diary with others so that they can comment and share advice with you
  - Form a community where people with each disease can communicate → Open a separate bulletin board for each eating habit
  - Special diet plan service consisting only of edible ingredients (yet to be implemented)


## 2. Design
### DiningCoach App Overview
- [DiningCoach App Overview Figma file](https://www.figma.com/file/cUA0Ded7l50uqjOluq48jq/DiningCoach-App-Overview)
  - This file only contains a few main screens of this app for simplicity.

### DiningCoach App Design
- [DiningCoach App Design Figma file](https://www.figma.com/file/EwPAtUD1s4bkQTvIkbDXiS/DiningCoach-App-Design)
  - This file contains every single screen of this app.


## 3. Tech Stacks used
**(Please note that tech stacks listed here are for backend only.)**
- Languages
  - Python
- Backend Framework
  - Django(Django Rest Framework)
- Python libraries
  - celery
  - django-filter
  - simplejwt, django-allauth, dj-rest-auth
  - drf-yasg
- Database
  - PostgreSQL
- Infra
  - AWS(EC2, RDS)
  - Docker, Docker Compose ***(Currently working on it!)***
- CI/CD
  - GitHub Actions ***(Currently working on it!)***
- Design
  - Figma


## 4. Project Architecture
### Overview Architecture
- ***Please be advised that we are currently in progress, and `Nginx`, `Gunicorn` are not available at the moment.***

<img src="images/DiningCoach Overview Architecture.jpg" alt="DiningCoach Overview Architecture (1200x700)" width="960" height="560">

### System Architecture
- ***Please be advised that we are currently in progress, and `GitHub Actions` is not available at the moment.***

<img src="images/DiningCoach System Architecture.jpg" alt="DiningCoach System Architecture (1200x900)" width="960" height="720">

### Server Architecture
<img src="images/DiningCoach Server Architecture.jpg" alt="DiningCoach Server Architecture (1200x500)" width="960" height="400">


## 5. ERD
- For more details click here: [DiningCoach ERD_v3](https://www.erdcloud.com/p/ziMmq2mBhe2d4cCTr)

<img src="images/DiningCoach ERD.jpg" alt="DiningCoach ERD (1200x700)" width="960" height="560">


## 6. API Docs
🔥 [Swagger API Documentation v1](https://www.diningcoach.org/swagger/)

<img src="images/DiningCoach API Swagger Docs 1.jpg" alt="DiningCoach API Swagger Docs 1 (1200x800)" width="960" height="640">
<img src="images/DiningCoach API Swagger Docs 2.jpg" alt="DiningCoach API Swagger Docs 2 (1200x800)" width="960" height="640">


## 7. Technical achievements
### (1) Improved user experience through the PostgreSQL Database and Django ORM optimisation
- **Problem (What issues we faced)**
  - When we measured the latency, which is the total delay to get a response when a user sends a request, our Food Search & Scan API took an average of 4 seconds. Especially `/food/search/processed` API sometimes even took longer than 5 seconds as there were over 700,000 number of data. Since we believe that this largely affects our user experience, we tried to make this as fast as possible. But at the same time, maintaining the accuracy of the search results was our highest priority.
- **Solution (How we solved)**
  - We tried to implement a few ways to decrease the latency of our API.
  - First of all, we created an index to attributes in each food table whose cardinality is high, such as 'food code', 'food name', and 'category'. However, this did not make a big difference in terms of speed. We later found out that our index creates a default `B-tree Index`, which simply did not apply to our situation. Since most of our search is based on finding results ***containing*** the input keyword, it creates a `LIKE` query, and this does a full scan search instead of utilising our index. Therefore, we created a `GIN Index` to the 'food name' column, which finally solved our problem.
  - Besides creating an index, we also tried to optimise the usage of Django ORM. As Django ORM auto generates SQL query and executes it in a lazy loading way, when an attribute from a related table is called, it gets data from its related tables every single time it is called. This causes a huge inefficiency resulting in a lot of delay to our API. To solve this issue, we used the `prefetch_related` method to get data in an eager loading way, which means that all data from related tables are loaded only once the first time when it is called.
- **Result (What achievements we made)**
  - Our Food Search & Scan API, which took an average of 4 seconds, has become an average of 1.2 seconds. This is more than 3 times faster than before and a huge improvement compared to the delay time before resolving the issue.

### (2) Resolved race condition with atomic locks using Django ORM
- **Problem (What issues we faced)**
  - When a user signs up to our DiningCoach service, our desired behaviour is to automatically create a new row to 'user' table, followed by a task to create empty rows to 'user info' and 'user health' table, respectively. However, when there were a lot of users creating a new account at the same time, this did not work as expected. The table rows should be created in a sequence of the time the user creates a new account, however, it was being created in a random order instead. This must not happen and should be resolved as soon as possible as it could violate ACID transaction properties.
  - Similarly, when a user tried to write or edit their meal diary, we expected the diary to be created or edited only once for each user request. However, when a user double-clicked the button either intentionally or by mistake, it was created or edited twice. This is an unexpected behavior that should be addressed as soon as possible since it could violate ACID transaction properties.
- **Solution (How we solved)**
  - There are a few ways to resolve these kinds of concurrency issues.
  - **Solution 1**
    - We can increase the isolation level of our database. An isolation level of a database means that a single transaction should be isolated from other transactions in the database system trying to simultaneously modify data. There are four kinds of isolation levels: `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, and `SERIALIZABLE`, where the last one has the highest isolation level and lowest concurrency, and vice versa. In our case, we considered increasing the isolation level to the `REPEATABLE READ` level from the default `READ COMMITTED` level. However, we opted out of this option since it would highly affect our server performance.
  - **Solution 2**
    - Instead of increasing the isolation level of our database as a whole, we can also use locks at a row level inside the table. This can be achieved by using the `FOR UPDATE` SQL query for the selected rows. Since Django ORM also provides this feature, we can simply use the `select_for_update` method along with the original queryset methods. Furthermore, the `F` object can be used to resolve concurrent issues by pulling out data directly from the database without having to save it to Python memory. The main advantage of using the `F` object is that we can manipulate data at each attribute level and also this can be done without using explicit locks. All of these solutions have been implemented in our server code, which will be used whenever POST and PUT methods are invoked.
  - **Solution 3**
    - If we are moving to a distributed environment where there are multiple server instances, the above two solutions may be inefficient. Instead, we can use Redis, a widely used in-memory DB, to lock data at the application level. Redis supports `setnx`(set not exists) and allows us to acquire atomic locks for concurrent transactions. This could be a better solution since concurrency issues can be controlled at our application level outside of the database, which makes it possible to deploy servers in a distributed environment. However, this has not been implemented in our system yet due to our limited amount of time.
- **Result (What achievements we made)**
  - By using locks, we were able to resolve these race condition situations. This may affect our speed of API to write or edit meal diaries, however, we believe it is not a critical part of our overall app performance compared to the importance of maintaining the consistency of our user and meal diary data.

### (3) Minimised server load by utilising Celery-based asynchronous task execution
- **Problem (What issues we faced)**
  - When a user signs up for our DiningCoach service, our business logic is to send them a confirmation email informing them their sign-up has been successful. Also, if a user wants to reset their password, an email containing the reset link should be sent to them. But, all these email-sending tasks take a lot of time, an average of 8 seconds per request to get a response. Also, our server becomes very slow for that period as it is still waiting for the job to be done.
  - Similarly, when a new meal diary is created or updated, its nutrition data, which is the total sum of the eaten food, has to be generated or regenerated. However, this is a heavily time-consuming process since all the nutrition data for each food should be retrieved from the table before adding them up. It took an average of 4 seconds for every meal diary to respond to create or update requests. We thought this should be done much faster for a better user experience.
- **Solution (How we solved)**
  - We thought this issue could be solved if the user could get a response instantly, but at the same time, the email-sending task should still be processed internally. We figured out that this can be done by implementing Celery, which is a famous Python library for dealing with asynchronous tasks.
  - To set up Celery, we first configured Redis, a widely used in-memory DB, to utilise it as our message broker. A message broker works as a task queue where it receives the message from the producer(DiningCoach Server) and stores the message until it can be sent to the consumer(Celery Worker). The main reason why we chose Redis as our message broker here is that we were already planning to use Redis to solve concurrency issues, and it would be better just to use the same database instead of a different one.
  - We separated all email-sending tasks to Celery Worker shared tasks, so that our server would not be bothered with processing requests and responses. Tasks to generate or regenerate nutrition data when a user creates or updates a meal diary have been separated in the same way.
  - Our business logic also has a task to permanently delete meal diaries in the trash bin after 30 days to save up memory space. Since this must be done at a scheduled time regularly, we have utilised the Celery Beat scheduler to execute this task every morning at 6 AM.
  - However, using celery can potentially create bottlenecks, which can make all the asynchronous tasks to be executed too slowly. If we encounter these issues, we expect to resolve them by customising some of the configuration settings, and this is something we should dig deeper into later.
- **Result (What achievements we made)**
  - Our User Sign Up & Password Reset API, which originally took over 8 seconds, has finally become less than a second (943 ms). Additionally, our Meal Diary Write & Edit API, which originally took over 4 seconds, has also now become less than a second (928 ms).
