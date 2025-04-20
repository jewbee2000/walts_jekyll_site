---
layout: post
title: Word Chain
date: 2024-04-02
lead: A web-based word game
---

# Compound Noun Chain Game

This is a we-based daily game (like wordle) where players find a chain of compound nouns from noun-A to noun-B. Each entered noun is validated to form a compound noun with the previous noun. If a prefix chain is invalid, progress cannot be made until the last noun in the chain is cleared and replaced with a valid compound. If noun-B is reached, the user’s solution is registered, something celebratory happens, and the user’s cumulative stats are shown.

![Screenshot](https://walter.teitelbaum.us/assets/files/word_chain.png "Screenshot")

# 🧩 Wordchain Game Backend

My dad invented this game, but I wrote the whole backend and frontend implementation. I coded the app with **Ruby** and the **Sinatra** framework. It utilizes **ActiveRecord** for database management and **Redis** for fast caching and word validation.

The backend handles:
- User interaction and session tracking
- Word chain validation logic
- User statistics management and persistence

---

## 🔧 Technologies Used

- **[Sinatra](http://sinatrarb.com/)** – Lightweight Ruby web framework for HTTP routing
- **[ActiveRecord](https://guides.rubyonrails.org/active_record_basics.html)** – ORM for interacting with the database
- **[Redis](https://redis.io/)** – In-memory data structure store for compound noun validation
- **[Rack::Cors](https://github.com/cyu/rack-cors)** – Middleware for Cross-Origin Resource Sharing
- **[SQLite3](https://www.sqlite.org/index.html)** – Simple file-based relational database

---

## 📁 Project Structure

### `app.rb`
Main Sinatra app file:
- Defines core API routes:
  - `GET /game` – Retrieve game data
  - `GET /stats` – Get user statistics
  - `POST /chain` and `POST /soln` – Validate submitted word chains
- Initializes Redis
- Includes helper methods for standardized responses and validation

### `models/user.rb`
Defines the `User` model with the following attributes:
- `uuid`
- `won`
- `current_streak`
- `max_streak`

These fields track user-specific performance stats.

### `models/init.rb`
Initializes all models:
- `User`
- `Game`
- `Solution`

### `db/schema.rb`
Represents the current schema definition for the SQLite3 database:
- Tables: `users`, `games`, `solutions`

### `db/migrate/...`
Includes a migration that updates the `shortest_path` column in the `games` table (from string to integer).

### `utils/csv2redis.rb`
Utility script for populating Redis from a CSV file:
- Normalizes compound nouns
- Loads them into Redis for fast lookup during gameplay

### `spec/app_spec.rb`
RSpec tests to verify:
- Core routes (`/`, `/game`, `/stats`) are working correctly
- Application behavior meets expectations

### `Gemfile`
Declares all gem dependencies:
- `sinatra`, `activerecord`, `redis`, `rspec`, etc.

### `config.ru`
Rack configuration file used to launch the Sinatra server.

### `Rakefile`
Defines database tasks using Rake and ActiveRecord, such as:
- `db:migrate`
- `db:seed`

---

## 🚀 Purpose and Architecture

The backend serves as the core logic engine for a wordchain game. It:

- Validates compound nouns using Redis for quick access
- Tracks and persists user streaks and wins
- Provides HTTP endpoints for frontend integration

### Components:

| Layer         | Technology  | Role                                      |
|---------------|-------------|-------------------------------------------|
| Web Server    | Sinatra     | Handles HTTP requests                     |
| Persistence   | SQLite3     | Stores user and game data                 |
| Caching/Logic | Redis       | Validates compound words and fast lookup  |
| ORM           | ActiveRecord| Maps Ruby objects to DB records           |

---

## Dictionary API

The Dictionary API validates prefix chains of compound nouns:

GET /q?w[]=cow&w[]=bell&w[]=hop&...


It responds with JSON `{“result”:0}` or `{“result”:1}` indicating whether the given array of words is a valid chain of compound nouns.

## Backend API

The API endpoints are as follows:

### GET /game

Responds with the daily game. E.g.

{“from”:”dog”,”to”:”blade”,”steps”:6,”expires”:ts}


### GET /stats

Responds with the user’s stats. E.g.

{“played”:100,”won”:60,”current_streak”:6,”max_streak”:10,”dist”:[60,20,10,2,1,1,7]}


"dist" is a distribution of the user’s solutions: +0 (i.e. shortest valid solution), +1, +2, +3, +4, +5, +more than 5.

### PUT /soln

Allows the user to submit a solution to the daily game. Responds with a success Boolean and the updated user stats.

## Tables

### Games

Associations: `has_many solutions`

Fields: Game number, Date, Start word, End word, Shortest path

### Users

Associations: `has_many solutions`

Fields: UUID, Won, Current_streak, Max_streak, Plus_1, Plus_2, Plus_3, Plus_4, Plus_5, Plus_more

### Solutions

Associations: `belongs_to Game`, `belongs_to User`

Fields: User_id, Game_id, Timestamp, Chain (comma-separated list of words)

## Authentication 

Anonymous identity is provided through a UUID stored in a cookie. Best practices should be adopted for using this cookie to create a secure authenticated session with the user.

## Game Generation

Daily games will be pre-generated (e.g. a year in advance) with offline tools that Ben and Louis have written, manually created, and stored in a table on the backend server.


[Link to my CAD files](https://cad.onshape.com/documents/19c47b2204936e0e6afb5d5f/w/8c687fab2e1043ea59059492/e/a7e77233d09cace7d0dfaa54)