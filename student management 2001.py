
from email.mime import application
import re
import mysql.connector as db
from prettytable import PrettyTable
import os


class Student:
    def __init__(self):

        try:
            os.mkdir("Allfile")

        except:
            pass




        self.__adminid = 'admin'
        self.__adminpasswd = 'admin123'



        # create table for 
        mydb = db.connect(host = 'localhost', user = 'root' , passwd = 'rameshgupta', database = 'rupa12')
        cur = mydb.cursor()
        query = '''create table if not exists RegisterStudent(
        id int primary key auto_increment,
        Name varchar(100) not null,
        contact bigint not null,
        email varchar(100) unique not null,
        # fees bigint not null,
        password varchar(100));'''
        cur.execute(query)


        query = '''create table if not exists SApplication(
        id int primary key auto_increment,
        Name varchar(100) not null,
        Course varchar(100) not null,
        email varchar(100) unique not null, 
        Percentage int not null,
        Last_college_name varchar(100) not null,
        Application_status varchar(20));'''
        cur.execute(query) 


        query = '''create table if not exists Student(
            rollno int primary key auto_increment,
            Name varchar(100) not null,
            course varchar(100) not null,
            email varchar(100) unique not null,
            # fees bigint not null,

            academic_year varchar(100));'''
        cur.execute(query)


        mydb.close()



    def connection(self):
        self.mydb = db.connect(host = 'localhost', user = 'root' , passwd = 'rameshgupta', database = 'rupa12')
        self.cur = self.mydb.cursor()


#------------------------------------------------------------------Admin Section--------------------------------------------------------


    def AdminLogin(self,adminid,adminpasswd):
        if self.__adminid == adminid:
            if self.__adminpasswd == adminpasswd:
                
                return True
            else:
                return ' Invalid password '

                
        else:
            return ' Invalid Id ' 


    def addNewStudent(self,Sname,Scourse,Semail,Syear):
        try:
            self.connection()
            data=(Semail,)
            query='''select Name from student where email=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            #print(res)
            if res==None:
                
                data=(Sname,Scourse,Semail,Syear)
                query='''insert into student(Name,course,email,academic_year) values(%s,%s,%s,%s)'''
                self.cur.execute(query,data)
                return 'Student Added Successfully..'
            else:
                return f'This email is already enrolled with name {res[0]}'    

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()    

    def showPendingApplication(self):
        try:
            self.connection()
            query='''select * from sapplication;'''
            self.cur.execute(query)

            res=self.cur.fetchall()
            t = PrettyTable(['Application ID','Name', 'Course','Email', 'Pecentage' ,'Last college name' , 'Application_status'])
            no_of_pending_app=0
            for app in res:

                if app[6].lower()=='pending':
                    no_of_pending_app+=1

                    t.add_row([app[0],app[1] ,app[2],app[3],app[4],app[5],app[6]])

            
            
            #print(res)
            if no_of_pending_app==0:
                print('No Pending Applications as of Now\n')
                return True
            else:
                print(t)    

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()

    def addStudentFromPending(self,studentToAdd,AcademicYear):
        try:
            self.connection()
            data=(studentToAdd,)
            query='''select * from sapplication where id=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            # print(res)
            if res==None:
                return f'This Application Id doesn\'t exist'
            else:
                if res[6]=='confirmed':
                    return 'This Application Id is already Confirmed'
                else:
                    self.addNewStudent(res[1],res[2],res[3],AcademicYear)
                    self.connection()
                    data=(studentToAdd,)
                    query='''update sapplication set Application_status='confirmed' where id=%s; '''
                    self.cur.execute(query,data)
                    return 'Student  Enrolled Successfully..'
                    
        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()   

    def listStudent(self):
        try:
            self.connection()
            query='''select * from student;'''
            self.cur.execute(query)
            res=self.cur.fetchall()

            if res==None:
                print('No students are admitted at this moment..')
            else:
                students=PrettyTable(['Roll no','Name','Course','Email','Academic Year'])    
                for student in res:
                    students.add_row([student[0],student[1],student[2],student[3],student[4]])
                print(students) 
                print()   

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()     

    def delstudent(self,studentToDelete):    
        try:
            self.connection()

            data=(studentToDelete,)
            query='''select * from student where rollno=%s'''
            self.cur.execute(query,data)
            res=self.cur.fetchone()
            if res==None:
                return 'This Roll no doesn\'t Exist'

            else:
                query='''delete from student where rollno=%s;'''
                self.cur.execute(query,data)
                return True
        
        except Exception as e:
            return e
            
        finally: 
            self.cur.execute("commit;")
            self.mydb.close()


    def studentLogin1(self , contact , pass1):
        self.connection()
        data = (contact , pass1)
        query = '''select contact from RegisterStudent where contact = %s && password = %s;'''
        self.cur.execute(query , data)
        record = self.cur.fetchone()

        self.mydb.close()

        return record


    # def Checkfees(self,id):
    #     self.connection()
    #     query='''select fees from RegisterStudent where contact=%s;'''
    #     data=(id,)
    #     self.cur.execute(query,data)
    #     record=self.cur.fetchone()
    #     self.mydb.close()
    #     return record[0]



            


    # def Creditfees(self,contact,amm):
    #     prev=self.Checkfees(contact)
    #     curr=prev+amm
    #     self.connection()
    #     query='''update RegisterStudent set fees=%s where contact=%s;'''
    #     data=(curr,contact)
    #     self.cur.execute(query,data)
    #     self.cur.execute("commit;")
    #     return "Successfully updated"






#------------------------------------------------------------------Validation Functions--------------------------------------------------------



    def validateUsername(self,name):
        name_length = len(name)
        x = re.findall('[A-Za-z\s]+',name)
        
        if len(x[0]) == name_length:
            return True 
        else:
            return False




    #check valid contact no
    def validateContact(self,contact):
        contact=str(contact)
        ptr=r"[6-9]\d{9}" 
        x=re.findall(ptr,contact)
        if len(x) > 0:
            return True
        else:
            return False  


    #check valid email id
    def validateEmail(self,email):
        ptr=r"^[a-zA-Z0-9\.]+@[a-z]+\.[a-z]+" 
        x=re.findall(ptr,email)
        if len(x) > 0:
            return True
        else:
            return False   

#------------------------------------------------------------------Student Section--------------------------------------------------------

    #Register Student function
    def StudentRegister(self,name,contact,email,passwd,confirm_pass):
        self.userName_flag = self.validateUsername(name)
        if not self.userName_flag:
            return "Username is not valid try only with alphabets"
        
        self.userContact_flag = self.validateContact(contact)
        if not self.userContact_flag:
            return "Contact Number is not valid"

        
        self.userEmail_flag = self.validateEmail(email)
        if not self.userEmail_flag:
            return "Email Id is not valid" 
      
        if passwd == confirm_pass :
            self.password_flag = True
        else:
            return "Password MisMatch Plz try again"
        
        if self.userName_flag == True and self.userContact_flag == True and self.userEmail_flag == True and self.password_flag == True:
            self.connection()

            try:
                data = (name,contact,email,passwd)
                query = '''insert into  registerstudent(Name,contact,email,password) values(%s,%s,%s,%s);'''

                self.cur.execute(query,data)

                self.cur.execute("commit;")
                self.mydb.close()
            except Exception as e:
                print(e)
                self.mydb.close()
                return 'Email or contact Already Exists....'
            return f"Student {name} is Successfully Registered" 

    def StudentLogin(self,StudentId,StudentPwd): 
        try:
            self.connection()
            data=(StudentId,)
            query='''select password from registerstudent where email=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            # print(res)
            if res==None:
                return 'Email does not exist please register First..'
            elif res[0] == StudentPwd:      
                return True
            else:
                return 'Password is incorrect.'            

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()    

    def SubmitApplication(self,Name,Course,Email,Percentage,Last_college):
        try:
            self.connection()
            data=(Email,)
            query='''select Name from sapplication where email=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            #print(res)
            if res==None:
                
                data=(Name,Course,Email,Percentage,Last_college,"Pending")
                query='''insert into sapplication(Name,Course,email,Percentage,Last_college_name,Application_status) values(%s,%s,%s,%s,%s,%s)'''
                self.cur.execute(query,data)
                return 'Application submitted Successfully..'
            else:
                return f'This Email is already registered with name {res[0]}'    

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()    

    def ViewApplication(self,email):
        try:
            self.connection()
            data=(email,)
            query='''select * from sapplication where email=%s; '''
            self.cur.execute(query,data)

            res=self.cur.fetchone()
            #print(res)
            if res==None:
                return f'No application has been submitted for this {email}'
                
                
            else:
                return f'\nName:{res[1]}\nCourse:{res[2]}\nEmail:{res[3]}\nPecentage:{res[4]}\nLast college name:{res[5]}\nApplication_status:{res[6]}\n'
  

        except Exception as e:
            print(e)
        finally:
            self.cur.execute("commit;")
            self.mydb.close()    


            
#------------------------------------------------------------------application start from here--------------------------------------------------------


app=Student()

print("**************** STUDENT MANAGEMENT SYSTEM **************")

while True: 
    print('1-Admin login\n2-Student Corner\n3-Exit ')

    ch=int(input('Enter your Choice:')) 


    #choice @1admin
    if ch == 1:
        print("****************** Admin Login Section *************")

        adminId=input("Enter Admin Id:")
        adminPwd=input("Enter Admin Password:")

        LoginStatus=app.AdminLogin(adminId,adminPwd)

        if LoginStatus==True:
            print("************ Admin Login Succefull **************")

            #Admin choice
            while True:  
                print('1-Add Student\n2-Remove Student\n3-List Student\n4-Logout') 

                Adch=int(input('Enter your Choice:')) 

                if Adch == 1:
                    print("****************** Add Student Section ***************")
                    while True:
                        print('\n1-Enroll and Add new student\n2-Exit')
                        addStudentCh=int(input('Enter your choice:'))


                        # if addStudentCh ==1:
                        #     print("***************** Add Student From Submitted Applications ********************")
                        #     print()

                        #     pendingAppStatus=app.showPendingApplication()
                        #     if  pendingAppStatus!=True:
                        #         studentToAdd = input('Enter Application Id of student you want to add:')
                        #         Syear=input('Enter the academic year in format YYYY-YY:')
                        #         addStudentStatus=app.addStudentFromPending(studentToAdd,Syear)
                        #         if addStudentStatus == True:
                        #             print("************* Student Added Sucessfully ******************")
                        #         else:
                        #             print(f"***************** {addStudentStatus} **************")


                        if addStudentCh==1:
                            Sname=input('Enter Student Name:')
                            Scourse=input('Enter student Course:')
                            Semail=input('Enter Student Email:')
                            Syear=input('Enter the academic year in format YYYY-YY:')

                            addNewStudentStatus=app.addNewStudent(Sname,Scourse,Semail,Syear)

                            if addNewStudentStatus==True:
                                print("****************** Student Added Sucessfully ***************")
                            else:
                                print(f"*************** {addNewStudentStatus} ****************")


                        elif addStudentCh==2:
                            print("***************** Exiting Add student section **********************")
                            break
                        else:
                            print("****************** Invalid Choice *******************")










                elif Adch == 2:
                    print("************** Remove Student Section **************")

                    app.listStudent()
                    studentToDelete=int(input("Enter Roll no of student,You want to remove."))
                    DeleteStatus=app.delstudent(studentToDelete)
                    if DeleteStatus==True:
                        print("************* student Removed Successfully *******************")
                    else:
                        print(f"**************** {DeleteStatus} ******************")    



                    
                    




                elif Adch == 3:
                    print("**************** List Student Section ****************")
                    app.listStudent()

                    



                # elif Adch == 4:
                #     print(" ***************** view Pending Applications Section *************")
                #     app.showPendingApplication()

                    




                elif Adch == 4:
                    print("*************** Logged Out **************")
                    break


                else:
                    print("************** Invalid Choice *****************")


        else:
            print(f"*******************{LoginStatus} ********************")

            
                              

    #choice @2student section
    elif ch == 2:
        print(" *********** student Section ***************")

        #student Choice
        # while True:

        
        #     contact=input("Enter student Contact:")
        #     x1=app.validateContact(contact)
        #     if x1==True:
        #         break
        #     else:
        #         print("\n******** Contact Invalid *********\n")

        # pass1 = input("Enter Password :")
        # y = app.studentLogin1(contact , pass1)
        # if y == None:
        #     print("\n********** incorrect Details ************\n")
        # else:
        #     print("\n********* Successfully Login ********\n")


        

        while True:

            print('\n1 - Register student \n2 - School Events\n3 -courses fess list\n4-Student Login\n5-Exit') 

            stuch=input('Enter your Choice:') 
            
            #student Choice @1 Register Student
            if stuch == "1":
                    print("******************** Register Student Section ****************")

                    SName=input("Enter your name:")
                    SPhone=int(input("Enter your Phone no:"))

                    SEmail=input("Enter your Email:")
                    SPassword=input("Enter your Password :")
                    SCPassword=input("Confirm Password:")

                    regStatus=app.StudentRegister(SName,SPhone,SEmail,SPassword,SCPassword)

                    print(f"************* {regStatus} ****************")



                




            elif stuch == "2":
                print("\n************* School Events ******************\n")
                with open("Allfile\events12.txt","r") as file:
                    data = file.read()
                    #  file.close()

                    print(data) 



                    

            elif stuch == "3":

                print("\n****************  courses Fees List *****************\n")
                with open("Allfile\ess.txt","r") as file:
                    data = file.read()
                    #  file.close()

                    print(data) 


                    # print("******************** Register Student Section ****************")

                    # SName=input("Enter your name:")
                    # SPhone=int(input("Enter your Phone no:"))

                    # SEmail=input("Enter your Email:")
                    # SPassword=input("Enter your Password :")
                    # SCPassword=input("Confirm Password:")

                    # regStatus=app.StudentRegister(SName,SPhone,SEmail,SPassword,SCPassword)

                    # print(f"************* {regStatus} ****************")


                #     print("/n************** Credit fees amount ***********\n")



                #     amm=int(input("Enter  fees Amount To be Credited:"))
                #     x=app.Creditfees(contact,amm)
                #     print(f"\n****************{x}**************\n")


                # elif stuch=="3":
                #     print("\n************ Check  fees Balance ****************\n")
                #     balance=app.Checkfees(contact)
                #     print(f"\n********** Balance is :{balance} ****************\n")
                #     pass


                




                #student Choice @2 Student Login
            elif stuch == "4":
                print("************** Student Login **************")

                StudentId=input("Enter Student Id:")
                StudentPwd=input("Enter Student Password:")

                LoginStatus=app.StudentLogin(StudentId,StudentPwd)

                if LoginStatus==True:
                    print("***************** student Login Succefull  ***************")



                            #student choice After Login
                    while True:
                    
                        print('1-Submit Application\n2-View Applications status\n3-Logout') 
                        log_st_ch=int(input('Enter your Choice:'))  
                        if log_st_ch == 1:
                            print("***************** Submit Application Section ***************")
                            Name=input("Enter your name:")
                                
                            Course=input("Enter your Course Appying for:")
                            Email=input("Enter your Email:")
                            Percentage=int(input("Enter your Percentage:"))
                            Last_college=input("Enter your Last Attended College Name:")

                            Submit_Status=app.SubmitApplication(Name,Course,Email,Percentage,Last_college)

                            if Submit_Status==True:
                                print("******************** Application Submited Successfully..******************")

                            else:
                                print(f"**************** {Submit_Status} ******************")    












                        elif log_st_ch == 2:
                            print("**************** Applications status *****************")
                            email=input("Enter your Email filled in application form :")
                            viewStatus=app.ViewApplication(email)

                            print(f"************** {viewStatus} ****************")



                        elif log_st_ch == 3:
                            print("************** logout ****************") 
                            break

                        else :
                            print("**************** Invalid choice *****************")        

                else:
                    print(f"***************** {LoginStatus} ******************")        


                            
                            



                    #student Choice @3 Exit
            elif stuch == "5":
                print("******************** Exiting Student Section *****************")
                break

                    #student Choice @ Invalid option
            else:
                print("****************** Invalid Choice ****************")

                
        #Choice @3-Exit
    elif ch == 3:
        print("****************** Exiting Application *****************")
        break

            
        #Choice @Invlid choice    
    else:
        print("******************* Invalid Choice ********************")
            
            
