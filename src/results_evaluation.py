import sys, os, subprocess

decompressed_path = ""
original_path = ""
compressed_video_path = ""
mode = ""
if(len(sys.argv[1:]) == 4):
    decompressed_path = sys.argv[1]
    original_path = sys.argv[2]
    compressed_video_path = sys.argv[3]
    mode = sys.argv[4]
else:
    print("Specify those parameters:\n\t-Decompressed input path (es. ./uncompressed_dataset_name/first_frame.png)\n\t-Original input path (es. ./dataset_name/first_frame.png)\n\t-Compressed video path (es. ./video_name.mp4)\n\t-Mode (es. LOSSY, LOSSLESS)")
    exit()


# Calculate the compression ratio
size = 0
folderpath = os.path.abspath(os.path.dirname(original_path[:-(len(original_path.split('/')[-1]))]))
for path, dirs, files in os.walk(folderpath):
    for f in files:
        fp = os.path.join(path, f)
        size += os.path.getsize(fp)
        
decompressed_size = 0
folderpath = os.path.abspath(os.path.dirname(decompressed_path[:-(len(decompressed_path.split('/')[-1]))]))
for path, dirs, files in os.walk(folderpath):
    for f in files:
        fp = os.path.join(path, f)
        decompressed_size += os.path.getsize(fp)

videosize = os.stat(os.path.abspath(compressed_video_path)).st_size  
print("Initial size of dataset: {} MB".format(size/1000000))
print("Compressed video size: {} MB".format(videosize/1000000))
print("Compression ratio: " + str(size/videosize))

if mode == "LOSSY":
    # ffmpeg call for ssim evaluation
    subprocess.run(["../../bin/ffmpeg", "-i", decompressed_path, "-i", original_path, "-lavfi", "ssim=stats_file=ssim_logfile.txt", "-f", "null", "-"])

    # ffmpeg call for psnr evaluation
    subprocess.run(["../../bin/ffmpeg", "-i", decompressed_path, "-i", original_path, "-lavfi", "psnr=stats_file=psnr_logfile.txt", "-f", "null", "-"])