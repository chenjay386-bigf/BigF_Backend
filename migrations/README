# BIGF Backend

Backend API for **BIGF**, a food brand and community platform built around products, recipes, social content, challenges, voting, rewards, and Pioneer Members.

The backend provides the API, authentication, database models, challenge management, social-media submissions, community functionality, and shop functionality required by the BIGF platform.

---

## Table of Contents

* [About BIGF](#about-bigf)
* [Backend Goals](#backend-goals)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Core Features](#core-features)
* [Authentication](#authentication)
* [Database](#database)
* [API Resources](#api-resources)
* [Challenge System](#challenge-system)
* [Social Media Submissions](#social-media-submissions)
* [Shop System](#shop-system)
* [Environment Variables](#environment-variables)
* [Installation](#installation)
* [Running the Backend](#running-the-backend)
* [Database Migrations](#database-migrations)
* [Testing](#testing)
* [Development Workflow](#development-workflow)
* [Future Improvements](#future-improvements)

---

## About BIGF

BIGF is a food brand that uses digital community and challenge marketing to grow product awareness and customer engagement.

The website is **not primarily a challenge website**.

The main business journey is:

```text
Discover BIGF
      ↓
Understand BIGF Products
      ↓
Discover Flavors
      ↓
Build Trust
      ↓
Purchase / Try BIGF
      ↓
Create & Share Content
      ↓
Join BIGF Challenge
      ↓
Vote / Participate
      ↓
Become a Pioneer Member
```

The challenge system is a **growth and marketing tool for the BIGF food brand**.

---

## Backend Goals

The backend is responsible for:

* User registration and authentication
* User profiles
* Following and community relationships
* Recipes
* Ingredients
* Posts
* Media
* Comments
* Likes
* Ratings
* Saved recipes
* Reshares
* Social-media submissions
* Challenges
* Challenge submissions
* Challenge voting
* Challenge rewards
* Products
* Categories
* Shopping cart
* Orders
* Payments
* Delivery
* Achievements
* Pioneer Member functionality

---

## Technology Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Marshmallow
* Flask-JWT-Extended
* Flask-Bcrypt
* Flask-CORS
* python-dotenv

### Database

* PostgreSQL

### API Architecture

The backend follows a resource-based REST API architecture.

```text
Client
  ↓
Flask API
  ↓
Resources
  ↓
Schemas
  ↓
Models
  ↓
PostgreSQL
```

---

## Project Structure

A simplified backend structure:

```text
BIGF-BACKEND/
│
├── app/
│   ├── __init__.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── profile.py
│   │   ├── recipe.py
│   │   ├── ingredient.py
│   │   ├── post.py
│   │   ├── media.py
│   │   ├── comment.py
│   │   ├── like.py
│   │   ├── rating.py
│   │   ├── saved_recipe.py
│   │   ├── reshare.py
│   │   ├── social_media_submission.py
│   │   ├── challenge.py
│   │   ├── challenge_submission.py
│   │   ├── challenge_vote.py
│   │   ├── challenge_reward.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── cart_item.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   ├── delivery.py
│   │   ├── achievement.py
│   │   └── user_achievement.py
│   │
│   ├── resources/
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── follow.py
│   │   ├── recipe.py
│   │   ├── ingredient.py
│   │   ├── post.py
│   │   ├── media.py
│   │   ├── comment.py
│   │   ├── like.py
│   │   ├── rating.py
│   │   ├── saved_recipe.py
│   │   ├── reshare.py
│   │   ├── social_media_submission.py
│   │   ├── challenge.py
│   │   ├── challenge_submission.py
│   │   ├── challenge_vote.py
│   │   ├── challenge_reward.py
│   │   └── shop.py
│   │
│   ├── schemas/
│   │   └── ...
│   │
│   ├── extensions.py
│   └── ...
│
├── migrations/
│
├── tests/
│
├── seed.py
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Core Features

### Authentication

Users can:

* Register
* Login
* Authenticate using JWT
* Access protected endpoints
* Manage their profile
* Update account information

Passwords are securely hashed using Flask-Bcrypt.

---

### Profiles

Users have profiles containing information such as:

* Username
* Profile information
* Followers
* Following
* Posts
* Recipes
* Challenge participation
* Achievements
* Pioneer Member status

---

### Community

The community system supports:

* Following users
* Creating posts
* Media
* Comments
* Likes
* Ratings
* Saving recipes
* Resharing content

---

## Challenge System

The BIGF challenge system is one of the main marketing components of the platform.

A challenge can contain:

* Title
* Description
* Start date
* End date
* Rules
* Prize/reward information
* Submission requirements
* Status

The challenge architecture consists of:

```text
Challenge
   ↓
Challenge Submission
   ↓
Challenge Vote
   ↓
Challenge Reward
```

### Challenge Flow

```text
User discovers BIGF
       ↓
User discovers current challenge
       ↓
User purchases / uses BIGF
       ↓
User creates content
       ↓
User publishes content on TikTok
       ↓
User submits TikTok URL
       ↓
Submission is reviewed
       ↓
Community votes
       ↓
Winner selected
       ↓
Reward issued
```

The current challenge strategy uses **TikTok submissions rather than local video uploads**.

---

## Social Media Submissions

Users can connect their BIGF challenge participation to external social platforms.

The current challenge flow focuses on TikTok:

```text
Create Video
     ↓
Publish on TikTok
     ↓
Copy TikTok URL
     ↓
Paste URL into BIGF
     ↓
Submit
     ↓
Voting
```

This allows BIGF to use customer-generated content as a social growth mechanism.

---

## Shop System

The backend supports BIGF product functionality.

The shop architecture includes:

```text
Category
   ↓
Product
   ↓
Cart
   ↓
Cart Item
   ↓
Order
   ↓
Payment
   ↓
Delivery
```

The shop allows the platform to connect product discovery with customer engagement.

The strategic objective is:

```text
Product Discovery
       ↓
Purchase
       ↓
Product Experience
       ↓
Social Content
       ↓
Challenge Participation
```

---

## Environment Variables

Create a `.env` file in the backend root.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/bigf
JWT_SECRET_KEY=your-secret-key
SECRET_KEY=your-secret-key
```

Do not commit `.env` to Git.

---

## Installation

Clone the repository and enter the backend directory:

```bash
git clone <repository-url>
cd BIGF-BACKEND
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Setup

Create a PostgreSQL database for BIGF.

Configure the database connection inside `.env`.

Then initialize migrations if required:

```bash
flask db init
```

Create a migration:

```bash
flask db migrate -m "Initial migration"
```

Apply migrations:

```bash
flask db upgrade
```

---

## Seed Data

The project can use `seed.py` to populate the database with development data.

Run:

```bash
python seed.py
```

Seed data may include:

* Users
* Products
* Categories
* Recipes
* Challenges
* Rewards
* Sample posts

---

## Running the Backend

Start the Flask development server:

```bash
flask run
```

Or, depending on the project entry point:

```bash
python run.py
```

The API will normally be available at:

```text
http://127.0.0.1:5000
```

---

## API Resources

The backend resource architecture is organized around the following modules:

| Resource                | Purpose                       |
| ----------------------- | ----------------------------- |
| Auth                    | Registration and login        |
| Profile                 | User profile management       |
| Follow                  | Following users               |
| Recipe                  | Recipes                       |
| Ingredient              | Recipe ingredients            |
| Post                    | Community posts               |
| Media                   | Media management              |
| Comment                 | Post comments                 |
| Like                    | Likes                         |
| Rating                  | Ratings                       |
| Saved Recipe            | Saved recipes                 |
| Reshare                 | Content reshares              |
| Social Media Submission | External social submissions   |
| Challenge               | Challenge management          |
| Challenge Submission    | User challenge entries        |
| Challenge Vote          | Community voting              |
| Challenge Reward        | Challenge prizes              |
| Shop                    | Products, cart and purchasing |

---

## API Authentication

Protected endpoints require a JWT token.

Example:

```http
Authorization: Bearer <access_token>
```

Authentication flow:

```text
POST /auth/register
        ↓
POST /auth/login
        ↓
JWT Access Token
        ↓
Protected API Requests
```

---

## Testing

Run the test suite with:

```bash
pytest
```

Tests should cover:

* Authentication
* Models
* Schemas
* Resources
* Challenge functionality
* Voting
* Product functionality
* Cart functionality
* API validation

---

## Development Workflow

Recommended workflow:

```text
1. Create/update model
        ↓
2. Create/update schema
        ↓
3. Create/update resource
        ↓
4. Register endpoint
        ↓
5. Create migration
        ↓
6. Apply migration
        ↓
7. Seed development data
        ↓
8. Write tests
        ↓
9. Run tests
        ↓
10. Connect frontend
```

---

## Security

The backend should:

* Never store plain-text passwords
* Never commit secrets
* Validate incoming data
* Protect authenticated routes
* Validate JWT tokens
* Restrict CORS appropriately in production
* Validate challenge submissions
* Prevent duplicate voting where applicable
* Validate product/order information
* Use environment variables for secrets

---

## Production Deployment

Before production deployment:

* Configure production PostgreSQL
* Set secure environment variables
* Disable Flask debug mode
* Configure production CORS
* Configure HTTPS
* Run database migrations
* Configure logging
* Configure payment integration
* Configure media storage
* Configure production JWT secrets

---

## Future Improvements

Potential future backend features include:

* Advanced product inventory
* Order tracking
* Payment gateway integration
* Delivery integration
* Admin dashboard API
* Challenge analytics
* Social-media verification
* Automated winner calculations
* Push notifications
* Email notifications
* Referral system
* Pioneer Member rewards
* Product reviews
* Coupon and promotional systems
* QR-code campaign tracking
* Marketing analytics

---

## BIGF Architecture Principle

The backend supports a simple business principle:

```text
BIGF PRODUCT
     ↓
CUSTOMER
     ↓
EXPERIENCE
     ↓
CONTENT
     ↓
SOCIAL SHARING
     ↓
CHALLENGE
     ↓
COMMUNITY
     ↓
LOYALTY
```

The technology exists to support **BIGF product growth**, with community and challenges acting as growth mechanisms.

---

## Status

**Project:** BIGF
**Component:** Backend API
**Architecture:** Flask REST API
**Database:** PostgreSQL
**Authentication:** JWT
**Status:** Active Development
