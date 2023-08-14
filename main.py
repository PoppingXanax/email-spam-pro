import requests
from colorama import Fore, Style

RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
RESET = Fore.RESET

API_KEY = 'KEY'  # Replace with your actual API key

def listMenu():
    print(f'[{GREEN}1{RESET}] {GREEN}Check Credits{RESET}')
    print(f'[{GREEN}2{RESET}] {GREEN}Create Task{RESET}')
    print(f'[{GREEN}3{RESET}] {GREEN}Check Task Status{RESET}')
    print(f'[{GREEN}4{RESET}] {GREEN}Stop Task{RESET}')
    print(f'[{GREEN}0{RESET}] {GREEN}Exit{RESET}')

def menu():
    print(f"{GREEN}=>{RESET} EmailSpam.Pro CLI | V1 {GREEN}<={RESET}")
    listMenu()
    
    while True:
        chooseOption = input(f"{GREEN}~{RESET} Enter an option: ")
        
        if chooseOption == '1':
            credit_amount = getCreditAmount()
            print(credit_amount)
        elif chooseOption == '2':
            target_email = input(f"{GREEN}~{RESET} Enter the target email: ")
            amount = input(f"{GREEN}~{RESET} Enter the amount: ")
            create_task_response = createTask(target_email, amount)
            print(create_task_response)
        elif chooseOption == '3':
            task_id = input(f"{GREEN}~{RESET} Enter the task ID: ")
            task_status = checkTaskStatus(task_id)
            print(task_status)
        elif chooseOption == '4':
            task_id = input(f"{GREEN}~{RESET} Enter the task ID: ")
            stop_task_response = stopTask(task_id)
            print(stop_task_response)
        elif chooseOption == '0':
            print(f"{GREEN}~{RESET} Exiting the program.")
            break
        else:
            print(f"{RED}~ Invalid option!{RESET}")

def getCreditAmount():
    url = f"https://emailspam.pro/api?apikey={API_KEY}&action=getCredits"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'credits' in data:
            credit_amount = data['credits']
            return f"{GREEN}~{RESET} Your credit amount is: {GREEN}{credit_amount}"
        else:
            return f"{GREEN}~{RESET} Credit information not available in the response."
    else:
        return f"{RED}{GREEN}~ Failed to fetch data. Status code: {response.status_code}"

from datetime import datetime

def createTask(target_email, amount):
    url = f"https://emailspam.pro/api?apikey={API_KEY}&action=createTask&email={target_email}&amount={amount}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'requestStatus' in data and data['requestStatus'] == 1:
            task_id = data.get('taskId', 'Unknown')
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"{GREEN}~ Task created successfully!\n  Task ID: {task_id}\n  Created At: {created_at}{RESET}"
        elif 'requestStatus' in data and data['requestStatus'] == 0:
            if 'requestError' in data:
                error_message = data['requestError']
                if 'Min' in error_message and 'Max' in error_message:
                    return f"{RED}~ Failed to create task. {error_message}{RESET}"
            else:
                return f"{RED}~ Failed to create task. Unknown error response.{RESET}"
        else:
            return f"{RED}~ Failed to create task. Unknown response data.{RESET}"
    else:
        return f"{RED}~ Failed to create task. Status code: {response.status_code}{RESET}"

def checkTaskStatus(task_id):
    url = f"https://emailspam.pro/api?apikey={API_KEY}&action=checkTask&id={task_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'requestStatus' in data and data['requestStatus'] == 1:
            task_email = data.get('taskEmail', 'Unknown')
            task_status = data.get('taskStatus', 'Unknown')
            task_amount = data.get('taskAmount', 'Unknown')
            task_amount_sent = data.get('taskAmountSent', 'Unknown')
            task_progress = data.get('taskProgress', 'Unknown')
            task_start_date = data.get('taskStartDate', 'Unknown')
            
            start_date_time = datetime.utcfromtimestamp(task_start_date).strftime("%Y-%m-%d %H:%M:%S")
            
            return (f"{GREEN}~ Task status:{RESET}\n"
                    f"  Email: {GREEN}{task_email}{RESET}\n"
                    f"  Status: {GREEN}{task_status}{RESET}\n"
                    f"  Amount: {GREEN}{task_amount}{RESET}\n"
                    f"  Amount Sent: {GREEN}{task_amount_sent}{RESET}\n"
                    f"  Progress: {GREEN}{task_progress}%{RESET}\n"
                    f"  Start Date: {GREEN}{start_date_time}{RESET}")
        else:
            return f"{RED}~ Failed to check task status. Unknown response data.{RESET}"
    else:
        return f"{RED}~ Failed to check task status. Status code: {response.status_code}{RESET}"


def stopTask(task_id):
    url = f"https://emailspam.pro/api?apikey={API_KEY}&action=stopTask&id={task_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'requestStatus' in data and data['requestStatus'] == 1:
            return f"{GREEN}~ Task stopped successfully!{RESET}"
        elif 'requestStatus' in data and data['requestStatus'] == 0:
            return f"{RED}~ Task was not stopped.{RESET}"
        else:
            return f"{RED}~ Failed to stop task. Unknown response data.{RESET}"
    else:
        return f"{RED}~ Failed to stop task. Status code: {response.status_code}{RESET}"

menu()
# by PoppingXanax
