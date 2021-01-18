create database pharamcy;

-- add not null constraints to the appropriate columns 
-- on delete and update cascades to be done
-- check constraint
-- cost should be float in orders

create table branch (bid int, bname varchar (20), baddress varchar (50) , primary key (bid) );
create table employee (ssn int, ename varchar (20), eaddress varchar (50) , eph_no char(10), constraint valid_no check (eph_no not like '%[^0-9]%'), primary key (ssn));
create table works (bid int , ssn int, foreign key (bid) references branch, foreign key (ssn) references employee, primary key (ssn));
create table customer (cid int,  cname varchar (20), cph_no char(10), ismember boolean, constraint valid_no check (cph_no not like '%[^0-9]%'), primary key (cid));
create table members (cid int, points int, foreign key (cid) references customer, primary key (cid));
create table medicines (mid int, mname varchar(20), price float, expdate date, prescription_required boolean, primary key (mid));
create table stock (bid int, mid int, quantity int, foreign key (bid) references branch, foreign key (mid) references medicines, primary key (bid, mid));
create table gift (gid int, gname varchar(20), quantity int, points int, primary key (gid));
create table sales (ono int, bid int, cid int, amount int, foreign key (bid) references branch, primary key (ono), foreign key (cid) references customer, primary key (ono));
create table orders (ono int, mid int, approved boolean, quantity int, cost int, primary key (ono, mid), foreign key (mid) references medicines, foreign key (ono) references sales);

-- to enter values 

create table sold_gifts (gid int, cid int, primary key (gid, cid), foreign key (gid) references gift, foreign key (cid) references customer);



insert into branch values (0001, 'Malleshwaram', '8th Main, Malleshwaram, Bangalore 560055');
insert into branch values (0002, 'Banashankari', '100 Feet Ring Road, Banashankari, Bangalore 560085');
insert into branch values (0003, 'Sadashivanagar','Sankey Rd, Bhashyam Circle, Bangalore 560063');
insert into branch values (0004, 'Yelahanka','Kattigenahalli, Yelahanka, Bangalore 560064');

insert into employee values (1001, 'Sarala','Kattigenahalli, Yelahanka, Bangalore 560064',9834921926);
insert into employee values (1002, 'Anees','Malleshwaram, 15th Cross, Bangalore 560055',9822973920);
insert into employee values (1003, 'Mahesh','80 Feet Rd, Sanjaynagar, Bengaluru 560094',9603990130);
insert into employee values (1004, 'Babu','Malleshwaram, 17th Cross, Bangalore 560055',9982630132);
insert into employee values (1005, 'Rajesh','Outer Ring Road, Banashankari, Bangalore 560085',9873920910);
insert into employee values (1006, 'Vimal','100 ft Ring Road, Banashankari, Bangalore 560085',9820301123);
insert into employee values (1007, 'Rajalakshmi','Sankey Rd, near Bhashyam Circle, Bangalore 560063',9843301923);
insert into employee values (1008, 'Anita','Kattigenahalli, Yelahanka, Bangalore 560064',9645920183);

insert into works values (0001, 1002);
insert into works values (0001, 1004);
insert into works values (0002, 1005);
insert into works values (0002, 1006);
insert into works values (0003, 1003);
insert into works values (0003, 1007);
insert into works values (0004, 1001);
insert into works values (0004, 1008);

insert into medicines values (2001, 'Crocin 650 mg', 30.24, '2022/09/01', False);
insert into medicines values (2002, 'Domstal 10 mg', 26.35, '2021/06/01', False);
insert into medicines values (2003, 'Fludac 20 mg', 50.00, '2021/11/01', True);

insert into stock values (0001, 2001, 300);
insert into stock values (0002, 2001, 150);
insert into stock values (0003, 2001, 50);
insert into stock values (0004, 2001, 174);
insert into stock values (0001, 2002, 152);
insert into stock values (0002, 2002, 98);
insert into stock values (0004, 2002, 100);
insert into stock values (0001, 2003, 56);
insert into stock values (0003, 2003, 49);
insert into stock values (0004, 2003, 28);

insert into gift values (3001, 'Weighing Machine', 30, 1000);
insert into gift values (3002, 'Thermometer',40, 600);