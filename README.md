# UAV Management system

- This project has been deployed using Docker and AWS Elastic Beanstalk. 
- You can access it through this link: http://uav-rental-app2-env.eba-qrzzev3m.us-east-1.elasticbeanstalk.com/
- Project screenshots are at the bottom of the page.



The UAV Management System is a web-based application developed to enable users to ease their part manufacturing and aircraft assembling processes. The processes include many rigid rules in order to achieve an efficient production line.

# Features

### Authorization and Authentication of Personnel.

- **User Registration and Login:** Django's built-in User model is used by the system to manage user accounts. A user is created during the registration process and assigned to a particular team.

- **Session Management:** User credentials are verified and sessions are created with the use login() and authenticate() methods.

- **Role Restrictions:** Each team is responsible for their own parts. If they try  to produce a restricted part type they will get the error message accordingly. Same For the Assembly Team they are only authorized to assemble aircraft which means they are not able to produce parts.
  

### Part and Aircraft Management
- CRUD operations for each part type in the Create Part Page.
- On the Assemble Aircraft page, team officials can produce an aircraft by using the required parts in the desired quantities. If there is a shortage of parts, they will receive an error message accordingly.
- Compability checks are made to prevent assembling different type parts and aircrafts together.
- Assembly team can see the aircrafts produced how many parts used for that aircraft.
  

# Database Structure

## Tables

1. Personnel Model
   - Uses Django's built-in User model for authentication.
   - Has a foreign key for respective their team. ( one to many relationship -> from team to personnel)

2. Team Model

   - Represents the teams it contains one parameter which is team name. (Wing Team, Avionics Team, Tail Team, Fuselage Team, Assembly Team)
   - Restriction checks are done based on team name.
  
3. Part

  - Contains fields for each type (Wing, Fuselage, Tail, Avionics)
  - Tracks assigned aircraft type and team responsible for part creation.
  - Supports the Parts inventory management with `is_assembled` flag.
  - Links to aircraft if used in assembly operation. There for allowing us to keep track which parts are used for which Aircraft.

4. Aircraft

  - Stores the predefined aircraft types ( TB2, TB3, AKINCI, KIZILELMA)
    

# Technological Stack

Backend: Python, Django, Django Rest Framework

Database: PostgreSQL

Frontend: JavaScript, HTML, css

Deployment: Docker, AWS Elastic Beanstalk



## Installation

### Prerequisites

Docker

Docker Compose

PostgreSQL

<br>




# Setup Instructions

1. Clone the Repository:

`git clone https://github.com/kyuceak/case-study.git
cd rental_project`

2. Configure Environment Variables:
- Create a .env file and provide the following details:

```
DB_NAME=<database_name>
DB_USER=<database_user>
DB_PASSWORD=<database_password>
DB_HOST=<database_host>
DB_PORT=5432
SECRET_KEY=<django_secret_key>
DEBUG=True
```

3. Build and start Docker Container

```
docker build -t aircraft-management-system .
docker run -p 80:80 aircraft-management-system
```



- Navigate to http://localhost:8000 in your web browser.


Login Page:






<img width=80% alt="Ekran Resmi 2024-12-22 17 15 58" src="https://github.com/user-attachments/assets/5cc52a08-02ab-4752-850e-d9be85eb5e21" /> 
<br>





Register Page:











<img width=80% alt="Ekran Resmi 2024-12-22 17 15 58" src="https://github.com/user-attachments/assets/322602bd-5ff5-44cf-84eb-9dbfddc4c591" />




Create Part Page:






<img width=80% alt="Ekran Resmi 2024-12-22 17 15 58" src="https://github.com/user-attachments/assets/97a9739c-d898-4f7b-9a6a-d4def1ec12c0" />






Assemble Aircraft Page:





<img width=80% alt="Ekran Resmi 2024-12-22 17 15 58" src="https://github.com/user-attachments/assets/c278b616-2c1d-4d2f-80c8-849950dbc80c" />




List Aircraft Page:

<img width=80% alt="Ekran Resmi 2024-12-22 17 15 58" src="https://github.com/user-attachments/assets/1328e72d-07cb-4456-a3f3-0f4809769448" />



