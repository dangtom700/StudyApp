
# Study Logging and Database

## Introduction

This project is to meant to store record of learning activities. The files and record of activities are then transfer into database that show user the timeline and activities done in that day.

## Project Objectives

The aim of this project is to create:

- Study habit and time management skills when learning new material
- Improve study performance through retrieving old record of learning material
- A text-based chat bot with pre-built command lines to perform certain tasks such as look up what activities are done in a given date
- A search engine to look up for the keyword in related context

## Scope and Deliverables

The data and record are kept inside this Obsidian vault and used for collecting and retrieving data. Any data that is wanted to executed has to be brought inside this vault.

The intended result is a desktop application that directly connect to a dedicated Obsidian vault that stores all data and record of learning activities. Another outcome for this project is a website that has a chat bot and other necessities for learning activities. The data of the chat bot is retrieved from a self-hosted database.

## Methodology and Approach

- Obsidian vault for creating files and record of learning activities
- Template files are store in template folder in Obsidian vault to create semi-structure files, easier for collecting and retrieving data. Files included are study logging, study report and study note
- Retrieving, collecting and processing text is intended to be done in Python. Then scale up with Java or C++ for faster and more secure performance
- Building a chat bot is done in Python for the beginning of the project later scale with Java
- PostgreSQL and MongoBD are choose to be the database depending how the data is querying and the structure of data

## Risk assessment

- School work is the top priority, so this project can be delayed due to school work overload
- Learning curve when building the application. The core and functionalities can be handled in Python for prototyping. Lack of understanding and experience in Java and database management
- Testing methodologies and strategies are not clear until the code is planned and built properly

## Timeline and Milestones

- Apr 29th, 2024. Documentation of project planning is created. New Obsidian vault is created for storing study material and study logging. Start learning habit to yield some raw data. BOOKS folder is list of learning material.
- May 13th, 2024. Finish creating the foundation of the project. Start to put into production for the first time.