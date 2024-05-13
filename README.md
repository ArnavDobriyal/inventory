
# Inventory Management System

## Overview:

This Inventory Management System is a web application built using FastAPI, designed to facilitate inventory management tasks for both owners and customers. It allows users to sign up, log in, view their respective dashboards, manage inventory items, track item expiry, and perform replenishment actions. The system distinguishes between owners and customers, providing tailored functionalities to each user type.

## Features:

### 1. User Authentication and Registration:
   - **Sign Up:** Users can create new accounts by providing their name, phone number, email, and password.
   - **Login:** Existing users can log in using their username (or email) and password.
   - **Authentication:** Upon login, the system verifies the user's credentials against stored records to grant access.

### 2. Dashboard:
   - **User-Specific Dashboards:** Depending on the user type (admin or customer), the system presents a tailored dashboard upon login.
   - **Overview:** The dashboard provides an overview of relevant information, such as total inventory items, expired items, and pending actions.
   - **Navigation:** Users can navigate to different sections of the application from the dashboard, such as inventory management, replenishment, and customer details.

### 3. Inventory Management:
   - **Owner's Inventory:** Owners can view their inventory, including details like item name, expiry date, size, quantity, and type (e.g., perishable/non-perishable).
   - **Adding Items:** Owners can add new items to their inventory, specifying relevant details for each item.
   - **Customer Inventory:** Customers can view the items available to them and manage their inventory, including deleting items they no longer need.

### 4. Item Expiry Tracking:
   - **Expired Items:** Both owners and customers can track expired items. The system displays relevant details about expired items, such as name, expiry date, and quantity.
   - **Actionable Information:** Users can take necessary actions, such as replenishment or removal, based on the expiry details provided.

### 5. Replenishment:
   - **Owner's Replenishment:** Owners can view items that need replenishment, such as low stock or expired items.
   - **Customer Replenishment:** Customers can also view items that need replenishment, ensuring they have access to fresh inventory when needed.

### 6. Customer Management:
   - **Customer Details:** Owners can view details of all customers, facilitating customer management tasks such as tracking customer orders or preferences.
   - **Customer Deletion:** Owners have the ability to delete customer accounts if necessary, providing administrative control over the user base.

### How It Works:
   - The system is built using FastAPI, a modern web framework for building APIs with Python.
   - It utilizes asynchronous programming to handle multiple concurrent requests efficiently.
   - Database operations are performed using SQL queries, allowing for data retrieval, insertion, and deletion.
   - HTML templates are rendered using Jinja2Templates, providing dynamic content generation for web pages.
   - User sessions are managed using a Singleton class (`SessionManager`), ensuring consistent user authentication across requests.
   - The system follows the Model-View-Controller (MVC) architectural pattern, separating concerns for better code organization and maintainability.

### Customization:
   - The system can be customized to add new features, such as advanced search functionality, reporting tools, or integration with external APIs for real-time data updates.
   - UI/UX enhancements can be made to improve the overall user experience, such as implementing interactive data visualization or incorporating modern design principles.
   - Additional security measures can be implemented to protect user data and prevent unauthorized access, such as role-based access control (RBAC) or two-factor authentication (2FA).
   - Performance optimization techniques can be applied to improve application responsiveness and scalability, such as caching frequently accessed data or optimizing database queries.

