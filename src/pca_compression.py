import os, cv2, sys, time, numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def pca_compression(input_path, output_path, n_components):
    number_of_files = len(next(os.walk(input_path))[2])    
        
    start_time = time.time()    
    for number in range(number_of_files):
        num = str(number).zfill(3)
        
        # Open frame    
        frame = cv2.cvtColor(cv2.imread(input_path + "Frame_" + num + ".png"), cv2.COLOR_BGR2RGB)
        
        # Split into red, green and blue channels
        r, g, b = cv2.split(frame)
        r, g, b = r/255, g/255, b/255
        
        # Perform PCA on each channel
        pca_r = PCA(n_components = n_components)
        r_compressed = pca_r.fit_transform(r)
        
        pca_g = PCA(n_components = n_components)
        g_compressed = pca_g.fit_transform(g)
        
        pca_b = PCA(n_components = n_components)
        b_compressed = pca_b.fit_transform(b)
        
        # Reconstruct the image
        r_reconstructed = pca_r.inverse_transform(r_compressed)
        g_reconstructed = pca_g.inverse_transform(g_compressed)
        b_reconstructed = pca_b.inverse_transform(b_compressed)
        
        reconstructed_frame = cv2.merge((r_reconstructed, g_reconstructed, b_reconstructed))
        result = cv2.normalize(reconstructed_frame, dst=None, alpha=0, beta=255,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # image_normalized = (reconstructed_frame - np.min(reconstructed_frame)) / (np.max(reconstructed_frame) - np.min(reconstructed_frame))
        # scaled_frame = (255 * reconstructed_frame).astype(np.uint8)
        
        cv2.imwrite(output_path + "Frame_" + num + ".png", cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
        """
        fig = plt.figure(figsize=(reconstructed_frame.shape[1] / 1, reconstructed_frame.shape[0] / 1), dpi=1)
        plt.axis('off')
        plt.imshow(reconstructed_frame)
        plt.savefig(output_path + "Frame_" + num + ".png",  dpi=1, bbox_inches = 'tight', pad_inches = 0)
        """
    
    end_time = time.time()
    print("PCA compression completed in ", end_time - start_time, " seconds.")



if __name__ == '__main__':
    input_path = ""
    output_path = ""
    components = 0

    if(len(sys.argv[1:]) == 3):
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        components = int(sys.argv[3])
    else:
        print("Specify those parameters:\n\t-Input path (es. ./ArtGallery/)\n\t-Output path (es. ./ArtGalleryCompressed/)\n\t-Number of components")
        exit()
    
    print(f"Starting pca compression using {components} components")
    pca_compression(input_path, output_path, components)