# Yoga Studio Web App

# Table of Contents

- [Yoga Studio Web App](#yoga-studio-web-app)
  - [Introduction](#introduction)
  - [Views](#views)
    - [Home Page](#home-page)
    - [Home Page for Logged-in Users](#home-page-for-logged-in-users)
    - [Login](#login)
    - [Registration](#registration)
    - [Update Profile](#update-profile)
    - [Booking View](#booking-view)
    - [Cancel Booking](#cancel-booking)
    - [Add Comment](#add-comment)
    - [Delete Comment](#delete-comment)
    - [Logout](#logout)
  - [Testing](#testing)
    - [Automated Tests](#automated-tests)
    - [Running Tests](#running-tests)
  - [Design and User Stories](#design-and-user-stories)
    - [Design](#design)
      - [Technical Architecture](#technical-architecture)
      - [User Interface (UI/UX)](#user-interface-uiux)
    - [User Stories](#user-stories)
      - [Visitor](#visitor)
      - [Logged-in User](#logged-in-user)
    - [Implemented Features](#implemented-features)
  - [Deployment](#deployment)
    - [GitHub and Heroku Deployment](#github-and-heroku-deployment)
  - [Credits](#credits)



## Introduction
This Django web application provides functionalities for user authentication, profile management, class booking, and commenting on yoga liveclasses.

![Mockup](../yogaMemberFullStack/yogaapp/static/yogaapp/static/images/mockup.jpg)

## Views

### Home Page
**URL:** `/`

**Description:** Renders the homepage of the Yoga Studio.

### Home Page for Logged-in Users
**URL:** `/home/`

**Description:** Renders the homepage for logged-in users, displaying all available live classes and the user's booked classes.

### Login
**URL:** `/login/`

**Description:** Handles user authentication. Uses Django's built-in `AuthenticationForm` for logging in users.

### Registration
**URL:** `/register/`

**Description:** Handles user registration. Uses a custom `UserRegisterForm` for registering new users.

### Update Profile
**URL:** `/update-profile/`

**Description:** Handles profile updates for logged-in users. Uses a `ProfileUpdateForm` for updating user profiles, including password updates.

### Booking View
**URL:** `/booking/<class_id>/`

**Description:** Handles booking of a live class for logged-in users. Creates a booking if the user has not already booked the class.

### Cancel Booking
**URL:** `/cancel-booking/<class_id>/`

**Description:** Handles cancellation of a booking for a live class. Deletes the booking if it exists for the logged-in user.

### Add Comment
**URL:** `/add-comment/<class_id>/`

**Description:** Handles adding a comment to a live class for logged-in users. Creates a comment associated with the specified live class.

### Delete Comment
**URL:** `/delete-comment/<comment_id>/`

**Description:** Handles deletion of a comment for logged-in users. Deletes the comment if the user is the owner of the comment.

### Logout
**URL:** `/logout/`

**Description:** Handles user logout. Logs out the current user session.

## Testing

### Automated Tests

The following table summarizes the results of automated tests for each view function:

| View Function            | Test Description                                | Test Result |
|--------------------------|-------------------------------------------------|-------------|
| `home`                   | Renders homepage correctly.                     | Passed      |
| `home_logged_in`         | Renders logged-in homepage correctly.           | Passed      |
| `login_view`             | Logs in user with valid credentials.            | Passed      |
|                          | Shows error with invalid credentials.           | Fail      |
| `register_view`          | Registers user with valid data.                 | Passed      |
|                          | Shows errors with invalid data.                 | Passed      |
| `update_profile`         | Updates user profile correctly.                 | Passed      |
|                          | Shows errors with invalid data.                 | Fail      |
| `booking_view`           | Books a class for logged-in user.               | Passed      |
| `cancel_booking`         | Cancels a booked class for logged-in user.      | Passed      |
| `add_comment`            | Adds a comment to a live class.                 | Passed      |
| `delete_comment`         | Deletes user's own comment.                    | Passed      |
| `logout_view`            | Logs out the user successfully.                 | Passed      |

### Fail Explanations
- Frequently tried to fix the error with error message showing in login and update, but with no luck. 

### HTML, CSS Testing
- Shows error and warnings:
Due to limited time I have decided to continue with my project and sumbit it anyway because it mainly works when deployed. If I had more time I would have tried more to fix the errors and warnings. 

### Lighthouse testing
- Over 90 in score in all categories.
![Lighthouse](../yogaMemberFullStack/yogaapp/static/yogaapp/static/images/lighthousetesting.png)

### Running Tests

To run these tests locally:

1. Ensure all dependencies are installed using `pip install -r requirements.txt`.
2. Run the tests using Django's test runner:

# Design and User Stories

## Design

### Technical Architecture

The application is built using Django, following a typical MVC (Model-View-Controller) architecture, where:

- **Models**: Define data models such as `User`, `LiveClass`, `Booking`, and `Comment`.
- **Views**: Handle the logic to process user requests and render data.
- **Templates**: Utilize Django's template system to create HTML interfaces.

### User Interface (UI/UX)

The interface is designed to be simple and intuitive for users:

- **Homepage**: Provides an overview of available classes and the user's booked classes.
- **Login and Registration**: Uses Django's authentication system for user login and registration forms.
- **Profile Management**: Allows users to update their profiles and change passwords.
- **Class Booking**: Enables users to book live classes.
- **Comments**: Enables users to add and delete comments on live classes.

## User Stories

### Visitor

1. **As a visitor, I want to see a list of available classes and their details.**
2. **As a visitor, I want to register as a user to book classes and add comments.**

### Logged-in User

1. **As a logged-in user, I want to log into my profile to manage my bookings.**
2. **As a logged-in user, I want to update my profile information and change my password.**
3. **As a logged-in user, I want to book live classes and see a list of my bookings.**
4. **As a logged-in user, I want to add comments on live classes and delete my own comments.**

## Implemented Features

The application implements the following features to fulfill the user stories:

- **User Authentication and Authorization** using Django's built-in `User` model.
- **Profile Management** with the ability to update user information including password.
- **Class Booking** with management of booking statuses and display of booked classes.
- **Comments** functionality allowing users to add and delete comments on live classes.

## Deployment
The site was deployed to GitHub Pages. The steps to deploy are as follows:
1. In the GitHub repository, navigate to the **Settings** tab.
2. From the source section drop-down menu, select the **Master Branch**.
3. Once the master branch has been selected, the page will automatically refresh with a detailed ribbon display to indicate the successful deployment.


### Credits
 - Fonts are from https://www.googlefont.com
 - favicon are from https://www.flaticon.com
 - Images are from https://www.canva.com
 - Social media icons in footer are from https://www.flaticon.com
