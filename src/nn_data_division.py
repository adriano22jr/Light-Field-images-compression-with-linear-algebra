import os, random, shutil
from typing import List, Tuple

def split_dataset_images(folder_path: str, dataset_prefix: str) -> Tuple[List[str], List[str], List[str]]:
    images = [img for img in os.listdir(folder_path) if img.startswith(dataset_prefix) and img.endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(images)

    total_images = len(images)
    train_size = int(0.8 * total_images)
    val_size = (total_images - train_size) // 2

    train_images = images[:train_size]
    val_images = images[train_size:train_size + val_size]
    test_images = images[train_size + val_size:]

    return train_images, val_images, test_images

def copy_images_to_folders(folder_path: str, train: List[str], val: List[str], test: List[str]):
    train_folder = os.path.join(folder_path, "train")
    val_folder = os.path.join(folder_path, "val")
    test_folder = os.path.join(folder_path, "test")

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    for img in train:
        shutil.copy(os.path.join(folder_path, img), os.path.join(train_folder, img))

    for img in val:
        shutil.copy(os.path.join(folder_path, img), os.path.join(val_folder, img))

    for img in test:
        shutil.copy(os.path.join(folder_path, img), os.path.join(test_folder, img))

if __name__ == "__main__":
    folder_path = "/workspace/nn_datasets/resized/"  
    dataset_prefix = "Messerschmitt"          

    train, val, test = split_dataset_images(folder_path, dataset_prefix)
    copy_images_to_folders(folder_path, train, val, test)