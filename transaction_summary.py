import datetime
import csv
import zmq

MAX_DESC_LENGTH = 35
MAX_NUM_DIGITS = 10


def receive_info(socket):
    is_start, time, is_end = 0, 0, 0
    
    message = socket.recv()
    
    command, days = message.decode().split(" ")
    if command == "summary":
        is_start = 1
        time = days
    elif command == "end":
        is_end = 1
        
    return is_start, time, is_end


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
        else:
            string += f"| $0\n"
        
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
        else:
            string += f"| $0\n"
        
        string += "-"*(MAX_DESC_LENGTH+MAX_NUM_DIGITS) + "\n"

    return string


def send_summary(socket, string):
    socket.send(str.encode(string))
    return


if __name__ == "__main__":
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    
    while (1):
        is_start, time_range, is_end = receive_info(socket)
        if is_start:
            file_path = "./transactions.csv"
            useful_array = parse_csv(file_path)
            summary_string = create_summary(useful_array, time_range)
            send_summary(socket, summary_string)
            
        if is_end:
            socket.send(b"getTransactionSummary ending")
            exit()
    
    context.term()


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