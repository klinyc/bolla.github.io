import csv
import sys
import uuid
import random
from datetime import datetime

TRANSACTIONS_CSV = '../data/transactions.csv'
USERS_CSV = '../data/users.csv'
RESTAURANTS_CSV = '../data/restaurants.csv'

# Helper functions to get user and restaurant data
def get_user_data(user_id):
    with open(USERS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if row[0] == user_id:
                return {'name': row[1], 'bowl_id': row[4]}
    return None

def get_restaurant_data(restaurant_id):
    with open(RESTAURANTS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if row[0] == restaurant_id:
                return {'name': row[1], 'location': row[2]}
    return None

def generate_transaction_amount():
    # Generate a realistic transaction amount for food waste reduction
    # Range: $8.50 to $24.99 (typical meal prices)
    return round(random.uniform(8.50, 24.99), 2)

def update_user_transaction_amount(user_id, transaction_amount):
    """Update the total transaction amount for a user"""
    users = []
    with open(USERS_CSV, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == user_id:
                current_total = float(row[6]) if row[6] else 0.0
                row[6] = str(round(current_total + transaction_amount, 2))
            users.append(row)
    
    with open(USERS_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(users)

# Add a check-in and increment user points

def add_checkin(user_id, restaurant_id):
    transaction_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Get user and restaurant data
    user_data = get_user_data(user_id)
    restaurant_data = get_restaurant_data(restaurant_id)
    
    if not user_data or not restaurant_data:
        print(f'Error: User or restaurant not found')
        return
    
    transaction_amount = generate_transaction_amount()
    
    # Add transaction record with additional columns
    with open(TRANSACTIONS_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            transaction_id, user_id, restaurant_id, timestamp,
            user_data['name'], restaurant_data['name'], restaurant_data['location'], user_data['bowl_id'], transaction_amount
        ])
    
    # Update user's total transaction amount
    update_user_transaction_amount(user_id, transaction_amount)
    # Increment user points
    users = []
    with open(USERS_CSV, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == user_id:
                row[5] = str(int(row[5]) + 1)  # points
                row[7] = str(float(row[7]) + 1.1)  # co2_reduced
                row[8] = str(float(row[8]) + 1.11)  # landfill_reduced
            users.append(row)
    with open(USERS_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(users)
    print(f'Check-in added for user {user_id} at restaurant {restaurant_id}')

def list_transactions():
    with open(TRANSACTIONS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) >= 9:  # New format with location
                print(f'Transaction ID: {row[0]}, User: {row[4]}, Restaurant: {row[5]}, Location: {row[6]}, Bowl ID: {row[7]}, Amount: ${row[8]}, Time: {row[3]}')
            elif len(row) >= 8:  # Format without location
                print(f'Transaction ID: {row[0]}, User: {row[4]}, Restaurant: {row[5]}, Bowl ID: {row[6]}, Amount: ${row[7]}, Time: {row[3]}')
            else:  # Old format
                print(f'Transaction ID: {row[0]}, User ID: {row[1]}, Restaurant ID: {row[2]}, Time: {row[3]}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python transactions.py [add <user_id> <restaurant_id> | list]')
    elif sys.argv[1] == 'add' and len(sys.argv) == 4:
        add_checkin(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'list':
        list_transactions()
    else:
        print('Invalid command.') 