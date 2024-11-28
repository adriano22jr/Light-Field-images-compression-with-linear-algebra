import sys, pathlib
import compressors

algorithm = ""
input_path = ""
output_path = ""

if(len(sys.argv[1:]) == 3):
    algorithm = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]
else:
    print("Specify those parameters:\n\t-Compression algorithm (HEVC, AV1, VP9, HUFFYUV, UTVIDEO, FFV1, HEVC-VS, AV1-VS, VP9-VS)\n\t-Input path (es. ./ArtGallery2/Frame_%3d.png)\n\t-Output path (es. output.mp4)")
    exit()
    
match algorithm:
    case "HEVC":
        if(pathlib.Path(output_path).suffix == ".mp4"):
            compressors.compressor_HEVC(input_path, output_path)
        else:
           print("HEVC needs an output file with extension .mp4")
    case "AV1":
        if(pathlib.Path(output_path).suffix == ".mkv"):
            compressors.compressor_AV1(input_path, output_path)
        else:
            print("AV1 needs an output file with extension .mkv")
    case "VP9":
        if(pathlib.Path(output_path).suffix == ".webm"):
            compressors.compressor_VP9(input_path, output_path)
        else:
            print("VP9 needs an output file with extension .webm")
    case "HUFFYUV":
        if(pathlib.Path(output_path).suffix == ".avi"):
            compressors.compressor_HUFFYUV(input_path, output_path)
        else:
           print("HUFFYUV needs an output file with extension .avi")
    case "UTVIDEO":
        if(pathlib.Path(output_path).suffix == ".avi"):
            compressors.compressor_UTVIDEO(input_path, output_path)
        else:
           print("UTVIDEO needs an output file with extension .avi")
    case "FFV1":
        if(pathlib.Path(output_path).suffix == ".avi"):
            compressors.compressor_FFV1(input_path, output_path)
        else:
           print("FFV1 needs an output file with extension .avi")
    case "HEVC-VS":
        if(pathlib.Path(output_path).suffix == ".mp4"):
            compressors.compressor_HEVCVS(input_path, output_path)
        else:
           print("HEVC-VS needs an output file with extension .mp4")
    case "AV1-VS":
        if(pathlib.Path(output_path).suffix == ".mkv"):
            compressors.compressor_AV1VS(input_path, output_path)
        else:
            print("AV1-VS needs an output file with extension .mkv")
    case "VP9-VS":
        if(pathlib.Path(output_path).suffix == ".webm"):
            compressors.compressor_VP9VS(input_path, output_path)
        else:
            print("VP9-VS needs an output file with extension .webm")