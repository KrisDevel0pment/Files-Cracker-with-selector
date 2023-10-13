import fitz
import itertools
import time
from colorama import init, Fore, Style
from tqdm import tqdm
from tkinter import filedialog
import tkinter as tk

#Explications et requierements
    #Script Python pour cracker les mots de passe des fichier ZIP et PDF.
    #Crée par KrisDevel0pment
    #Lien de mon GitHub : https://github.com/KrisDevel0pment 

    #Avant d'executer le script, merci d'installer les modules suivants :
        #pip install tqdm PyMuPDF colorama pyzipper

    #Ligne 87 : max_length = (Nombre de caratère max)

init(autoreset=True)  # Active la coloration des polices

def choose_file(file_type):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[(f"{file_type} files", f"*.{file_type}")])
    return file_path

def brute_force_zip(charset, max_length):
    zip_file_path = choose_file("zip")
    
    if not zip_file_path:
        print("Fichier ZIP non sélectionné. Sortie du programme.")
        return

    try:
        with pyzipper.AESZipFile(zip_file_path) as zipf:
            total_attempts = 0
            start_time = time.time()
            for length in range(1, max_length + 1):
                with tqdm(total=len(charset)**length, desc=f"Testing ZIP passwords of length {length}", bar_format="{l_bar}{bar}", position=0, colour='green') as pbar:
                    for attempt in itertools.product(charset, repeat=length):
                        password = ''.join(attempt)
                        try:
                            zipf.extractall(pwd=password.encode('utf-8'))
                            end_time = time.time()
                            pbar.close()
                            print("\n\n")
                            print(Fore.RESET + Style.RESET_ALL + f"ZIP Password found: {Fore.GREEN}{password}")
                            time_taken = f"Time taken: {Fore.GREEN}{end_time - start_time:.2f} {Style.BRIGHT}seconds"
                            print(time_taken)
                            return password
                        except Exception as e:
                            pbar.update(1)
                            continue  # Ajout de l'instruction continue pour gérer les erreurs
        print("Password not found after testing", total_attempts, "combinations.")
    except Exception as e:
        print(f"Error: {e}")

def brute_force_pdf(charset, max_length):
    pdf_file_path = choose_file("pdf")
    
    if not pdf_file_path:
        print("Fichier PDF non sélectionné. Sortie du programme.")
        return

    try:
        pdf_document = fitz.open(pdf_file_path)
        total_attempts = 0
        start_time = time.time()
        
        for length in range(1, max_length + 1):
            with tqdm(total=len(charset)**length, desc=f"Testing PDF encryption passwords of length {length}", bar_format="{l_bar}{bar}", position=0, colour='green') as pbar:
                for attempt in itertools.product(charset, repeat=length):
                    password = ''.join(attempt)
                    try:
                        for page in pdf_document:
                            if page.authenticate(password):
                                end_time = time.time()
                                pbar.close()
                                print("\n\n")
                                print(Fore.RESET + Style.RESET_ALL + f"PDF Encryption Password found: {Fore.GREEN}{password}")
                                time_taken = f"Time taken: {Fore.GREEN}{end_time - start_time:.2f} {Style.BRIGHT}seconds"
                                print(time_taken)
                                return password
                        pbar.update(1)  # Mise à jour de la barre de progression après chaque tentative
                    except Exception as e:
                        pbar.update(1)
                        continue  # Ajout de l'instruction continue pour gérer les erreurs

        print("Password not found after testing", total_attempts, "combinations.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:'\",.<>/?~"
    max_length = 10 

    file_type = input("Entrez 'zip' pour tester un fichier ZIP ou 'pdf' pour tester un fichier PDF: ")
if file_type == "zip":
    brute_force_zip(charset, max_length)
elif file_type == "pdf":
    brute_force_pdf(charset, max_length)
else:
    print("Type de fichier non reconnu. Sortie du programme.")