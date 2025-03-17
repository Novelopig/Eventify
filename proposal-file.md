# Proposal for Eventify - Event Planning Portal

**Date:** 01-21-2025  
**Teamenbers:** Fangfang Chen, Aaron James Asuncion, Byeonggil Kim, Changheon Oh

## Project Overview:

Eventify is a web-based event planning portal designed to simplify the organization, management, and discovery of events. It caters to individual users, event planners, and administrators by providing a seamless interface for creating, managing, and discovering events. The project emphasizes simplicity, leveraging Django and Python for all core functionalities, and uses the default SQLite database for straightforward implementation.

---

## Benefits of Eventify

- Simplifies event creation and management.
- Empowers users with personalized features like history tracking and private collections.
- Provides admins with robust tools for moderation and analytics.
- Built with a lightweight, efficient technology stack for ease of maintenance.

---

## Team Members and Roles

- **Aaron James Asuncion**: Design Lead (Figma, HTML/CSS)  
  Responsible for creating the visual identity, wireframes, and mockups using Figma.
- **Changheon Oh**: Front-End Developer (Django Templates, HTML/CSS)  
  Focuses on implementing the user interface and ensuring responsiveness.
- **Fangfang Chen**: Back-End Developer (Django, Python, SQL)  
  Manages the Django backend, including models and views.
- **Byeonggil Kim**: Repository Manager  
  Manages the GitHub repository, tracks issues, ensures adherence to version control, and oversees code reviews and CI/CD guidelines.

---

## Users

- **Primary Users**: Individuals or businesses looking to create and share events. Users looking to browse, search for, and save local events of interest. Both Event Organizers and Event Attendees have the same access.

- **Admin Users**: Managing users, events, and content within the system.

---

## Features

### As a user, I can:

- **Create, Edit, and Delete Events**  
  Description: Users can create, update, and remove the events that they have created. When creating events, users can input essential details such as the event title, description, start, end date and time, max attendees, location of the event. They also have the option to upload image for events, categorize events.

- **Browse, Sort, Filter, and Search Events**  
  Description: The platform offers robust browsing functionality, allowing users to sort events by categories like location, date, or popularity. Filters can be applied to narrow down searches to specific interests or types of events (e.g., concerts, conferences, parties).

- **Like and Unlike Events**  
  Description: Users can mark events they like, which are then stored in their profile. If they change their mind, they can, unlike the event, and it will be removed from their linked list.

- **Flag Inappropriate or Erroneous Events**  
  Description: If a user finds an event that is inappropriate or contains incorrect information, they can flag it for review by an administrator. Flagged events are logged and visible in the admin panel for further action.

- **Add Comments on Events**  
  Description: Users can interact with events by leaving comments. These comments are shown publicly.

- **Save Events to Favorite**  
  Description: Users can save events that interest them to a Favorite list, giving them easy access later.

- **Browse, Sort, Filter, and Search Favorites events**  
  Description: Saved events in a user's Favorite list can be organized with similar sorting and filtering options as the broader event listings. Users can look up events by name, type, or date in their Favorate list.

- **View User Profile/dashboard**  
  Description: A user’s Profile/dashboard can create event and will display events they’ve added to favorite and attended

- **Create and Manage Accounts**  
  Description:Users can create an account, they have login to access saved Favorite list, liked events, and other personalized features. They can change their password and profile picture, username and bio.

### As an admin, I can:

- **Edit and Delete User Accounts**  
  Description: Admin users have full control over user accounts. They can view, modify, or delete accounts if necessary, ensuring the platform remains free from spam or inappropriate activity.

- **Edit and Delete Events**  
  Description: Admins can edit or remove any event listed on the platform. This includes correcting event details, removing erroneous content, and ensuring that all listed events comply with platform guidelines.

- **Edit and Delete Comments**  
  Description: Admins have the ability to moderate comments, removing comments and events.

- **Review Flagged Events**  
  Description: Admins can review and remove flagged events.

- **Integrate Maps API**
  Description: Admins can integrate Maps into the platform to enhance event location features. This will allow users to view event locations on an interactive map, improving accessibility and clarity for attendees.

- **Generate Statistics**  
  Description: Admins can access real-time statistics on platform activity, including the number of active users, events, flagged content, and more(if nessesary).

- **Manage Admin Panel**
  Description: The admin panel provides a comprehensive interface for managing users, events, comments, flagged content, and generating statistics. It features customizations to Django’s default admin interface, offering a more user-friendly layout. Admins can view detailed logs and analytics, review flagged content, and perform moderation actions with a few clicks.

---

## Technologies Used

Eventify will be developed using the following technologies:

- **Django (Python)**: The backbone of the backend functionality, Django allows for efficient handling of requests, views, models, and templates. Its built-in features, such as the authentication system, make it ideal for this project.
- **SQLite**: Chosen for its lightweight nature, SQLite provides a simple yet powerful database solution that requires minimal setup and is easy to manage, making it a suitable choice for Eventify.
- **Django Authentication System**: Handles all user authentication processes, ensuring that users can securely log in, register, and manage their profiles.
- **Django Admin Panel**: Customized to suit the needs of Eventify, the admin panel provides a user-friendly interface for managing users, events, and comments, along with essential moderation and reporting tools.
- **Django Templates**: Used to render HTML for user-facing pages, templates ensure that the site's look and feel are consistent and can be easily updated when necessary.
- **Third-Party API Integration**: The platform will integrate a third-party map API to enhance event location features. This integration will allow users to view event locations on an interactive map, improving accessibility and clarity for event attendees. The map will provide users with directions and help them easily find the event venue.

---

## Page Summaries (A simplified section for designers to reference to support them in getting started)

- **Homepage**  
  The homepage will serve as the entry point for users to explore various events. It will include a search bar, event categories, and quick links to popular events. Featured events will be displayed, allowing users to easily browse events.

- **Event Listing Page**  
  This page will display a list of events. Users can sort, filter, and search for events by date, location, and type. Each event listing will include a brief summary with a link to the event details page.

- **Event Details Page**  
  The event details page will provide comprehensive information about a specific event, including date, time, location, and a detailed description. Users can like, comment on, and save the event to their collection from this page.

- **Sign Up Page**  
  The Sign up page is showing a form for the user to sign up an account, including user name, email, password (Ffchen234456, at least 8 characters).

- **Login Page**  
  The login page will allow users to securely access their accounts. Users can log in with their email and password, or reset their password if necessary.

- **User Dashboard**  
  The user dashboard will Users can create, update, and remove the events that they have created and display all of a user’s Favorate events, and a history of events they’ve attended.

- **Admin Panel**  
  The admin panel will allow administrators to manage users, events, comments, and flagged content. It will also provide statistical insights into event activity and user engagement.

---

## Project Milestones

### Week 1:Project Kickoff

- Set up GitHub repository and branch protection rules.
- Create and submit the Request for Proposal (RFP).
- Create and submit the Proposal document including the application features and architecture, define the milestones and project timeline.

### Week 2: Initial Setup & Core Features & User Authentication

- Draft Visual guidelines.
- Wireframes and Mockups for key pages (home, event listing, Event Details, event details, login) in Figma (Figma design file or FigJam file).
- Data model: Entity-Relationship diagram. JPEG or PNG image.
- Django Setup: Set up the Django project, create initial models (User, Event, Comment, etc.).
- Set Up URLs for Routing.
- User Authentication: Set up user authentication, registration, and account management.
- Event Management: Develop CRUD operations for events.
- Installation Steps with Markdown file.

### Week 3:Search, Sorting, and Filtering

- Search Functionality: Implement search functionality for users to search for events based on keywords.
- Sort and Filter: Add event sorting (by date, popularity, etc.) and filtering options (e.g., event type, location) for users.
- Event Interaction: Implement the Like/Unlike, Save to Favorites, and Flag inappropriate content features.
- Admin Panel Enhancements: Customize Django’s admin panel to better manage events, users, and flagged content.
- Map API Finalization: Enhance the map functionality for the admin panel, allowing full event location features.

### Week 4: User Interaction & Admin Features

- Commenting on Events: Allow users to comment on events, with moderation capabilities in the admin panel.
- Admin Moderation: Implement admin functionality for editing and comments, deleting events, Editing and deleting user accounts, managing flagged content(approve or remove).
- User Profile Enhancements: A list of events the user has created, liked, or saved. Profile customization options (profile picture, bio).
- Testing & Debugging: Begin testing core features (event creation, user profile, search functionality).
- Styling Pages: Complete styling for all pages based on visual guidelines.
- Performance Optimization: Review and optimize the platform’s performance for user interaction and admin features.

### Week 5:Final Testing & Documentation

- Final Testing: Conduct extensive testing across all features (event management, user interactions, search and filtering ...).
- Bug Fixing: Address any issues identified during testing, and finalize debugging.
- Documentation:Create a user manual and API documentation.
- Final review of the project, making sure all features are integrated and functional.
- Submit the final project for evaluation.

---

## Expected Deliverables

- Request for Proposal (RFP): Due: end of week 1 (Format: Markdown file)
- Proposal Document: Due: end of week 1 (Format: Markdown file)
- Visual Guidelines: Due: end of week 2 (Format: Figma design file)
- Figma Wireframes: Due: end of every week (Format: Figma design file or FigJam file)
- Mockups: Due: end of every week (Format: Figma design document)
- Installation steps:Due: end of week 2(Format: Markdown file)
- Data model: Entity-Relationship Diagram.Due: end of week 2 (Format: JPEG or PNG image)
- Source code:Due: end of every week
- Final presentation:Due: last class(Format: slide deck)
