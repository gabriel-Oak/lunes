import os
import platform

def clear_screen():
    """Limpa a tela do console de forma multiplataforma"""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_separator(char='-', length=50):
    """Imprime uma linha separadora"""
    print(char * length)

def print_header(title):
    """Imprime um cabeçalho formatado"""
    clear_screen()
    print_separator('=')
    print(f"  {title}")
    print_separator('=')