# KimberleePhan

## Title: <br> 
Faculity Directory<br>
## Purpose:<br> 
The purpose of this web app is to see different stats at a selected university and their faculty. The target users are anyone who wants to look at different stats a university has.<br>
## Demo: <br>
[Demo Video](https://mediaspace.illinois.edu/media/t/1_e0c9ez2q)<br>
## Installation: <br>
You would need to download this repo. In order for this app to work you would need to install and import the academic world database for SQL, mongoDB, and neo4j. To run the app you would need to use python3 ./app to start the application. You would also need to have the neo4j database up and running before running the add. <br>
## Usage: <br>
To you the application you would need to select a university from the dropdown menu on the top and it would populate 4 of the widgets. You can add a faculty member into the database by inputting their name, position, email, phone, and what university they are affiliated with. You can also see the stats of a faculty member by selecting a member from a drop down menu. <br>
## Design: <br>
For this applicaition I used 3 databases (SQL, mongoDB, and neo4j). I used these databases to make queries to get information to populate 6 widgets. <br><br>
Widget 1: <br>
* Show the number of faculty member for each university
* Used html tags for the title and the number
* Queries the SQL database <br><br>

Widget 2: <br>
* Shows the all the faculty members for the university selected
* Used the DataTable from Dash to show the faculty members
* Queries the SQL database <br><br>

Widget 3: <br>
* Shows the top 10 keywords among faculty at a university
* Used a graph from Dash to display the keywords
* Queries the SQL database<br><br>

Widget 4: <br>
* Inserts a new faculty member into the database
* Uses form inputs to get information from the user
* Uses a submit button to insert the new facutly member
* Inserts into a SQL database <br><br>

Widget 5: <br>
* Shows keywords and the number of publications assocaited with a faculty member
* Uses a dropdown menu to select the faculty member
* Uses html tags to show the keywords and the count number
* Keywords queries from the mongoDB database
* Faculty publication count queries from the neo4j database <br><br>

Widget 6: <br>
* Shows profile of a selected faculty member
* Uses the input from widget 5 to update the elements
* Uses an html image from Dash to display a picture of a faculty member if it exists
* Uses html tags to show the name, position, email and the phone number
* Queries an SQL database <br><br>

## Implementation: <br>
This applcation was written in python, uses the Dash framework, and queries an SQL database, mongoDB database, and neo4j database. To get the widgets to populate I used callback statements. <br>
## Database Techniques: <br>
* Prepared statment
* Parallel query execution
* Stored Procedure <br><br>
## Extra-Credit Capabilities: <br>
* Multi-database querying
## Contribution: <br>
I worked on this application by myself.
