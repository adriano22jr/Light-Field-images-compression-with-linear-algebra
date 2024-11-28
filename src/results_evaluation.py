import sys, os, subprocess

decompressed_path = ""
original_path = ""
compressed_video_path = ""
if(len(sys.argv[1:]) == 3):
    decompressed_path = sys.argv[1]
    original_path = sys.argv[2]
    compressed_video_path = sys.argv[3]
else:
    print("Specify those parameters:\n\t-Decompressed input path (es. ./uncompressed_dataset_name/first_frame.png)\n\t-Original input path (es. ./dataset_name/first_frame.png)\n\t-Compressed video path (es. ./video_name.mp4)")
    exit()


# Calculate the compression ratio
size = 0
folderpath = os.path.abspath(os.path.dirname(original_path[:-(len(original_path.split('/')[-1]))]))
for path, dirs, files in os.walk(folderpath):
    for f in files:
        fp = os.path.join(path, f)
        size += os.path.getsize(fp)
        
decompressed_size = 0
decompressed_folderpath = os.path.abspath(os.path.dirname(decompressed_path[:-(len(decompressed_path.split('/')[-1]))]))
for path, dirs, files in os.walk(decompressed_folderpath):
    for f in files:
        fp = os.path.join(path, f)
        decompressed_size += os.path.getsize(fp)

videosize = os.stat(os.path.abspath(compressed_video_path)).st_size  
print("Initial size of dataset: {} MB".format(size/1000000))
print("Final size of dataset: {} MB".format(decompressed_size/1000000))
print("Compressed video size: {} MB".format(videosize/1000000))
print("Compression ratio dataset/dataset: " + str(size/decompressed_size)) 
print("Compression ratio dataset/video: " + str(size/videosize))


# ffmpeg call for ssim evaluation
subprocess.run(["../../bin/ffmpeg", "-i", decompressed_path, "-i", original_path, "-lavfi", "ssim=stats_file=ssim_logfile.txt", "-f", "null", "-"])

# ffmpeg call for psnr evaluation
subprocess.run(["../../bin/ffmpeg", "-i", decompressed_path, "-i", original_path, "-lavfi", "psnr=stats_file=psnr_logfile.txt", "-f", "null", "-"])