import random
import datetime

first_names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia", "David", "Isabella", "Alexander", "Ava"]
middle_names = ["Paul", "Grace", "James", "Rose", "Robert", "Lily", "Daniel", "Mia", "Christopher", "Avery"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Anderson", "Taylor", "Thomas"]

person_list = []

for _ in range(10):
    f_name = random.choice(first_names)
    m_name = random.choice(middle_names)
    l_name = random.choice(last_names)
    dob = datetime.date(random.randint(1970, 2003), random.randint(1, 12), random.randint(1, 28))
    p_number = f"+1 ({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    person_dict = {
        "f_name": f_name,
        "m_name": m_name,
        "l_name": l_name,
        "dob": dob,
        "p_number": p_number
    }
    
    person_list.append(person_dict)

