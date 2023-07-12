# SOEN 6011 - Web Warriors 
## Problem Statement 

Career service applications are digital platforms that help people manage their careers by facilitating career-related tasks and providing resources and support. These programs can be accessed via computers, laptops, or mobile devices, making the services convenient and accessible. Some of the common features of career services applications include: 

1. Job Search and Application
2. Resume/CV Creation and Management
3. Career Assessment and Exploration
4. Skill Development and Training
5. Networking and Mentorship
6. Interview Preparation and Mock Interviews
7. Personalized recommendations and guidance

Some of the well-known tools that help support individuals in their career development include LinkedIn, Handshake, Indeed, CareerBuilder, Glassdoor, Monster etc. Each tool has its own set of features and services to help people with various parts of their career planning, job search, and professional growth. 

The goal of this project is to create a career services platform where students and other job seekers may publish and update their resumes, perform job searches, and track the status of their applications. This service can also allow companies to narrow down their potential employee candidates and assist businesses locate specific people based on their needs, while job seekers can customize their profile to the market. The website can be accessed online with a PC or mobile devices having Internet access. 

## Team Members and Roles
| S. No. | Resource Name | GitHub Username | Role | Responsibilities |
|--------|:-------------:|:---------------:|:----:|:-----------------|
| 1. | Shefali Upadhyaya | Shefali-Upadhyaya | Team Lead | 1. Lead the Team Sprint planning <br> 2. Monitoring progress and feedback <br> 3. Organizing meetings <br> 4. Scrum Board administration <br> 5. Project documentation <br> 6. Communication and Collaboration |
| 2. | Iona Thomas | ionathomas | Software Architect | 1. System design <br> 2. Technology selection <br> 3. Design patterns <br> 4. Application of best practices <br> 5. Project & Technical documentation <br> 6. Communication and Collaboration |
| 3. | Hani Saravanan  | hannaa12 | Front-End Developer | 1. Web development <br> 2. User Interface implementation <br> 3. Responsive design <br> 4. Testing and Debugging <br> 5. Version Control <br> 6. Communication and Collaboration |
| 4. | Ashu Kumar | kin-kins | Back-End Developer | 1. Database management <br> 2. Integration <br> 3. Security and Authentication <br> 4. Testing and Debugging  Version Control <br> 5. Communication and Collaboration                                     |
| 5. | SanVinoth Pacham Sri Srinivasan | sanvinoth | Quality Assurance Engineer | 1. Developing and maintaining quality standards <br> 2. Quality Control <br> 3. Testing and Evaluation <br> 4. Version Control <br> 5. Communication and Collaboration                                    |
| 6. | Jothi Basu Lkv | jothibasulkv01 | Support Engineer | 1. Continuous improvement <br> 2. Bug fixing support <br> 3. Issue resolution <br> 4. Knowledge management <br> 5. Crisis management <br> 6. Communication and Collaboration |

## Project Approach
The approach to the online career services system will differ depending on the type of the users: 

1. Students/Candidates can create an account on the portal. They can log into their account, build/upload their resume, browse through the job board, apply to positions, and track their applications. 
2. Employers can create an account on the portal. They can log into their account, generate, and modify job postings, update the status of the postings, browse through the candidates who have applied for a particular posting, view their resume, and select candidates for an interview. 
3. Admins are super users where they can manage all the user profiles – Employers and Candidates. They can update job postings and the status of the job postings.

The project will last 4 weeks, and the development process will be an adapted version of Agile with an iteration every week. Sprint 1, i.e., the first is dedicated to setting up the development environment. The sprint cycle will be followed from Sprint 1 to Sprint 4. At the end of each iteration, clarifications of user stories will be done, which will be developed in the next iteration. The sprint cycle that will be followed in the project: 

### Sprint 1 (July 5, 2023 – July 12, 2023) schedule:   

| Sprint 1 / Dates | July 5, 2023 | July 6, 2023 | July 7, 2023 | July 8, 2023 | July 9, 2023 | July 10, 2023 | July 11, 2023 | July 12, 2023 |
|:----------------:|:------------:|:------------:|:------------:|:------------:|:------------:|:-------------:|:-------------:|:-------------:|
| | Review Project Description | Scrum Meeting 1 - Online | Working on assigned tasks | Working on assigned tasks | Scrum Meeting 2 - In-Person | Working on assigned tasks | Working on assigned tasks | Finishing touches and submission of Sprint 1 |

### Sprint 2 (July 13, 2023 – July 19, 2023) schedule: TBA
### Sprint 3 (July 20, 2023 – July 31, 2023) schedule: TBA
### Sprint 4 (August 1, 2023 – August 9, 2023) schedule: TBA

## Project Technologies
The system will be deployed on an AWS EC2 instance or localhost. The database for the application will be hosted on an AWS RDS (Relational Database Service). To facilitate communication between the Docker containers and the host environment, we will utilize port mapping with the application's services exposed on port 8000. This architecture allows for a scalable and reliable deployment of the web app, leveraging the infrastructure and services provided by AWS. The EC2 instance handles the web server functionality, while the RDS database ensures efficient storage and retrieval of data for the application.

![Technology Overview](https://github.com/kin-kins/Web_Warriors-SOEN6011summer2023/blob/main/Sprint%201/arch%20overview.png)

- **Programming Language:** Python 3.9
- **Python Packages:**
  - pymysql
  - hashlib
  - flask
- **Containerization tool:** Docker
- **Framework:** Flask
- **Database:** AWS RDS MySQL
- **IDE:** VS Code, PyCharm
- **Version Control:** Github CLI, Github Desktop
- **Testing Framework:** To be decided
- **Restful API**
