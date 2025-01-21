from PIL import Image
import os

def resize_image(input_path, output_path, new_size=(960, 720)):
    try:
        with Image.open(input_path) as img:
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            resized_img.save(output_path)
            print(f"Immagine salvata in: {output_path}")
    except Exception as e:
        print(f"Errore durante il ridimensionamento di {input_path}: {e}")

def batch_resize_and_rename(input_folder, output_folder, new_size=(960, 720)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    folder_name = os.path.basename(os.path.normpath(input_folder))
    
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            name, ext = os.path.splitext(filename)
            new_filename = f"{folder_name}_{name}{ext}"
            output_path = os.path.join(output_folder, new_filename)
            
            resize_image(input_path, output_path, new_size)
        else:
            print(f"File {filename} ignorato (non è un'immagine supportata).")


# Ridimensiona tutte le immagini di una cartella
batch_resize_and_rename("../datasets/Blob/", "../nn_datasets/resized")
batch_resize_and_rename("../datasets/Car/", "../nn_datasets/resized")
batch_resize_and_rename("../datasets/Cobblestone/", "../nn_datasets/resized")
batch_resize_and_rename("../datasets/Mannequin/", "../nn_datasets/resized")