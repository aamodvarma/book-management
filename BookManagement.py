import mysql.connector
from getpass import getpass

def OrderProduct(mydb, mycursor, user):
    ItemDetails(mycursor,user)
    id = int(input("Enter the ID of the book you want to order:"))
    ItemDetails(mycursor,user,id)
    mycursor.execute(f"update product set newowner='{user}'  where id={id}")
    mydb.commit()
    print("The above book has been ordered")


def CancelOrder(mydb,mycursor,user):
    sql=f"select * from product where newowner={user}"
    mycursor.execute(sql)
    b = mycursor.fetchall()
    for a in b:
        if not a[5] :
            print(f"\nID(id): {a[0]}\nBook Name(name): {a[1]}\nAuthor Name(author): {a[2]}\nCost(cost): {a[3]}\n")
    print("These are the books you've previously ordered")
    id = int(input("Enter the ID of the book you want to cancel:"))
    mycursor.execute(f"update product set newowner='{user}'  where id={id}")
    mydb.commit()
    print("The order has been canceled")



def AddProduct(mydb, mycursor, user):
    try:
        sql="create table product ( id int unique, name varchar(20) , author varchar(20) , cost int, owner varchar(20), newowner varchar(20) default null  );"
        mycursor.execute(sql)
    except:
        pass
    name=input("Enter the Book Name : ")
    author=input("Enter the Author Name : ")
    cost=int(input("Enter the cost:"))
    sql=f'Insert into product(name, author,  cost, owner) values ("{name}","{author}",{cost}, "{user}")'
    mycursor.execute(sql)
    mydb.commit()
    
def EditProduct(mydb, mycursor, user):

    ItemDetails(mycursor,user)
    id=int(input("Enter product ID to be edited : "))
    sql=f"select * from product where id={id}"
    mycursor.execute(sql)

    a=mycursor.fetchone()

    if a[4] != user:
        print("You are not authorized to edit this book")
        return;

    ItemDetails(mycursor,user,id)
    print("")
    fld=input("Enter the field which you want to edit : ")
    val=input("Enter the value you want to set : ")
    sql=f"Update product set {fld}='{val}' where id={id}"
    mycursor.execute(sql)
    print("Editing Done")
    print("After correction the record is : ")
    ItemDetails(mycursor,user,id)
    mydb.commit()
    
def DelProduct(mydb, mycursor, user):

    ItemDetails(mycursor,user)
    id=int(input("Enter product ID to be deleted : "))
    sql=f"select * from product where id={id}"
    mycursor.execute(sql)
    a=mycursor.fetchone()

    if a[4] != user:
        print("You are not authorized to delete this book")
        return;
    sql=f"delete from product where id={id}"
    mycursor.execute(sql)
    mydb.commit()
    print("Item Deleted")

def ItemDetails(mycursor, user, id=0):
    if  id==0:
        sql=f"select * from product"
    else:
        sql=f"select * from product where id={id}"
    mycursor.execute(sql)
    b = mycursor.fetchall()
    for a in b:
        if not a[5] :
            print(f"\nID(id): {a[0]}\nBook Name(name): {a[1]}\nAuthor Name(author): {a[2]}\nCost(cost): {a[3]}\n")
    
    
def SearchBook(mycursor, user):
    name=(input("Enter the name of book you want to search:"))
    sql=f'select * from product where name like "%{name}%"'
    mycursor.execute(sql)
    a = mycursor.fetchall()
    for b in a:
        print(f"\nID: {b[0]}\nBook Name: {b[1]}\nAuthor Name: {b[2]}\nCost: {b[3]}\n")
    

def MenuSet(user):
    mydb=mysql.connector.connect(host="localhost",user="root",password="192005",database="book")
    mycursor=mydb.cursor()

    print("1. Add Book ")
    print("2. Edit Book ")
    print("3. Delete Book ")
    print("4. Order Book ")
    print("5. View Book Details")
    print("6. Search book")
    print("7. Exit")
    
    userInput = int(input("Please Select An Above Option: "))
    if(userInput == 1):
        AddProduct(mydb, mycursor,user)
    elif(userInput == 2):
        EditProduct(mydb, mycursor,user)
    elif (userInput==3):
        DelProduct(mydb, mycursor,user)
    elif (userInput==4):
        OrderProduct(mydb,mycursor,user)
    elif (userInput==5):
        ItemDetails(mycursor,user)
    elif (userInput==6):
        SearchBook(mycursor,user)


    elif (userInput==7):
        return None;
    else:
        print("Enter a choice:")
    MenuSet(user)

        

def SignUp(mydb, mycursor):
    try:
        sql="create table users ( username varchar(20) , password varchar(20) , email varchar(30), phone int(20));"
        mycursor.execute(sql)
    except:
        pass;
    username=input("Enter the username: ")
    password = getpass()

    email=(input("Enter the email:"))
    phone = int(input("Enter your phome:"))
    sql=f'Insert into users values("{username}","{password}","{email}","{phone}")'
    mycursor.execute(sql)
    mydb.commit()

    print("Account Created")
def SignIn(mycursor):
    username = (input("Enter the username:"))
    password = getpass()
    sql=f"select password from users where username='{username}'"
    mycursor.execute(sql)
    a = mycursor.fetchone()[0]
    if password == a:
        print("Signed in")
        MenuSet(username)
    else:
        print("Wrong password")

def DeleteAccount(mydb,mycursor):
    username = (input("Enter the username:"))
    password = getpass()
    sql=f"select password from users where username='{username}'"
    mycursor.execute(sql)

    a = mycursor.fetchone()[0]
    if password == a:
        sql=f"delete from users where username='{username}'"
        mycursor.execute(sql)
        mydb.commit()
        print("Account Deleted")



    else:
        print("Wrong password")



def UserSet():
    mydb=mysql.connector.connect(host="localhost",user="root",password="192005",database="book")
    mycursor=mydb.cursor()

    print("1. Sign Up")
    print("2. Sign In")
    print("3. Delete Account")
    print("4. Exit")
    
    userInput = int(input("Please Select An Above Option: "))
    if(userInput == 1):
        SignUp(mydb, mycursor)
    elif(userInput == 2):
        SignIn( mycursor)
    elif (userInput==3):
        DeleteAccount(mydb,mycursor);
    elif userInput==4:
        pass
    else:
        print("Enter a choice:")
    UserSet()

            
UserSet()


    

