import datetime
import csv

MAX_DESC_LENGTH = 35
MAX_NUM_DIGITS = 10


def receive_info():
    
    # start?, time, end?
    return 1, 'all', 1 


def parse_csv(path):
    
    array = []
    with open(path, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            array.append(row)
    
    return array[1:]


def create_summary(array, time_range):
    string = ''
    total_expense = 0
    total_income = 0
    
    if time_range == "all":
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"
        string += "All Transaction Info\n"
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"
        for line in array:
            
            cat, desc, amount, date = line
            
            sign = '+'
            if cat == "expense":
                sign = '-'
                total_expense += int(amount)
            else:
                total_income += int(amount)
            
            string += f"{desc.ljust(MAX_DESC_LENGTH)}| {sign}${amount}\n"
            
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"
        string += "Total Income" + " "*(MAX_DESC_LENGTH - 12) + f"| ${total_income}\n"
        string += "Total Expense" + " "*(MAX_DESC_LENGTH - 13) + f"| ${total_expense}\n"
        
        string += "Net Income" + " "*(MAX_DESC_LENGTH - 10)
        if total_expense > total_income:
            string += f"| -${total_expense - total_income}\n"
        elif total_income > total_expense:
            string += f"| +${total_income - total_expense}\n"
        
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"
        
        
    
    else:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days = int(time_range))
        # start_date <= date_to_check <= end_date
        
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"
        string += f"{start_date} -> {end_date} Transaction Info\n"
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"
        for line in array:
            
            cat, desc, amount, date = line
            
            line_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            
            if not (start_date <= line_date <= end_date):
                continue
            
            sign = '+'
            if cat == "expense":
                sign = '-'
                total_expense += int(amount)
            else:
                total_income += int(amount)
            
            string += f"{desc.ljust(MAX_DESC_LENGTH)}| {sign}${amount}\n"
            
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"
        string += "Total Income" + " "*(MAX_DESC_LENGTH - 12) + f"| ${total_income}\n"
        string += "Total Expense" + " "*(MAX_DESC_LENGTH - 13) + f"| ${total_expense}\n"
        
        string += "Net Income" + " "*(MAX_DESC_LENGTH - 10)
        if total_expense > total_income:
            string += f"| -${total_expense - total_income}\n"
        elif total_income > total_expense:
            string += f"| +${total_income - total_expense}\n"
        
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"

    return string


def send_summary(string):
    print(string)
    return


if __name__ == "__main__":
    while (1):
        is_start, time_range, is_end = receive_info()
        if is_start:
            file_path = "./transactions.csv"
            useful_array = parse_csv(file_path)
            summary_string = create_summary(useful_array, time_range)
            send_summary(summary_string)
            
        if is_end:
            exit()


# Tracking Date -> Tracking Date
# ----------------------
# Line Item     | +/- amount
# Line Item     | +/- amount
# Line Item     | +/- amount
# ----------------------
# Total Income  | amount
# Total Expenses| amount
# Total Net:    | +/- amount

# Net Income      |