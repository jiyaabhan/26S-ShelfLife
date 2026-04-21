# ShelfLife

ShelfLife is a course materials marketplace built for Northeastern students. The goal is to make it easier for students to buy and sell textbooks, calculators, lab kits, software access codes, and other class-related materials without having to rely on general resale apps that are not organized around courses.

## Project Overview

A lot of students finish a class and no longer need the materials they bought for it, while other students are just starting that same course and need those exact items. ShelfLife is designed to connect those two groups in a way that feels more useful than a generic marketplace.

What makes the project different is that listings are tied to courses. Instead of searching through unrelated posts, buyers can look up materials by course and sellers can price items with more context. The platform also includes features that support trust, like seller ratings and pricing history, so users can make more informed decisions.

## Main User Roles

ShelfLife is built around four user roles:

### Seller
A seller can create listings for course materials, check past prices before posting, update listing details, and manage active or sold items.

### Buyer
A buyer can search for materials by course, compare listings, save items to a wishlist, and view seller ratings before making a decision.

### Data Analyst
A data analyst can look at marketplace activity, pricing trends, course-level demand, and seller performance across the platform.

### Admin
An admin can manage the course catalog, review flagged listings, monitor transactions, and handle account or listing issues when needed.

## Core Features

Some of the main features planned for ShelfLife include:

- Course-based search for materials.
- Listings for textbooks, calculators, lab kits, and other academic supplies.
- Historical price information to help users judge whether a listing is reasonable.
- Seller ratings and reviews.
- Wishlist support for buyers.
- Analytics views for trends, demand, and seller activity.
- Admin tools for course management and moderation.

## Why We Built It

The main idea behind ShelfLife came from a common student problem: course materials are expensive, but many of those materials are only used for one semester. At the same time, students often have perfectly usable items sitting around after a class ends.

We wanted to build something that felt more targeted than Facebook Marketplace or other general resale platforms. By organizing listings around actual courses, ShelfLife is meant to make the buying and selling process more practical for students.

## Repository Structure

This repository currently includes the following main folders:

- `app/` – Streamlit front end.
- `api/` – Flask API and backend routes.
- `database-files/` – SQL files for database setup and sample data.
- `datasets/` – Data files used by the project if needed.
- `docs/` – Supporting project documentation.
- `ml-src/` – Space for model-related or analytics-related work if used.

## Tech Stack

The project is being built with:

- Python
- Flask
- Streamlit
- MySQL
- Docker / Docker Compose

## Getting Started

### Prerequisites

Before running the project, make sure you have:

- A GitHub account
- A Git client such as GitHub Desktop or VS Code
- Docker Desktop
- Python 3.11 if you plan to run parts of the project outside Docker

### Running the Project

From the root of the repository, run:

```bash
docker compose up -d
```

This should start the project services in Docker.

### Database Note

Any `.sql` files inside the `database-files/` folder are executed when a new database container is created. If the schema or sample data changes, the database container may need to be recreated so those files run again.

## Demo Scenario (Key Features to Show)

- A buyer searches for a specific course (for example, “CS 3200”) and views the listings that are tied to that course.

- A seller creates a new listing for a textbook, including entering a title, description, price, and linking the listing to the correct course.

- The interface shows how buyers can scan and compare multiple listings for the same course material to find an option that fits their budget.

- If available, an admin or analytics view is opened briefly to show how the team can monitor marketplace activity and course level demand.

- While the application is running, we point out the tech stack in use (Streamlit front end, Flask API, MySQL database, and Docker) and how the pieces fit together.

## Testing

We manually test ShelfLife by stepping through the main user flows from the perspective of each role. For buyers, we verify that searching by course, opening a listing, and moving between listings works without errors. For sellers, we create and update listings to confirm that forms save correctly and data appears in the expected place. When admin or analytics views are available, we open them to make sure pages load, filters behave as expected, and summary information matches the underlying sample data.

## Current Status

ShelfLife is being developed as part of the Spring 2026 CS 3200 course project at Northeastern University. This README will continue to be updated as the application is finalized and more implementation details are confirmed.

## Team

- Ariz Nawaz
- Madhav Sabu
- Vineeth Kanpa
- Jiya Bhan
- Keila Olaverria

## Demo Video

Demo link: to be added
