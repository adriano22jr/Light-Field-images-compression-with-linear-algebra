import os
import random
import shutil
from typing import List, Tuple

def split_dataset_images(folder_path: str, dataset_prefix: str) -> Tuple[List[str], List[str], List[str]]:
    """
    Divide le immagini di un dataset in tre liste: train, val e test.

    Args:
        folder_path (str): Percorso alla cartella contenente le immagini.
        dataset_prefix (str): Prefisso del dataset da considerare.

    Returns:
        Tuple[List[str], List[str], List[str]]: Tre liste con i nomi delle immagini per train, val e test.
    """
    # Trova le immagini con il prefisso specificato
    images = [img for img in os.listdir(folder_path) if img.startswith(dataset_prefix) and img.endswith(('.png', '.jpg', '.jpeg'))]

    # Mescola le immagini in modo casuale
    random.shuffle(images)

    # Calcola le dimensioni delle suddivisioni
    total_images = len(images)
    train_size = int(0.8 * total_images)
    val_size = (total_images - train_size) // 2

    # Suddividi le immagini nelle tre liste
    train_images = images[:train_size]
    val_images = images[train_size:train_size + val_size]
    test_images = images[train_size + val_size:]

    return train_images, val_images, test_images

def copy_images_to_folders(folder_path: str, train: List[str], val: List[str], test: List[str]):
    """
    Copia le immagini divise in cartelle chiamate train, val e test.

    Args:
        folder_path (str): Percorso alla cartella contenente le immagini originali.
        train (List[str]): Lista delle immagini per il training.
        val (List[str]): Lista delle immagini per la validazione.
        test (List[str]): Lista delle immagini per il testing.
    """
    # Percorsi delle cartelle di destinazione
    train_folder = os.path.join(folder_path, "train")
    val_folder = os.path.join(folder_path, "val")
    test_folder = os.path.join(folder_path, "test")

    # Creazione delle cartelle se non esistono
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    # Copia delle immagini nelle rispettive cartelle
    for img in train:
        shutil.copy(os.path.join(folder_path, img), os.path.join(train_folder, img))

    for img in val:
        shutil.copy(os.path.join(folder_path, img), os.path.join(val_folder, img))

    for img in test:
        shutil.copy(os.path.join(folder_path, img), os.path.join(test_folder, img))

# Esempio di utilizzo
if __name__ == "__main__":
    folder_path = "/workspace/nn_datasets/resized/"  
    dataset_prefix = "Messerschmitt"          

    train, val, test = split_dataset_images(folder_path, dataset_prefix)

    # Copia delle immagini nelle cartelle train, val e test
    copy_images_to_folders(folder_path, train, val, test)