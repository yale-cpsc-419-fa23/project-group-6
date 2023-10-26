# Music Recommendation App

## Project Summary:

Our Music Recommendation App aims to create a dynamic platform where users can upload and edit their favorite tracks while also discovering new music tailored to their preferences. Further, it fosters community building by enabling users to connect with others having similar music interests. We look forward to bringing our vision to life through this project.

## Team Members:
- Jiayi Chen
- Kai Gao
- Yue Quan

## Timeline:

### 1. MVP Release (Due: Nov 3)
- Basic three-tier architecture: data, application, and presentation tiers.
- User registration and secure login.
- Initial drag-and-drop music upload feature.
- Homepage and simple search feature

### 2. Alpha Version (Due: Nov 17)
- Enhanced user profile features.
- Metadata editing for track information.
- Basic recommendation system initiation.
- Genre exploration introduction.
- Front-end visualization for album art.

### 3. Optional Deliverable: Recommendation System Enhancement (Due: Nov 26)
- Optimization of the recommendation engine for faster and more accurate results.

### 4. Beta Version (Due: Dec 1)
- Fully functional music recommendation engine, equipped to produce daily mixes.
- Introduction of the Like and Dislike system.
- Top played list integration for daily, weekly, monthly statistics.
- Introduction of the Connect & Collaborate features.


### 5. Final Version (Due: Dec 5)
- Rectification of bugs and glitches identified during the beta phase.
- Enhancement of the front-end for smoother user experiences and more intuitive interfaces.
- Strengthening of the back-end with advanced analytics, database integrity checks, and reliability measures.
- Conducting extensive tests to ensure stability during novel user interactions.


#### MISCELLANEOUS

##### Database:
1. User
2. Music
3. User-Music (Create)
4. User-Music (Like)
5. User-User (Follow/Friend?)
6. Music-Tag
7. Tag
8. ImpressionStats
9. UserStats

Due to size constraints, we've stored our datasets on Google Drive. Access the datasets using your Yale account [at this link](https://drive.google.com/drive/folders/1Y0rKHs0sMmie-0wBxS__c0QH3HWUgug_?usp=sharing).

##### Project Structure:
```
/music_recommendation_mvc
|-- /app
|   |-- __init__.py
|   |-- /models
|   |   |-- __init__.py
|   |   |-- song.py
|   |-- /views
|   |   |-- __init__.py
|   |   |-- base.html
|   |   |-- index.html
|   |   |-- upload.html
|   |   |-- recommendations.html
|   |-- /controllers
|   |   |-- __init__.py
|   |   |-- main_controller.py
|   |   |-- upload_controller.py
|   |   |-- recommendation_controller.py
|   |-- /static
|   |   |-- /css
|   |   |-- /js
|   |   |-- /uploads
|   |-- /utils
|   |   |-- __init__.py
|   |   |-- recommendation_utils.py
|   |-- config.py
|-- run.py
|-- requirements.txt

```