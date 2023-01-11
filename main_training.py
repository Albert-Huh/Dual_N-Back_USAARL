import pygame
from n_back_training import Session
import time
import os

def askSubjectInfo():
    subject_num = input("Subject Number: ")
    session_num = input("Session Number: ")
    age = input("Age: ")
    gender = input("Gender (M or F): ").upper()
    return subject_num, session_num, age, gender

def askLevel():
    level = int(input("Enter difficulty (0 [Low], 1 [Medium], 2 [High]): "))
    return level

def main():
    n = None
    while n == None:
            n_input = askLevel()
            if n_input in (0, 1, 2):
                n = n_input    
            else:
                print("Invalid input, please try again")

    info_flag = False
   
    while info_flag == False:
        is_int = 0
        subject_num, session_num, age, gender = askSubjectInfo()
        for i in [subject_num, session_num, age]:
            try:
                isinstance(int(i), int)
            except ValueError:
                is_int += 1
        if is_int > 0:
            print("Invalid inputs, please try again")
        else:
            if gender != "M" and gender != "F":
                print("Invalid gender input, please try again")
                info_flag = False
            else:
                info_flag = True
        
    datapath = os.path.join(os.getcwd(), "reports")
    # Check whether the specified path exists or not
    isExist = os.path.exists(datapath)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(datapath)

    datapath = os.path.join(os.getcwd(), "results")
    # Check whether the specified path exists or not
    isExist = os.path.exists(datapath)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(datapath)

    file_name = str(time.strftime("%Y%m%d_%H%M%S"))  + "_S" + subject_num + "_" + session_num + "_training"
    with open("reports/" + file_name + "_" + "_Report.txt", 'w') as report_file:
        with open("results/" + file_name + "_" + "_Result.txt", 'w') as result_file:
            pygame.init()
            session_time = time.time()
            report_file.write(file_name + "\n")
            report_file.write("Subject" + subject_num + "\n")
            report_file.write("Session" + session_num + "\n")
            report_file.write("Age: " + age + "\n")
            report_file.write("Gender: " + gender + "\n") 
            session = Session(2, report_file, result_file, n)
            session.run_session()
            print("Whole Session: " + str(time.time() - session_time))
            report_file.write("Whole Session: " + str(time.time() - session_time))

    # with open("reports/" + last.capitalize() + first.capitalize() + "_" + str(time.strftime("%Y%m%d_%H%M%S")) + "_Report.txt", 'w') as report_file:
    #     with open("results/" + last.capitalize() + first.capitalize() + "_" + str(time.strftime("%Y%m%d_%H%M%S")) + "_Result.txt", 'w') as result_file:
    #         pygame.init()
    #         session_time = time.time()
    #         session = Session(12, report_file, result_file, n)
    #         session.run_session()
    #         print("Whole Session: " + str(time.time() - session_time))
    #         report_file.write("Whole Session: " + str(time.time() - session_time))


if __name__ == "__main__" or __name__ == "main":
    main()