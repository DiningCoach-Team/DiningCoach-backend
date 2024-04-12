# DiningCoach API server
### DiningCoach, for those who need special meal assistance
<img src="images/DiningCoach App Overview.jpg" alt="DiningCoach App Overview Image" width="500" height="700">


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
**(Note that tech stacks listed here are for backend only.)**
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
- TBA

### System Architecture
- TBA

### Server Architecture
- TBA


## 5. ERD
<img src="images/DiningCoach ERD.jpg" alt="DiningCoach ERD" width="600" height="330">

- For more details click here: [DiningCoach ERD_v3](https://www.erdcloud.com/p/ziMmq2mBhe2d4cCTr)


## 6. API Docs
🔥 [Swagger API Documentation](https://www.diningcoach.org/swagger/)


## 7. Technical achievements
### (1) Improved user experience through Django ORM and database optimisation
- TBA

### (2) Solved race condition with atomic lock using Django ORM
- TBA

### (3) Minimised server load by utilising Celery-based asnychrnonous task execution
- TBA
