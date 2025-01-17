import os, cv2, sys, time, numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
import re
import subprocess

def svd_compression(input_path, output_path, n_components):
    number_of_files = len(next(os.walk(input_path))[2])    
        
    start_time = time.time()    
    for number in range(number_of_files):
        num = str(number).zfill(3)
        
        # Open frame    
        frame = cv2.cvtColor(cv2.imread(input_path + "Frame_" + num + ".png"), cv2.COLOR_BGR2RGB)
        
        # Split into red, green and blue channels
        r, g, b = cv2.split(frame)
        r, g, b = r/255, g/255, b/255
        
        # Perform SVD on each channel
        svd_r = TruncatedSVD(n_components = n_components)
        r_compressed = svd_r.fit_transform(r)
        
        svd_g = TruncatedSVD(n_components = n_components)
        g_compressed = svd_g.fit_transform(g)
        
        svd_b = TruncatedSVD(n_components = n_components)
        b_compressed = svd_b.fit_transform(b)
        
        # Reconstruct the image
        r_reconstructed = svd_r.inverse_transform(r_compressed)
        g_reconstructed = svd_g.inverse_transform(g_compressed)
        b_reconstructed = svd_b.inverse_transform(b_compressed)
        
        reconstructed_frame = cv2.merge((r_reconstructed, g_reconstructed, b_reconstructed))
        result = cv2.normalize(reconstructed_frame, dst=None, alpha=0, beta=255,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        
        
        cv2.imwrite(output_path + "/Frame_" + num + ".png", cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
    
    end_time = time.time()
    print("SVD compression completed in ", end_time - start_time, " seconds.")

def calculate_metrics(decompressed_path, original_path):
    # Esegui il comando per calcolare SSIM usando ffmpeg
    ssim_result = subprocess.run(
        ["../../bin/ffmpeg", "-i", decompressed_path, "-i", original_path, "-lavfi", "ssim=stats_file=ssim_logfile.txt", "-f", "null", "-"],
        capture_output=True, text=True
    )
    
    # Esegui il comando per calcolare PSNR usando ffmpeg
    psnr_result = subprocess.run(
        ["../../bin/ffmpeg", "-i", decompressed_path, "-i", original_path, "-lavfi", "psnr=stats_file=psnr_logfile.txt", "-f", "null", "-"],
        capture_output=True, text=True
    )
    
    # Estrai il valore SSIM dal log
    ssim_match = re.search(r"All:([\d.]+)", ssim_result.stderr)
    ssim = float(ssim_match.group(1)) if ssim_match else None

    # Estrai il valore PSNR medio dal log
    psnr_match = re.search(r"average:([\d.]+)", psnr_result.stderr)
    #print(psnr_result.stderr)
    psnr = float(psnr_match.group(1)) if psnr_match else None
    
    return ssim, psnr

# Traccia i grafici
def plot_metrics_separate(ssim_values, psnr_values, svd_components):
    plt.figure(figsize=(12, 8))
    psnr_values = [0 if x is None else x for x in psnr_values]
    #Grafico per SSIM
    plt.subplot(2, 1, 1)
    plt.xticks(svd_components)
    plt.plot(svd_components, ssim_values, marker='o', color='blue', label='SSIM')
    plt.title("SSIM in base al numero di componenti SVD", fontsize=14)
    plt.xlabel("Numero di componenti SVD", fontsize=12)
    plt.ylabel("SSIM", fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend(fontsize=12)
    #  Grafico per PSNR
    plt.subplot(2, 1, 2)
    plt.xticks(svd_components)
    plt.plot(svd_components, psnr_values, marker='s', color='orange', label='PSNR')
    plt.title("PSNR in base al numero di componenti SVD", fontsize=14)
    plt.xlabel("Numero di componenti SVD", fontsize=12)
    plt.ylabel("PSNR (dB)", fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend(fontsize=12)
    plt.tight_layout()  # Adatta layout
    plt.show()
    plt.savefig("ssim_psnr_vs_svd_components.png")


if __name__ == '__main__':
    input_path = ""
    output_path = ""
    components = 0

    if(len(sys.argv[1:]) == 2):
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    else:
        print("Specify those parameters:\n\t-Input path (es. ./ArtGallery/)\n\t-Output path (es. ./ArtGalleryCompressed/)\n\t-Number of components")
        exit()
    
    sample_image = cv2.imread(os.path.join(input_path, "Frame_000.png"))
    height, width, _ = sample_image.shape
    max_component = min(height, width)
    components_range = [round(x) for x in np.linspace(20, max_component, 10)]
    ssim_scores = []
    psnr_scores = []

    for n_components in components_range:
        print(f"Testing SVD compression with {n_components} components...")
        # Create directory for the current n_components
        component_dir = os.path.join(output_path, str(n_components))
        os.makedirs(component_dir, exist_ok=True)
        svd_compression(input_path, component_dir, n_components)
    
        # Calcola SSIM e PSNR
        ssim, psnr = calculate_metrics(component_dir + "/Frame_000.png", input_path + "Frame_000.png")
        ssim_scores.append(ssim)
        psnr_scores.append(psnr)

    print(ssim_scores)
    print(psnr_scores)
    plot_metrics_separate(ssim_scores,psnr_scores,components_range)
