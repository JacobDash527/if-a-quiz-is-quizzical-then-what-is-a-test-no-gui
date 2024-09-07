import sqlite3
import time
import hashlib
import random
from time import time

#connect to db
db = sqlite3.connect("database.db")
db.row_factory = sqlite3.Row
query = db.cursor()

def log_in():
    email_addr = input("\nEmail address: ")
    password = input("\nPassword: ")

    pass_hash = hashlib.md5(password.encode("utf-8")).hexdigest()

    sql = f"""
            SELECT user_id, pass_hash, fname, lname
            FROM user
            WHERE email_address = "{email_addr}";
            """
                    
    for row in query.execute(sql):
        results = [row['user_id'], row['pass_hash'], row['fname'], row['lname']]

    if pass_hash == results[1]:
        print("\nLogin successful!")
        return results[0], True, results[2], results[3]
    else:
        print("\nEmail address or password incorrect, try again lil bro")

def sign_up():
    email_addr = input("\nEmail address: ")
    password = input("\nPassword: ")

    fname = input("\nFirst name: ")
    lname = input("\nLast name: ")

    pass_hash = hashlib.md5(password.encode("utf-8")).hexdigest()

    sql = f"""
            INSERT INTO user(email_address, pass_hash, teacher, fname, lname)
            VALUES("{email_addr}", "{pass_hash}", 0, "{fname}", "{lname}");
            """
                
    query.execute(sql)
    db.commit()

def create_class(userid):
    class_name = input("\nEnter class name: ")

    sql = f"""
            INSERT INTO classes(teacher, class_name)
            VALUES({userid}, "{class_name}")
            """
    query.execute(sql)
    db.commit()

    print("Class created successfully")

def join_class(userid):
    class_id = input("\nWhat is the class id, your teacher should have it: ")

    sql = f"""
            INSERT INTO usersclasses(user_id, class_id)
            VALUES({userid}, {class_id})
            """
    
    query.execute(sql)
    db.commit()

    print("Class joined successfully")

def view_class(userid):
    chosen_class = int(input("\nEnter the number corresponding to a class as seen above: "))
    classes = get_teachers_classes(userid) + get_classes(userid)
    return get_class_name(classes[chosen_class-1]), classes[chosen_class-1]

def get_classes(userid):
    classes = []
    sql = f"""
            SELECT class_id
            FROM usersclasses
            WHERE user_id = {userid}
            """
    
    for row in query.execute(sql):
        classes.append(row[0])
    
    return classes

def get_teachers_classes(userid):
    classes = []
    sql = f"""
            SELECT class_id
            FROM classes
            WHERE teacher = {userid} 
            """
    
    for row in query.execute(sql):
        classes.append(row[0])
    
    return classes

def get_class_name(class_id):
    sql = f"""
            SELECT class_name
            FROM classes
            WHERE class_id = {class_id}
            """
    
    for row in query.execute(sql):
        class_name = row['class_name']
    
    return class_name

def create_question():
    iterations = 0
    for subject in get_subjects():
        iterations += 1
        print(f"[{iterations}] {subject}")

    subject = input("\nPlease enter the correct subject according to the number above: ")
    question = input("\nPlease provide a worded question: ")
    correct_answer = input("\nPlease provide the correct answer: ")
    a_1 = input("Please provide incorrect answer 1: ")
    a_2 = input("Please provide incorrect answer 2: ")
    a_3 = input("Please provide incorrect answer 3: ")

    sql = f"""
            INSERT INTO questions(subject, a_correct, a_1, a_2, a_3, question )
            VALUES({subject}, "{correct_answer}", "{a_1}", "{a_2}", "{a_3}", "{question}")
            """
    
    query.execute(sql)
    db.commit()

def user_is_teacher(userid, classid):
    sql = f"""
            SELECT *
            FROM classes
            WHERE teacher = {userid}
            AND class_id = {classid}
            """

    for row in query.execute(sql):
        if row['teacher'] == userid:
            return True

def banish_child(class_id):
    students = get_students(class_id)
    iterations = 0
    for i in students:
        iterations += 1
        print(f"[{iterations}] {get_user_name(i)}")

    child = int(input("\nEnter the number corresponding to the student you would like to remove: "))

    sql = f"""
            DELETE FROM usersclasses
            WHERE class_id = {class_id}
            AND user_id = {students[child-1]}
            """
    print(f"\n{get_user_name(students[child-1])} has been successfuly banished. BE GONE IMBECILE!")
    query.execute(sql)
    db.commit()

def generate_quiz(class_id):
    quiz_name = input("Enter a name for the quiz: ")
    quiz_length = int(input("How many questions should the quiz be?: "))
    time_allowed = input("How much time is allowed for the quiz? (Seconds):")
    iterations = 0
    for subject in get_subjects():
        iterations += 1
        print(f"[{iterations}] {subject}")
    subject_id = input("Please select a subject from the list above: ")

    questions = []

    sql = f"""
            INSERT INTO quizzes(class_id, quiz_name, time_allowed)
            VALUES({class_id}, "{quiz_name}", {time_allowed})
            """
    query.execute(sql)
    db.commit()

    quiz_id = query.lastrowid
 
    for i in range(0, quiz_length):
        valid_question = False
        while valid_question == False:
            sql = f"""
                    SELECT question_id
                    FROM questions
                    WHERE subject = {subject_id}
                    ORDER BY RANDOM()
                    LIMIT 1
                    """
            
            for row in query.execute(sql):
                question_id = row["question_id"]
            
            if question_id in questions:
                pass
            else:
                questions.append(question_id)
                valid_question = True

    for question in questions:
        sql = f"""
                INSERT INTO quizzesquestions(quiz_id, question_id)
                VALUES({quiz_id}, {question})
                """
        query.execute(sql)
        db.commit()

def get_subjects():
    subjects = []
    sql = f"""
            SELECT subject_name
            FROM subjects
            """
    
    for row in query.execute(sql):
        subjects.append(row["subject_name"])
    
    return subjects

def get_students(class_id):
    students = []

    sql = f"""
            SELECT user_id
            FROM usersclasses
            WHERE class_id = {class_id}
            """
    
    for row in query.execute(sql):
        students.append(row["user_id"])
    
    return students

def get_user_name(user_id):
    name = ""
    sql = f"""
            SELECT fname, lname
            FROM user
            WHERE user_id = {user_id}
            """
    
    for row in query.execute(sql):
        name = f"{row['fname']} {row['lname']}"
    
    return name

def get_assigned_quizzes(current_class_id):
    quizzes = []
    sql = f"""
            SELECT quiz_id
            FROM quizzes
            WHERE class_id = {current_class_id}
            """
    
    for row in query.execute(sql):
        quizzes.append(row["quiz_id"])
    
    return quizzes

def get_quiz_name(quiz_id):
    sql = f"""
            SELECT quiz_name
            FROM quizzes
            WHERE quiz_id = {quiz_id}
            """

    for row in query.execute(sql):
        name = row["quiz_name"]
    
    return name

def get_quiz_score(user_id, quiz_id):
    score = 0
    sql = f"""
            SELECT score
            FROM userquizzes
            WHERE user_id = {user_id}
            AND quiz_id = {quiz_id}
            """
    
    for row in query.execute(sql):
        score = row["score"]
        
    return score

def take_quiz(user_id, quiz_id):
    answers = []
    questions = []
    score = 0
    exists = False
    start_time = int(time())
    over_time = False
    time_limit = 0
    answered = 0

    sql = f"""
            SELECT time_allowed
            FROM quizzes
            WHERE quiz_id = {quiz_id}
            """

    for row in query.execute(sql):
        time_limit = row["time_allowed"]
    print(f"Time: {time_limit}")

    sql = f"""
            SELECT *
            FROM userquizzes
            WHERE user_id = {user_id}
            AND quiz_id = {quiz_id}
            """
    
    for row in query.execute(sql):
        exists = True

    if exists == False:
        sql = f"""
                INSERT INTO userquizzes(quiz_id, user_id)
                VALUES({quiz_id}, {user_id})
                """
        query.execute(sql)
        db.commit()

    sql = f"""
            SELECT question_id
            FROM quizzesquestions
            WHERE quiz_id = {quiz_id}
            """
    
    for row in query.execute(sql):
        questions.append(row["question_id"])
    
    for question in questions:
        sql = f"""
                SELECT question, a_correct, a_1, a_2, a_3
                FROM questions
                WHERE question_id = {question}
                """
        
        for row in query.execute(sql):
            iterations = 0
            if over_time == False:
                iterations += 1
                options = [row["a_correct"], row["a_1"], row["a_2"], row["a_3"]]
                random.shuffle(options)

                print(f"\nQuestion ({iterations}/{len(questions)}): {row["question"]}\n[1] {options[0]}\n[2] {options[1]}\n[3] {options[2]}\n[4] {options[3]}\nTime left: {int(time_limit-(time()- start_time))} seconds")
                answer = input("Please enter the number corresponding to your answer as seen above: ")
                answers.append(options[int(answer)-1])
                if (int(time()) - start_time) >= time_limit:
                    over_time = True
                answered += 1
        
    for i in range(0, answered):
        sql = f"""
            SELECT question, a_correct, a_1, a_2, a_3
            FROM questions
            WHERE question_id = {questions[i]}
            """
        
        for row in query.execute(sql):
            print(f"\nQuestion: {row["question"]}\nYour answer: {answers[i]}\nCorrect answer: {row["a_correct"]}")
            if answers[i] == row["a_correct"]:
                score += 1
        
    score_str = f"{score}/{len(questions)}"
    print(f"\nYour final score is {score}/{len(questions)}")

    sql = f"""
            UPDATE userquizzes
            SET score = "{score_str}"
            WHERE quiz_id = {quiz_id}
            AND user_id = {user_id}
            """
    
    query.execute(sql)
    db.commit()