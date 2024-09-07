import queries

logged_in = False
admin = False
userid = 0
fname = ""
lname = ""

in_class = False
current_class_id = 0
class_name = ""

def list_classes():
    print("\nClasses:")
    teacher_classes = queries.get_teachers_classes(userid)
    classes = queries.get_classes(userid)
    iterations = 0
    for i in teacher_classes:
        iterations += 1
        print(f"[{iterations}] {queries.get_class_name(i)} (Teacher)")
    for i in classes:
        iterations += 1
        print(f"[{iterations}] {queries.get_class_name(i)} (Student)")

#as you can see there are still a few remnants of the old flask version such as the directory system
dir = "/home"

while True:
    while logged_in == False:
        action = input("\nWhat would you like to do, (Type !help for options): ")

        match action:
            case "!help":
                print("\nOptions: sign-up, log-in")
            case "log-in":
                userid, logged_in, fname, lname = queries.log_in()
            case "sign-up":
                queries.sign_up()
            case _:
                print("\nThat wasn't on the list idiot!")

    while logged_in == True:
        print(f"\n--------------------------------------------------------------------------\n{fname} {lname} {dir}")     
        action = input("\nWhat would you like to do, (Type !help for options): ")

        #home
        if dir == "/home":
            match action:
                case "!help":
                    print("\nOptions: classes, create-question, back")
                case "back":
                    print("Cannot leave home directory")
                case "classes":
                    dir = "/home/classes"
                    list_classes()
                case "create-question":
                    queries.create_question()

        elif dir.startswith("/home/classes/class="):
            match action:
                case "!help":
                    print("Options: assign-quiz, banish-child, take-quiz, back")
                case "assign-quiz":
                    if queries.user_is_teacher(userid, current_class_id) == True:
                        queries.generate_quiz(current_class_id)
                    else:
                        print("Only the class teacher can assign quizzes")
                case "banish-child":
                    if queries.user_is_teacher(userid, current_class_id) == True:
                        queries.banish_child(current_class_id)
                    else:
                        print("Only the class teacher can assign quizzes") 
                case "take-quiz":
                    quizzes = queries.get_assigned_quizzes(current_class_id)
                    iterations = 0
                    for i in quizzes:
                        iterations += 1
                        print(f"[{iterations}] {queries.get_quiz_name(i)} Score: {queries.get_quiz_score(userid, i)}")
                    
                    quiz = quizzes[int(input("\nEnter the quiz number as seen above: "))-1]
                    queries.take_quiz(userid, quiz)
                case "back":
                    dir = "/home/classes"

        #classes
        elif dir == "/home/classes":

            match action:
                case "!help":
                    print("\nOptions: create-class, join-class, view-class, back")
                case "back":
                    dir = "/home"
                case "create-class":
                    queries.create_class(userid)
                case "join-class":
                    list_classes()
                    queries.join_class(userid)
                case "view-class":
                    list_classes()
                    class_name, current_class_id = queries.view_class(userid)
                    dir = f"/home/classes/class={class_name} class_id={current_class_id}"
                    quizzes = queries.get_assigned_quizzes(current_class_id)
                    iterations = 0
                    for i in quizzes:
                        iterations += 1
                        print(f"[{iterations}] {queries.get_quiz_name(i)} Score: {queries.get_quiz_score(userid, i)}")
                case "back":
                    dir = "/home"
