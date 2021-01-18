import psycopg2

def branch_report(branch):
    #sales

    print("-------------------------------------------------------------------------------BRANCH REPORT----------------------------------------------------------------------------------------")
    print("\n")
    print("SALES REPORT OF THE BRANCH")
    query = "select bid, total_sales from branch natural join (select bid, sum(amount) as total_sales from sales group by bid) as newTable where bid = %s;"
    cursor.execute(query, (branch,))
    record = cursor.fetchall()
    try:
        #print("\n")
        print("Total sales: ", record[0][1])
    except:
        print("Total sales:  None")
    
    # Employees
    query = "select ssn, ename from branch natural join works natural join employee where bid =%s;"
    cursor.execute(query, (branch,))
    record = cursor.fetchall()
    print("\n")
    print("EMPLOYEES OF THE BRANCH: ")
    #print("\n")
    print("(ssn, ename)")
    for i in record:
        print(i)
    
    # Medincines below threshold
    print("\n")
    print("MEDICINES BELOW THRESHOLD")
    threshold = 50
    query = "select mid, mname from ((select mid from medicines) except (select mid from stock where quantity > %s and bid =%s))as t1 natural join medicines;"
    cursor.execute(query, (threshold, branch))
    record = cursor.fetchall()
    #print("\n")
    print("(mid, mname)")
    for i in record:
        print(i)
    print("\n")
    
def pharmacy_report():
    # Sales of each branch
    print("-------------------------------------------------------------------------------PHARMACY REPORT----------------------------------------------------------------------------------------")
    print("\n")
    print("SALES REPORT OF EACH BRANCH")
    query = "select branch.bid, bname, total_sales from branch natural join (select bid, sum(amount) as total_sales from sales group by bid) as newTable;"
    cursor.execute(query)
    record = cursor.fetchall()
    for i in record:
        print(i)
    print("\n")

    # No of customers who bought from the different branches
    print("\n")
    print("PURCHASE HISTORY OF CUSTOMERS:")
    print("(bid, No of customers)")
    query = "select bid, total_customers from branch natural join (select bid, count(cid) as total_customers from sales group by bid) as newable natural join customer;"
    cursor.execute(query)
    record = cursor.fetchall()
    for i in record:
        print(i)

    # Medicines in each branch that are below the threshold
    print("\n")
    print("MEDICINES BELOW THRESHOLD ")
    threshold = 50
    query = "select bid, bname, mid, mname from ((select bid, mid from branch, medicines) except (select bid, mid from stock where quantity > %s))as t1 natural join branch natural join medicines order by bid;"
    cursor.execute(query, (threshold,))
    record = cursor.fetchall()
    print("(branchID, bName, medicineID, medicine_name)")
    for i in record:
        print(i)    

    # Employee details per branch
    print("\n")
    print("EMPLOYEE DETAILS :")
    query = "select bid, bname, ssn, ename from branch natural join works natural join employee order by bid;"
    cursor.execute(query, (threshold,))
    record = cursor.fetchall()
    print("(branchID, bName, ssn, Ename)")
    for i in record:
        print(i) 
    print("\n")   
    
def customer_details(cid):
    print("-------------------------------------------------------------------------------CUSTOMER DETAILS----------------------------------------------------------------------------------------")
    # Customer personal details
    print("\n")
    print("PERSONAL DETAILS")
    query = "select * from customer where cid = %s"
    cursor.execute(query, (cid,))
    record = cursor.fetchall()
    for i in record:
        print(i)
    # Customer history of orders, as in medicines bought and quantity
    print("\n")
    print("HISTORY of medicines bought and quantity")
    print("Order_no, Medicine_id, Medicine_name, Quantity, Cost")
    query ="select ono, mid, mname, quantity, cost from sales natural join orders natural join medicines natural join customer where cid =%s"
    cursor.execute(query, (cid,))
    record = cursor.fetchall()
    for i in record:
        print(i)
     
    # Customer gifts purchase
    print("\n")
    print("GIFT PURCHASES")
    query = "select gid, gname from customer natural join sold_gifts natural join gift where cid =  %s "
    cursor.execute(query, (cid,))
    record = cursor.fetchall()
    for i in record:
        print(i)
    print("\n")
    print("POINTS")
    query="select points from members natural join customer where cid=%s"
    cursor.execute(query, (cid,))
    record = cursor.fetchall()
    for i in record:
        print(i)
    print("\n")
    

def new_customer():
    
    query = "select count(cid) from customer"
    cursor.execute(query)
    record=cursor.fetchone()
    name= input("HELLO WELCOME!\n Enter your name ")
    ph_no=int(input("Enter you phone number "))
    membership=input("Would you like to be a member? ")
    query ="insert into customer values ((select count(cid) from customer) +5001, %s, %s, %s);"
    try:
        cursor.execute(query, (name, ph_no, membership))
        if (membership):
            query= "insert into members values((select count(cid)+5000 from customer), 0);"
            cursor.execute(query)
    except:
        print("Please provide valid details");
        new_customer();
    finally:
        query = "select max(cid) from customer"
        cursor.execute(query)
        cid=cursor.fetchone()
        print("Your customer id is ", cid)
    

def availability_medicines(bid):
    a = input("Enter medicine required: ")
    query="select stock.mid, mname, expdate, quantity, price from medicines, stock where medicines.mid= stock.mid and position (%s in mname) >0 and quantity >0 and bid= %s;"
    cursor.execute(query,(a, bid))
    record = cursor.fetchall()
    return record
        
def order_placing(cid, bid): 
    con1 = psycopg2.connect(user = "postgres",password = "ruchi@77",host = "localhost",port = "5432", database = "pharmacy")
    con1.autocommit=False
    cur = con1.cursor()
    query="insert into sales values((select count(ono) from sales) +1, %s, %s, 0);"
    cur.execute(query, (bid, cid))
    query = "select * from sales;"
    cur.execute(query)
    record=cur.fetchall();
    cont=1;
    while(cont):
        try:
            available = availability_medicines(bid)
            a=-1
            i=-1
            while(a==-1):
                
                print('(mid, mname, expdate, quantity, price)')
                for i in range (0,len(available)):
                    print(i+1, available[i])    
                print("\n")      
                a =int(input("Which medicine do you need? Enter 0 you don't want any of these medicines: "))
                if(a > i+1 or a<0):
                    print("Enter valid option")
                    a=-1
            if(a>0):
                print("\n")
                b= int(input("Enter the quantity required"))
                if(b<=0):
                    print("Item was not ordered as the quantity provided was not appropriate")
                else:
                    query = "select prescription_required from medicines where mid = %s;"
                    cur.execute(query, (available[a-1][0],))
                    res= cur.fetchall()
                    approve=True
                    approval=1
                    if(res[0][0]):
                        query = "select orders.approved from orders natural join sales where cid= %s and mid = %s"
                        cur.execute(query, (cid, available[a-1][0]))
                        res1 = cur.fetchall()
                        try:
                            if (res1[0][0]==False):
                                approval=int(input("Has precsription been submitted?"))
                            if (approval!=1):
                                approve=False
                        except:
                            approval=int(input("Has precsription been submitted?"))
                            if (approval!=1):
                                approve=False
                    query= "insert into orders values((select count(ono) from sales), %s, %s, %s, %s*%s*(select price from medicines where mid=%s));"
                    cur.execute(query, (available[a-1][0], approve, b*approval, b,approval,available[a-1][0]))
            print("\n")
            cont = int(input("Do you want to order more medicines?"))
            if (cont ==0):

                        query ="update sales set amount = (select sum(cost) from orders where ono =(select count(ono) from sales)) where ono =(select count(ono) from sales);"
                        cur.execute(query)
                        
                        query ="select * from orders where ono = (select count(ono) from sales);"
                        cur.execute(query)
                        res2 = cur.fetchall()
                        for i in res2:
                            print (i)
                        query = "select amount from sales where ono = (select max(ono) from sales);"
                        cur.execute(query)
                        res3 = cur.fetchone()
                        if(res3[0]==None):
                            query="drop rule del_protect on sales;"
                            cur.execute(query)
                            query="delete from sales where ono=(select count(ono) from sales);"
                            cur.execute(query)
                            query="CREATE RULE del_protect AS ON DELETE TO sales DO INSTEAD NOTHING;"
                            cur.execute(query)
                        print("\n")
                        print("Total Amount: ", res3[0])
                        con1.commit()
                        
        except(Exception, psycopg2.DatabaseError) as error :
            print ("Error in transction Reverting all other operations of the transction ", error)
            con1.rollback()
            break
    print("\n")


def buy_gift(cid):
    con2 = psycopg2.connect(user = "postgres",password = "ruchi@77",host = "localhost",port = "5432", database = "pharmacy")
    con2.autocommit=False
    cur2 = con2.cursor()
    try:
        query = "select count(cid) from members where cid=%s;"
        cur2.execute(query, (cid,))
        res=cur2.fetchall()
        if(res[0][0] !=0):
            query = "select * from gift where points <= (select points from members where cid = %s);"
            cur2.execute(query, (cid,))
            res=cur2.fetchall()
            if(res==[]):
                print("SORRY! You don't have enough points to buy any gifts")
            else:
                i=-1
                for i in range (0,len(res)):
                    print(i+1, res[i])
                choice=int(input("Which gift do you want?"))
                if (choice > i+1 or choice <=0):
                    print("Invalid option, try again")
                else:
                    query = "insert into sold_gifts values (%s, %s)"
                    cur2.execute(query, (res[choice-1][0],cid))
                    print("Congratulations! You have availed the gift!")
        else:
            print("You're not a member, SORRY! You can not avail gifts")
        con2.commit()
    except(Exception, psycopg2.DatabaseError) as error :
            print ("Error in transction Reverting all other operations of the transction ", error)
            con2.rollback()   
    print("\n") 

def connected():
    print("Welcome!")
    while(True):
        print("Enter;")
        print("1 to view the pharmacy report")
        print("2 to view branch report")
        print("3 to view customer details")
        print("4 to place an order")
        print("5 to avail gifts")
        print("any other key to exit")
        choices=int(input())
        if(choices==1):
            pharmacy_report()
        elif(choices==2):
            print("\n")
            branch=int(input("ENTER branch no.: "))
            branch_report(branch)
        elif(choices==3):
            print("\n")
            customer=int(input("ENTER customer id: "))
            customer_details(customer)
        elif(choices==4):
            print("\n")
            ec=int(input("Are you an existing customer of this pharmacy? "))
            if(ec==0):
                new_customer()
            print("\n")
            branch=int(input("ENTER branch no.: "))
            customer=int(input("ENTER customer id: "))
            order_placing(customer,branch)
        elif(choices==5):
            print("\n")
            customer=int(input("ENTER customer id: "))
            buy_gift(customer)
        else:
            break

connection = None
cursor =None

try:
    connection = psycopg2.connect(user = "postgres",password = "ruchi@77",host = "localhost",port = "5432", database = "pharmacy")
    cursor = connection.cursor()
    connected()

except Exception as e:
    print("Exception is:",str(e))
finally:
    if (connection):
        connection.commit()
        connection.close()
        print("Connection closed")
