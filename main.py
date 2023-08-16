import os
import requests
from datetime import datetime
from colorama import Fore, Style

RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
RESET = Fore.RESET


API_KEY = ''  # Replace with your actual API key
ONLINE_CHECK = 'https://emailspam.pro/'

def checkAPIKeyValidity(api_key):
    url = f"https://emailspam.pro/api?apikey={api_key}&action=getCredits"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if 'requestStatus' in data and data['requestStatus'] == 0:
                    return False  # Invalid API key
                else:
                    return True  # Valid API key or other response
            except ValueError:
                return False  # Invalid API key if response is not valid JSON
        else:
            return False  # Invalid API key if there's an issue with the check
    except requests.exceptions.RequestException:
        return False  # Invalid API key if there's a network error


def checkAPIKey():
    if not os.path.exists('key.txt'):
        print(f"{RED}~ API Key file 'key.txt' does not exist. Please set a valid key in the tool to create it.{RESET}")
        exit()
    else:
        with open('key.txt', 'r') as key_file:
            api_key = key_file.read().strip()
            if len(api_key) == 0:
                print(f"{RED}~ API Key is blank. Please set a valid key in the tool to set it.{RESET}")
                exit()
            elif not checkAPIKeyValidity(api_key):
                print(f"{RED}~ Invalid API Key found in 'key.txt'. Please set a valid key in the tool to set it.{RESET}")
                exit()
            else:
                return api_key

def isOnline():
    check = requests.get(ONLINE_CHECK)
    if check.status_code == 200:
        print(f"{GREEN}~ {RESET}Server {GREEN}ONLINE{RESET}{GREEN}{RESET} ~{RESET}")
    else:
        print(f"{RED}~ {RESET}Server {RED}ONLINE{RESET}{RED}{RESET} ~{RESET}")

def setAPIKey():
    if not os.path.exists('key.txt'):
        while True:
            setKey = input(f"{GREEN}~{RESET} Enter your API Key: ")
            if len(setKey) == 40:
                if checkAPIKeyValidity(setKey):
                    print(f"{GREEN}~{RESET} API Key Set{GREEN} Successfully{RESET}")
                    with open('key.txt', 'w') as key_file:
                        key_file.write(setKey)  # Write the API key to the file
                    break  # Exit the loop if the input is valid
                else:
                    print(f"{RED}~ Invalid API Key. Please try again.")
            elif len(setKey) == 0:
                print(f"{RED}~ API Key cannot be blank. Please try again.")
            else:
                print(f"{RED}~ API Key must be exactly 40 characters. Please try again.")
    else:
        api_key = checkAPIKey()  # Check the API key in key.txt
        if not checkAPIKeyValidity(api_key):
            print(f"{RED}~ Invalid API Key found in 'key.txt'. Please run setAPIKey to set a valid key.{RESET}")


def menu():
    print(f"{GREEN}=>{RESET} send-email.com CLI | V1 {GREEN}<={RESET}")
    isOnline()

    api_key = checkAPIKey()  # Check if API key exists and is valid

    print('---------------')
    if checkAPIKeyValidity(api_key):
        print(f"{GREEN}API Key: Valid{RESET}")
    else:
        print(f"{RED}API Key: Invalid{RESET}")
    print('---------------')
    print(f'[{GREEN}+{RESET}]{GREEN} Set API Key{RESET}')
    print('---------------')
    print(f'[{GREEN}1{RESET}]{GREEN} Check Credits{RESET}')
    print(f'[{GREEN}2{RESET}] {GREEN}Create Task{RESET}')
    print(f'[{GREEN}3{RESET}] {GREEN}Check Task Status{RESET}')
    print(f'[{GREEN}4{RESET}] {GREEN}Stop Task{RESET}')
    print(f'[{GREEN}0{RESET}] {GREEN}Exit{RESET}')

    while True:
        chooseOption = input(f"{GREEN}~{RESET} Enter an option: ")
        
        if chooseOption == '1':
            credit_amount = getCreditAmount(api_key)
            print(credit_amount)
        elif chooseOption == '2':
            target_email = input(f"{GREEN}~{RESET} Enter the target email: ")
            amount = input(f"{GREEN}~{RESET} Enter the amount: ")
            create_task_response = createTask(api_key, target_email, amount)
            print(create_task_response)
        elif chooseOption == '3':
            task_id = input(f"{GREEN}~{RESET} Enter the task ID: ")
            task_status = checkTaskStatus(api_key, task_id)
            print(task_status)
        elif chooseOption == '4':
            task_id = input(f"{GREEN}~{RESET} Enter the task ID: ")
            stop_task_response = stopTask(api_key, task_id)
            print(stop_task_response)
        elif chooseOption == '0':
            print(f"{GREEN}~{RESET} Exiting the program.")
            break
        else:
            print(f"{RED}~ Invalid option!{RESET}")

def getCreditAmount(api_key):
    url = f"https://emailspam.pro/api?apikey={api_key}&action=getCredits"
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

def createTask(api_key, target_email, amount):
    url = f"https://emailspam.pro/api?apikey={api_key}&action=createTask&email={target_email}&amount={amount}"
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

def checkTaskStatus(api_key, task_id):
    url = f"https://emailspam.pro/api?apikey={api_key}&action=checkTask&id={task_id}"
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

def stopTask(api_key, task_id):
    url = f"https://emailspam.pro/api?apikey={api_key}&action=stopTask&id={task_id}"
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

# Call the menu function
# by PoppingXanax
menu()
