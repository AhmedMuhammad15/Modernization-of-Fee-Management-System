import random

FEES_PER_CREDIT_HOUR = 5000  
ADMISSION_FEE_RATE = 25000   
SECURITY_DEPOSIT_RATE = 10000 
ACTIVITY_CHARGES_RATE = 5000  

def generate_roll_number(dept, batch, student_list):
    matching_students = [x for x in student_list if x['roll_no'].startswith(f"{dept}-{batch}-")]
    if not matching_students:
        next_num = 101
    else:
        last_roll = matching_students[-1]['roll_no']
        try: next_num = int(last_roll.split('-')[-1]) + 1
        except: next_num = 101 + len(matching_students)
    return f"{dept.upper()}-{batch.upper()}-{next_num}"

def generate_bank_receipt(dept, batch):
    return f"CHLN-{dept.upper()}{batch.upper()}-{random.randint(10000, 99999)}"

def calculate_fees(semester, credit_hours):
    base_tuition = float(credit_hours * FEES_PER_CREDIT_HOUR)
    if semester == 1:
        total_computed = base_tuition + ADMISSION_FEE_RATE + SECURITY_DEPOSIT_RATE
    else:
        total_computed = base_tuition + ACTIVITY_CHARGES_RATE
    return total_computed