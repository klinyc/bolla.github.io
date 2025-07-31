import csv
import sys
import uuid

USERS_CSV = '../data/users.csv'

def add_user(name, phone, email):
    user_id = str(uuid.uuid4())
    bowl_id = str(uuid.uuid4())
    with open(USERS_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, name, phone, email, bowl_id, 0, 0.0, 0.0, 0.0])
    print(f'User added: {name} (ID: {user_id}, Phone: {phone}, Email: {email}, Bowl ID: {bowl_id})')

def list_users():
    with open(USERS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            print(f'ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}, Email: {row[3]}, Bowl ID: {row[4]}, Points: {row[5]}, Total Amount: ${row[6]}, CO2 Reduced: {row[7]}, Landfill Reduced: {row[8]}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python user_management.py [add <name> <phone> <email> | list]')
    elif sys.argv[1] == 'add' and len(sys.argv) == 5:
        add_user(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'list':
        list_users()
    else:
        print('Invalid command.') 