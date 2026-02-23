# Desafio DIO: Ataques de Força Bruta com Medusa e Kali Linux

## Introdução
Este projeto documenta a execução de ataques de força bruta utilizando o Kali Linux e a ferramenta Medusa, simulando cenários em diferentes serviços para demonstrar a compreensão de técnicas de cibersegurança e medidas de prevenção.

## Descrição do Desafio
O desafio consiste em implementar, documentar e partilhar um projeto prático focado em ataques de força bruta. Foram explorados os seguintes cenários:
- **Reconhecimento**: Descoberta de IP e varredura de portas com Nmap.
- **FTP**: Ataque de força bruta em um servidor FTP.
- **Formulário Web (DVWA)**: Automação de tentativas de login em um formulário web.
- **Password Spraying (SMB)**: Ataque de password spraying em um serviço SMB com enumeração de utilizadores.
- **Automação**: Criação de scripts em Bash e Python para automatizar varreduras e geração de wordlists.
- **Arquitetura**: Documentação da topologia de rede e especificações técnicas do laboratório.

## Ambiente de Simulação e Topologia

### Topologia de Rede e Fluxo de Trabalho

```mermaid
graph LR
    subgraph "Rede de Laboratório (192.168.1.0/24)"
        K[Kali Linux<br/>(Atacante)] --- SW((Switch))
        M[Metasploitable 2<br/>(Alvo)] --- SW
    end
    
    subgraph "Fases do Ataque"
        M --> F[FTP: Porta 21]
        M --> H[HTTP: Porta 80]
        M --> S[SMB: Porta 445]
    end

    style K fill:#1a1a1a,stroke:#333,color:#fff
    style M fill:#7d0000,stroke:#333,color:#fff
    style SW fill:#f4f4f4,stroke:#333
```

Para a execução deste desafio, foi configurado um ambiente simulado no VirtualBox utilizando uma rede interna (Host-Only). As especificações técnicas detalhadas podem ser encontradas no arquivo `especificacoes_tecnicas.md`.

O laboratório incluiu:
- **Servidor FTP**: Configurado com `vsftpd` para permitir acesso anónimo e um utilizador de teste (`testuser:password123`).
- **Servidor Web com DVWA**: Configurado com Apache, MySQL e PHP, e a aplicação Damn Vulnerable Web Application (DVWA) para simular um formulário de login vulnerável. Um formulário de login simples foi criado para o ataque de força bruta.
- **Servidor SMB**: Configurado com Samba para simular um serviço SMB, com um utilizador de teste (`user1:Password123`).

## Ferramentas de Automação Desenvolvidas

Neste projeto, foram desenvolvidos scripts personalizados para otimizar as etapas do teste de invasão:
- **`scanner.sh`**: Script em Bash para automatizar a execução do Nmap com detecção de serviços.
- **`wordlist_gen.py`**: Script em Python para gerar combinações de palavras-passe personalizadas para ataques de força bruta.

## Metodologia do Projeto

### 0. Reconhecimento e Varredura
Antes dos ataques, foi realizada a identificação do alvo na rede e a varredura de serviços abertos:
- **Descoberta de IP**: Utilização do `netdiscover` para localizar o IP da máquina alvo.
- **Nmap**: Varredura de portas para identificar serviços vulneráveis (FTP, HTTP, SMB).
- **Comando**: `nmap -sV 192.168.1.20`

### 1. Ataque de Força Bruta em FTP
- **Ferramenta**: Medusa
- **Alvo**: Servidor FTP local (127.0.0.1)
- **Wordlists**: `users.txt` (testuser, admin, user) e `passwords.txt` (password123, 123456, admin)
- **Comando**: `medusa -h 127.0.0.1 -U users.txt -P passwords.txt -M ftp -O ftp_attack_log.txt`
- **Resultado**: Credenciais `testuser:password123` e `user:password123` foram encontradas.

### 2. Ataque de Força Bruta em Formulário Web
- **Ferramenta**: Script Python personalizado (devido a problemas com o módulo `web-form` do Medusa)
- **Alvo**: Formulário de login em `http://127.0.0.1/login.php`
- **Wordlists**: `web_users.txt` (admin, user, test) e `web_passwords.txt` (password, 123456, admin123)
- **Metodologia**: O script Python envia requisições POST para o formulário, verificando a resposta para a string "Login bem-sucedido!".
- **Resultado**: Credenciais `admin:password` foram encontradas.

### 3. Password Spraying em SMB
- **Ferramenta**: Medusa
- **Alvo**: Servidor SMB local (127.0.0.1)
- **Wordlists**: `smb_users.txt` (user1, user2, admin) e `smb_password.txt` (Password123)
- **Comando**: `medusa -h 127.0.0.1 -U smb_users.txt -P smb_password.txt -M smbnt -O smb_attack_log.txt`
- **Resultado**: Credenciais `user1:Password123`, `user2:Password123` e `admin:Password123` foram identificadas como válidas, embora o Medusa tenha retornado um erro genérico na validação.

## Medidas de Mitigação
Para prevenir ataques de força bruta e password spraying, recomenda-se as seguintes medidas:
- **Políticas de Palavra-passe Fortes**: Exigir palavras-passe complexas, com comprimento mínimo, caracteres especiais, números e letras maiúsculas/minúsculas.
- **Bloqueio de Contas**: Implementar um mecanismo de bloqueio de contas após um número limitado de tentativas falhadas de login.
- **Limitação de Taxa (Rate Limiting)**: Restringir o número de tentativas de login por endereço IP ou por conta em um determinado período.
- **Autenticação Multifator (MFA)**: Adicionar uma camada extra de segurança, exigindo um segundo fator de autenticação.
- **Monitorização e Alerta**: Monitorizar logs de autenticação para detetar padrões de ataques de força bruta e gerar alertas.
- **CAPTCHA**: Utilizar CAPTCHAs em formulários de login para dificultar a automação de ataques.
- **Nomes de Utilizador Complexos**: Evitar nomes de utilizador comuns como "admin", "user", etc.

## Conclusão
Este desafio demonstrou a eficácia de ataques de força bruta e password spraying contra serviços comuns (FTP, Web, SMB) e a importância de implementar medidas de segurança robustas para proteger sistemas contra essas ameaças.

## Referências
- [Kali Linux Official Site](https://www.kali.org/)
- [Medusa Documentation](https://www.foofus.net/?page_id=10)
- [Damn Vulnerable Web Application (DVWA)](https://dvwa.co.uk/)
- [Samba Official Site](https://www.samba.org/)
