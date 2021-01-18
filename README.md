# Mini-Pharmacy-Database-Management-System

A pharmaceutical company is present in multiple areas-various branches, and has many employees working in each branch.Each branch has a unique Branch ID. Each Branch sells multiple medicines and keeps a track of quantity of each item present. Each item has a unique code, and a fixed price associated with it.
Customers of this pharmaceutical company can choose to be members. Members are awarded with points each time on their purchase of any item from the store. These points can be redeemed to avail gifts.
Each gift costs certain points for purchase. Customer can choose to buy them if he/she has adequate points.


The project deals with a simple database that can handle basic operations that are required in a pharmaceutical company. It involves report viewing, placing of orders, and dealing with purchases of gifts. Basic transactions have been set up for the same :

-Pharmacy Report:
It displays sales report of each branch,total transactions happened.Gives the purchase history of each branch.Displays medicines below threshold in each branch, and prints employee details of employees working in each branch.

-Branch Report:
It displays same contents as of pharmacy report but for a given branch id.
There are 4 branches in total.

-Customer details:
Personal details of that customer,history of his/her medicines they bought and displays gift purchases and points if he is a member. 

-Placing an Order:
Asks if you are an existing customer if yes,you can continue with your cid(customer ID) or else you can create one.
Transaction starts now:
Enter branch id and customer id and give the name of the medicine and it gives a list of all medicines available with the quantity present in that particular branch.Select the medicine and mention the quantity.The bill is calculated.

-Availing gifts:
You being a customer if you are a member, then each time you make a transaction points would be added to your customer id which you can redeem and get gifts like Thermometer,Weighing machine.

Implementation of the above functionalities have been done in python by importing **psycopg**.
Psycopg is the most popular PostgreSQL adapter for Python programming language.It is written in C and provides to efficiently perform the full range of SQL operations against Postgres database.





