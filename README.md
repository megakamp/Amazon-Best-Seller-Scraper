🧭 Overview

TaskFlow Manager is a comprehensive desktop automation system designed to streamline task management, internal communication, and meeting coordination within organizations.
It’s built with role-based access control, ensuring that managers, supervisors, and employees each have specific permissions aligned with their responsibilities.

The system brings together task delegation, team chat, calendar-based planning, email notifications, and KPI reporting in a single, user-friendly interface.

⚙️ Key Features
🔐 Secure Authentication

Each user logs in with their own credentials.

Passwords are securely stored using bcrypt hashing.

Supports roles: Manager → Supervisor → Employee hierarchy.

🧾 Task Management

Create, assign, and track tasks with detailed descriptions and deadlines.

Role-based delegation:

Managers assign tasks to Supervisors.

Supervisors assign tasks to Employees.

Task progress can be updated via 4 status options:
Received, In Progress, Completed, Delayed.

All changes are logged for transparency.

📅 Calendar Integration

Tasks appear in a built-in calendar view.

Assign tasks by clicking on specific days.

Prevents backdated task assignments for better scheduling accuracy.

💬 Team Chat

Department-based or custom chat groups for internal communication.

Allows both group and private messages.

Keeps conversation history for team visibility.

📞 Meeting Management

Create and manage meetings with Zoom, Teams, or Google Meet links.

Schedule date/time and join meetings with one click.

Ideal for remote or hybrid teams.

✉️ Email Notifications

Automatic email alerts when a new task is assigned.

Uses secure TLS connection for reliable delivery.

📊 KPI & Reporting

Built-in performance metrics:

Total, completed, and delayed tasks.

Average cycle time for task completion.

Helps managers analyze productivity and workload balance.

🧩 Technical Details

Language: Python 3

UI: Tkinter (desktop interface)

Database: SQLite

Security: bcrypt for password hashing, TLS for email

Dependencies: bcrypt, smtplib, sqlite3, tkinter

🚀 Use Cases

Small to medium-sized businesses looking to digitize internal task flow.

Teams that need a transparent, structured task and communication tool.

Organizations seeking a lightweight alternative to enterprise task management suites.

💡 Future Improvements

Real-time chat via WebSocket or socket server.

Integration with Google Calendar and Microsoft Outlook.

2FA (Two-Factor Authentication) for enhanced security.

Dashboard analytics and visual KPI charts.
