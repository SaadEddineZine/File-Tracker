import os
import time
import shutil
import hashlib
from tkinter import *
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

# Chemin du répertoire à surveiller
DIR_TO_WATCH = "./repertoireTest"
# Fichier de journal pour enregistrer les modifications
LOG_FILE = "modifications.txt"
# Dossier pour les fichiers sensibles
SENSITIVE_FOLDER = "./sensitive"

# Assurez-vous que le dossier sensible existe
if not os.path.exists(SENSITIVE_FOLDER):
    os.makedirs(SENSITIVE_FOLDER)

# Fonction pour calculer le hachage d'un fichier
def compute_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hash_sha256.update(byte_block)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error computing hash for {file_path}: {e}")
        return None

# Fonction pour vérifier si un fichier est sensible (copie existante dans le dossier sensible)
def is_sensitive_file(file_path):
    file_name = os.path.basename(file_path)
    sensitive_file_path = os.path.join(SENSITIVE_FOLDER, file_name)
    return os.path.exists(sensitive_file_path)

# Gestionnaire d'événements pour suivre les modifications
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, log_text):
        self.log_text = log_text

    def on_modified(self, event):
        if not event.is_directory:
            self.log_change("Modifié", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.log_change("Créé", event.src_path)

    def log_change(self, action, file_path):
        # Vérifie si le fichier est sensible
        if is_sensitive_file(file_path):
            log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action} : {file_path} [ALERTE : FICHIER SENSIBLE]"
            self.alert_file_change(file_path)
        else:
            log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action} : {file_path}"
        
        # Enregistrer dans le fichier de log
        with open(LOG_FILE, "a") as log:
            log.write(log_entry + "\n")
        
        # Afficher dans l'interface
        self.log_text.insert(END, log_entry + "\n")
        self.log_text.yview(END)

    def alert_file_change(self, file_path):
        # Display an alert in the GUI
        self.log_text.insert(END, f"*** ALERTE : Modification du fichier sensible détectée *** {file_path}\n")
        self.log_text.yview(END)

# Fonction pour ajouter un fichier sensible
def add_sensitive_file():
    file_name = file_name_entry.get()
    if not file_name:
        messagebox.showwarning("Nom de fichier manquant", "Veuillez entrer un nom de fichier.")
        return
    
    # Vérifier si le fichier existe déjà
    file_path = os.path.join(DIR_TO_WATCH, file_name)
    if os.path.exists(file_path):
        messagebox.showwarning("Fichier existant", "Le fichier existe déjà dans le répertoire surveillé.")
        return
    
    # Créer un nouveau fichier si il n'existe pas
    try:
        with open(file_path, 'w') as f:
            f.write("Contenu initial du fichier sensible.")
        
        # Copier le fichier dans le dossier sensible
        sensitive_file_path = os.path.join(SENSITIVE_FOLDER, file_name)
        shutil.copy(file_path, sensitive_file_path)
        
        log_text.insert(END, f"*** Fichier sensible ajouté et copié vers le dossier sensible: {file_name} ***\n")
        log_text.yview(END)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la création du fichier sensible: {e}")

# Fonction pour démarrer l'observateur
def start_monitoring():
    # Assurez-vous que le dossier à surveiller existe
    if not os.path.exists(DIR_TO_WATCH):
        os.makedirs(DIR_TO_WATCH)

    event_handler = FileChangeHandler(log_text)
    observer = Observer()
    observer.schedule(event_handler, path=DIR_TO_WATCH, recursive=False)

    observer.start()
    status_label.config(text="Surveillance en cours...", fg="green")
    stop_button.config(state=NORMAL)
    
    # Run the observer in a separate thread to avoid freezing the GUI
    def stop_observer():
        observer.stop()
        observer.join()
        status_label.config(text="Surveillance arrêtée.", fg="red")
        stop_button.config(state=DISABLED)

    # Make sure the stop button can stop the observer
    stop_button.config(command=stop_observer)

# Créer l'interface utilisateur
root = Tk()
root.title("Moniteur de Fichiers")
root.geometry("700x500")

# Label pour le statut
status_label = Label(root, text="Surveillance arrêtée.", fg="red", font=("Helvetica", 14))
status_label.pack(pady=10)

# Zone de texte pour afficher les logs
log_text = Text(root, height=15, width=70, wrap=WORD, font=("Courier", 10))
log_text.pack(pady=10)

# Entry et bouton pour ajouter un fichier sensible
file_name_label = Label(root, text="Nom du fichier sensible :")
file_name_label.pack(pady=5)

file_name_entry = Entry(root, width=40)
file_name_entry.pack(pady=5)

add_file_button = Button(root, text="Ajouter fichier sensible", command=add_sensitive_file)
add_file_button.pack(pady=10)

# Boutons pour démarrer, arrêter la surveillance
start_button = Button(root, text="Démarrer la surveillance", command=lambda: threading.Thread(target=start_monitoring).start())
start_button.pack(pady=10)

stop_button = Button(root, text="Arrêter la surveillance", state=DISABLED)
stop_button.pack(pady=10)

root.mainloop()
