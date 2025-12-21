# Mini Instagram Clone with Django

A mini Instagram-like social media application built using Python and Django, focusing on core social media functionalities. The application includes user authentication, profile management, follow and unfollow system, post creation, likes, comments, and a dynamic feed based on followed users.

The project was developed mainly for learning purposes, with an emphasis on understanding Django backend workflows, database relationships, and feature integration.

# live preview--> hikniraula.pythonanywhere.com
---

## Features

### Authentication & Profiles
- User signup, login, and logout
- Login using username or email
- Automatic profile creation
- Profile editing with image, bio, location, and website

### Follow System
- Follow and unfollow users
- Follow-back logic
- Friend declaration for mutual followers
- Separate pages for Following, Followers, and Friends

### Feed System
- Prioritized feed based on followed users
- Seen-post tracking
- Reset feed history
- "See more" functionality

### Posts
- Upload posts with image and caption
- Edit and delete own posts
- Hashtag extraction from captions
- Detailed post view

### Like and Save Posts
- Like and unlike posts with real-time updates
- Save and unsave posts
- Automatic update of like and save counts using Django signals
- Dedicated page showing users who liked a post

### Comments
- Real-time comment creation
- Comment deletion by post owner
- Edit and delete permissions for comment owner
- Comment count updates using signals
- Detailed comment view per post

### Direct Messaging
- One-to-one private chat
- Support for text and image messages
- Conversation inbox

---

## Tech Stack

- Backend: Python, Django
- Frontend: HTML, CSS, JavaScript (AJAX)
- Database: SQLite (default)

---

## Development Approach

Frontend layout, styling, and JavaScript (AJAX) interactions were primarily developed with assistance from AI tools like CHATGT & DEEPSEEK and online learning resources. I have a basic understanding of the frontend flow and used these tools mainly to improve productivity and learn implementation patterns.

Backend development, including authentication, database relationships, feed logic, follow system, and post interaction handling, was implemented by me, with some ideas and optimizations taken from AI tools and tutorials. All assisted code was reviewed and adapted before use.

---

## Notes

This project is intended for learning and portfolio purposes. Further improvements can be made in terms of performance, security, and user interface.

---

## Author

Ashik Niraula
