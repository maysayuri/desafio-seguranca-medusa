# Especificações Técnicas do Ambiente de Laboratório

Este documento detalha as configurações de hardware e software utilizadas para a realização dos testes de invasão e simulações de força bruta.

## 1. Máquina Atacante: Kali Linux
*   **Sistema Operativo**: Kali Linux 2024.1 (64-bit)
*   **Finalidade**: Execução de ferramentas de reconhecimento, varredura e exploração.
*   **Ferramentas Principais**:
    *   Nmap (Varredura de rede)
    *   Medusa (Ataque de força bruta)
    *   Python 3 (Scripts personalizados)
    *   Bash (Automação de tarefas)

## 2. Máquina Alvo: Metasploitable 2
*   **Sistema Operativo**: Ubuntu Linux (Versão vulnerável personalizada)
*   **Finalidade**: Servir como alvo para testes de segurança em um ambiente controlado.
*   **Serviços Vulneráveis Simulados**:
    *   **FTP (Porta 21)**: Serviço `vsftpd` configurado com credenciais fracas.
    *   **HTTP (Porta 80)**: Servidor Apache rodando a aplicação DVWA (Damn Vulnerable Web Application).
    *   **SMB (Porta 445)**: Serviço Samba configurado para simular vulnerabilidades de rede local.

## 3. Configuração de Rede (Topologia)
*   **Tipo de Rede**: Rede Interna (Host-Only) no VirtualBox.
*   **Segmento de Rede**: 192.168.1.0/24
*   **IP Atacante (Kali)**: 192.168.1.15
*   **IP Alvo (Metasploitable)**: 192.168.1.20
*   **Gateway**: 192.168.1.1
