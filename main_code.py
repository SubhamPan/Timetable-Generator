import pandas as pd

class Slot:

    # map<char, int> day_to_number
    DAY_ORDER = {
        'M' : 1,
        'T' : 2,
        'W' : 3,
        'Th' : 4,
        'F' : 5,
        'Sa' : 6
    }

    def __init__(self, day, period, section_type):
        self.day = day
        self.period = period
        self.section_type = section_type

    def __hash__(self):
        return hash((self.day, self.period))
    
    def __eq__(self, other):
        return self.day == other.day and self.period == other.period
    
    def __lt__(self, other):
        if self.DAY_ORDER[self.day] != self.DAY_ORDER[other.day]:
            return self.DAY_ORDER[self.day] < self.DAY_ORDER[other.day]
        return self.period < other.period

    
    def __repr__(self):
        return f"Slot(day = {self.day}, period = {self.period}, section type = {self.section_type})"
    

class Combo:
    def __init__(self, lec_slots, tut_slots, prac_slots):
        self.slots = []
        self.slots.extend(lec_slots)
        self.slots.extend(tut_slots)
        self.slots.extend(prac_slots)

    def __repr__(self):
        return f"Combo(slots = {self.slots})"    


# #degbugging version of Combo
# class Combo:
#     def __init__(self, lec_slots, tut_slots, prac_slots):
#         print(f"\n\n Combo Constructor called. \n\n")
#         self.slots = []
#         print(f"Adding lecture slots: {lec_slots}")
#         self.slots.extend(lec_slots)
#         print(f"Adding tutorial slots: {tut_slots}")
#         self.slots.extend(tut_slots)
#         print(f"Adding practical slots: {prac_slots}")
#         self.slots.extend(prac_slots)
    
#     def __repr__(self):
#         slots_repr = ', '.join(repr(slot) for slot in self.slots)
#         return f"Combo(slots = [{slots_repr}])"



class Course:
    def __init__(self, course_id):
        self.course_id = course_id

        self.course_credits = 0

        self.lectures = [] # vector<Lecture> == vector<vector<Slot>>
        self.tutorials = []
        self.practicals = []

        self.name = ""
        self.midsem = ""
        self.compre = ""

        self.details = ""

        self.combos = [] # vector<Combo>

    def __repr__(self):
        return f"Course(course_id = {self.course_id}, name = {self.name}, midsem = {self.midsem}, compre = {self.compre}, details = {self.details}\nlectures = {self.lectures}\n, tutorials = {self.tutorials}\n, practicals = {self.practicals}\n, combos = {self.combos})"



# ----------------------------------------------------------------

courses = []

num_courses = int(input("Enter the number of courses:"))

for i in range(num_courses): 
    course_id = (input(f"Enter the course id for course {i+1}:"))
    courses.append(Course(course_id))


def check_if_input_is_valid():

    global num_courses

    if num_courses > 12:
        print(f"Ya bitch nice try. Enter fewer courses next time mf.\n")
        exit(0)
    
    def check_for_duplicate_course_ids():
        distinct_courses = set()

        for course in courses:
            if course.course_id in distinct_courses:
                print(f"Duplicate course id: \"{course.course_id}\". Please enter unique course ids.\n")
                exit(0)
            
            distinct_courses.add(course.course_id)

    check_for_duplicate_course_ids()


check_if_input_is_valid()


#---------------------------------------------------
# print("You have entered the following courses: ")
# for course in courses: print(repr(course))
#---------------------------------------------------

# pages 10 to 73.
# excel sheet modified (using rows_remover.py) and saved.

# --------------------------------------------------

def get_slots_from_string(s, section_type):

    slots = []
    prev = 0


    # s can be NaN.
    if isinstance(s, str): pass
    else: return slots


    n = len(s)
    # print("s: ", s)

    for i in range(len(s)):

        if s[i].isdigit():

            days_string = s[prev:i]

            prev = i
            while i+1 < n and (s[i+1].isdigit() or s[i+1] == ' '):
                i += 1
            
            periods_string = s[prev:i+1]

            days = days_string.split()
            periods = periods_string.split()

            # print(days, periods)
            
            for day in days:
                for period in periods:
                    slots.append(Slot(day, period, section_type))

                # #edge case for practicals: W 1 2
                # if day.isdigit():
                #     continue

                # slots.append(Slot(day, s[i]))
            prev = i


    return slots
    


'''
Need to pre-cook all the missing data for each course.
'''



excel_file_path = "Timetable_27_Dec_2024_removed_removed_rows_removed.xlsx"

try:
    df = pd.read_excel(excel_file_path)
except PermissionError:
    print(f"Permission denied: Unable to access '{excel_file_path}'. Please check if the file is open or if you have the necessary permissions.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    exit(1)




flag = False
curr_course_idx = -1

for index, row in df.iterrows() :

    if row[1] != '' and isinstance(row[1], str) and row[1].lower() != 'lecture' and row[1].lower() != 'tutorial' and row[1].lower() != 'practical':

        flag = False
        for i, course in enumerate(courses): 
            if row[1] == course.course_id:
                
                flag = True
                curr_course_idx = i
                
                course.name = row[2] # course.name = row["Course Name"]
                course.course_credits = row[5]
                course.midsem = row[10] # course.midsem = row["Midsem"]
                course.compre = row[11] # course.compre = row["Compre"]


    if flag == True : 
        if row[6] == '' or isinstance(row[6], str) == False:
            continue
        else:
            section = row[6]

            # debugging---------------------------
            # print(section)
            # temp = []
            # temp = get_slots_from_string(row[9])
            # print(temp)
            # for slot in temp:
            #     print(slot.day, slot.period)
            # -------------------------------------
            

            if section[0] == 'L': courses[curr_course_idx].lectures.append(get_slots_from_string(row[9], 'L'))
            elif section[0] == 'T': courses[curr_course_idx].tutorials.append(get_slots_from_string(row[9], 'T'))
            else: courses[curr_course_idx].practicals.append(get_slots_from_string(row[9], 'P'))

    else : 

        pass

# check if user had inputted correct course IDs
for course in courses:
    if course.name == "":
        print(f"Error: Course ID '{course.course_id}' not found in the scraped data.")
        exit(1)

#---------------------------------------------------
# print("updated details after scraping: ")
# for course in courses: print(repr(course))
#---------------------------------------------------


# making combos [i.e. combinations of lectures, tutorials, practicals]
for course in courses:

    cl = len(course.lectures)
    ct = len(course.tutorials)
    cp = len(course.practicals)

    if cl == 0:
        if ct == 0:
            if cp == 0:
                continue
            else:
                for k in range(cp):
                    course.combos.append(Combo([], [], course.practicals[k]))
        else:
            if cp == 0:
                for j in range(ct):
                    course.combos.append(Combo([], course.tutorials[j], []))
            else:
                for j in range(ct):
                    for k in range(cp):
                        course.combos.append(Combo([], course.tutorials[j], course.practicals[k]))
    elif ct == 0:
        if cp == 0:
            for i in range(cl):
                course.combos.append(Combo(course.lectures[i], [], []))
        else:
            for i in range(cl):
                for k in range(cp):
                    course.combos.append(Combo(course.lectures[i], [], course.practicals[k]))
    elif cp == 0:
        for i in range(cl):
            for j in range(ct):
                course.combos.append(Combo(course.lectures[i], course.tutorials[j], []))
    else:
        for i in range(cl):
            for j in range(ct):
                for k in range(cp):
                    course.combos.append(Combo(course.lectures[i], course.tutorials[j], course.practicals[k]))


    # the following code didnt work cuz there was a possibility of lecs / tuts / pracs being empty.

    # for i in range(len(course.lectures)):
    #     for j in range(len(course.tutorials)):
    #         for k in range(len(course.practicals)):

    #             no_of_slots = len(course.lectures[i]) + len(course.tutorials[j]) + len(course.practicals[k])

    #             slots_used = set()
    #             for slot in course.lectures[i]: slots_used.add(slot)
    #             for slot in course.tutorials[j]: slots_used.add(slot)
    #             for slot in course.practicals[k]: slots_used.add(slot)

    #             no_of_distinct_slots = len(slots_used)

    #             if no_of_slots != no_of_distinct_slots:
    #                 continue
                
    #             course.combos.append(Combo(course.lectures[i], course.tutorials[j], course.practicals[k]))



# updating the details of each course:
for course in courses: course.details = course.course_id + ' - ' + course.name


#---------------------------------------------------
print("updated details after making combos: ")
for course in courses: print(repr(course))
#---------------------------------------------------



# ALL GOOD UNTIL HERE ^ ^ ^ ^  -----------------------------------------------------------------------------------------------------------


# FIRST CONDITION: Sum of credits of input  <= 25!
def check_credits_limit():

    global courses

    credits_sum = 0
    for course in courses : 
        credits_sum += course.course_credits

    if credits_sum > 25:
        print(f"The list of entered courses have a credit sum of {credits_sum} which exceeds the 25 credit limit. Give a different list of courses.\n")
        exit(0)


check_credits_limit()


#returns true if there is clash, returns false if there is no clash.
def pairwise_clash(idx1, idx2):

    
    
    # does midsem clash?
    if courses[idx1].midsem == courses[idx2].midsem :
        return True
    
    # does compre clash?
    if courses[idx1].compre == courses[idx2].compre :
        return True

    
    outer_flag = False
    for combo1 in courses[idx1].combos : 
        for combo2 in courses[idx2].combos :
            
            inner_flag = True
            # if any of the slots are the same, then clash
            for slot1 in combo1.slots :
                for slot2 in combo2.slots :
                    if slot1 == slot2 :
                        inner_flag = False
                        

            if inner_flag == True :
                outer_flag = True
                
    if outer_flag == True : # there exists a non-clash pair of combos.
        return False
    else :
        return True


# Go pairwise

for i in range(len(courses)) :
    for j in range(i+1, len(courses)) :
        
        if pairwise_clash(i, j) == True :
            print(f"Clash detected between {courses[i].course_id} and {courses[j].course_id}.\n")
            exit(0)


# clash example: MATH F243, CS F407. (put these 2 courses as input to see an example of a clash.)

# No clash until now
# TIMETABLE GENERATION CODE BELOW =================================================================
# Try building a timetable------------------------------------------------------------------


# try your cdc's for example:
# CS F303, CS F363, CS F364.

# trying the course I plan to take next sem:
# CS F303, CS F363, CS F364, MATH F243, ECON F354, CS F320.
# SOP: CS F376


courses.sort(key = lambda course : len(course.combos), reverse = True)
# the above sorting slightly optimizes performance. It also takes care of the edge case of SOPs not having any combos.


slots_used = set()
map_timetable = {}
no_of_timetables_generated = 0
successful_timetables = []

# returns true -> if we should keep looking.
# returns false -> if we should stop looking.
def dfs(idx) : 

    global no_of_timetables_generated, successful_timetables, slots_used, map_timetable

    if idx == num_courses:
        no_of_timetables_generated += 1
        successful_timetables.append(map_timetable.copy())

        if no_of_timetables_generated < 50:
            return True
        else:
            return False
        
    
    for combo in courses[idx].combos :
        newly_inserted_slots = set()
        flag = True

        for slot in combo.slots :
            if slot in slots_used :
                flag = False
                break
            else :
                slots_used.add(slot)
                newly_inserted_slots.add(slot)
                map_timetable[slot] = courses[idx].details + ' - ' + slot.section_type


        if flag == True :
            if dfs(idx+1) == False :
                return False


        for x in newly_inserted_slots : 
            slots_used.remove(x)
            del map_timetable[x]

    
    return True

# -------------------------------------------------------

dfs(0)

print(f"\n================================")

print(f"Generated {no_of_timetables_generated} possible timetables.")

# print all successful timetables

for i, timetable in enumerate(successful_timetables):
    print(f"Timetable {i+1}:")
    sorted_slots = sorted(timetable.items(), key = lambda x : x[0])
    for slot, course in sorted_slots:
        print(f"{slot}: {course}")
    print("\n")


# ========================================================================================

# Sum of credits of input  <= 25!

# Go pairwise first:
# 1. Does their midsem clash?
# 2. Does their compre clash?
# 3. create non-intra-clashable tuples of {lecture slot, tutorial slot, practical slot} of each course. store them in vectors for each (inputted) course.
# 4. Now for a pair of courses, if there exists any pair of tuple does not clash, then no clash. else, there is a clash.

# If there is no clash until now... :
# try building a timetable.
# if there is a clash, just return saying there is a clash and abort.
# how to detect there is a clash? 
# choose some tuple of {lecture slot, tutorial slot, practical slot} for course 1. put the occupied slots into a set.
# recurse into the next course.

