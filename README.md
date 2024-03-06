<img src="app/views/static/img/logo.png" alt="Music Recommendation App Logo" width="200" height="200"/>

# Music Recommendation App

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![Project Timeline](https://img.shields.io/badge/project_timeline-latest-green)](https://github.com/yale-cpsc-419-fa23/project-group-6/blob/main/PROJECT_TIMELINE.md)
[![Database Schema](https://img.shields.io/badge/database_schema-latest-green)](https://github.com/yale-cpsc-419-fa23/project-group-6/blob/main/DATABASE_SCHEMA.md)

> A dynamic platform designed for music discovery and community building among users with similar music interests.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Install](#install)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Team Members](#team-members)
  
## Introduction

Our Music Recommendation App aims to create a dynamic platform where users can upload and edit their favorite tracks
while also discovering new music tailored to their preferences. Further, it fosters community building by enabling users
to connect with others having similar music interests. We look forward to bringing our vision to life through this
project.

## Features
- User registration and secure login system
- Drag-and-drop music upload functionality
- Music recommendation engine for personalized suggestions
- Like and Dislike system to refine recommendations
- User profiles with track metadata editing
- Community features such as Follow and Collaborate
- Genre exploration for music discovery

## Install

To set up the Music Recommendation App, follow these steps:

```bash
git clone https://github.com/yale-cpsc-419-fa23/project-group-6
cd project-group-6
pip install -r requirements.txt
```

To download the dataset, please refer to the [DATABASE_SCHEMA file](https://github.com/yale-cpsc-419-fa23/project-group-6/blob/main/DATABASE_SCHEMA.md) for instructions. After downloading the sqlite file and placing it in the app directory, the app is ready to run.

## Usage

To run the Music Recommendation App:

```bash
python run.py
```

Navigate to the URL provided in the console to access the web application.

## Project Structure

```
/project-group-6
|-- /app
|   |-- /controllers
|   |   |-- __init__.py
|   |   |-- auth_controller.py
|   |   |-- main_controller.py
|   |   |-- music_controller.py
|   |   |-- settings_controller.py
|   |   |-- user_controller.py
|   |-- /models
|   |   |-- __init__.py
|   |   |-- genre.py
|   |   |-- song.py
|   |   |-- user.py
|   |   |-- user_song_create.py
|   |   |-- user_song_like.py
|   |   |-- user_user_follow.py
|   |-- /uploads
|   |-- /utils
|   |   |-- __init__.py
|   |   |-- audio_feature_utils.py
|   |   |-- recommendation_utils.py
|   |-- /views
|   |   |-- /static
|   |   |-- /templates
|   |   |-- __init__.py
|   |   |-- forms.py
|   |-- __init__.py
|   |-- config.py
|   |-- *database.sqlite*
|-- run.py
|-- requirements.txt
```

## Team Members

- Jiayi Chen
- Kai Gao
- Yue Quan