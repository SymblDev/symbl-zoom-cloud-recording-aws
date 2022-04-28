import json
import boto3
import os, sys, subprocess, shlex, re
from subprocess import call

class FFMPEG(object):
    
    """https://stackoverflow.com/questions/9896644/getting-ffprobe-information-with-python"""
    def probe_file(self, filename):
        cmnd = ['/opt/ffmpeglib/ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
        p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(filename)
        out, err =  p.communicate()
        print("==========probe_file output==========")
        print(out)
        if err:
            print("========= probe_file error ========")
            print(err)
      
    def merge_and_upload_audio(self, bucket, s3_path):
        output_file = '/tmp/output.m4a'
        
        files = os.listdir('/tmp')
        files_m4a = [i for i in files if i.endswith('.m4a')]
        
        # sort the files as we read from Zoom Rec
        files_m4a = sorted(files_m4a, key=lambda x: int(os.path.splitext(x)[0]))
        
        index = 0
        i_option = ''
        filter_complex_option = ''
        
        for audio_file in files_m4a:
            i_option = i_option + '-i /tmp/' + audio_file + ' '
            filter_complex_option = filter_complex_option + f'[{index}:a]'
            index = index + 1
        
        filter_complex_option = filter_complex_option + f'amerge=inputs={index}[a]'
        
        print('i option: '+ i_option)
        print('filter option: '+ filter_complex_option)
        
        ffmpeg_cmd = f'/opt/ffmpeglib/ffmpeg {i_option} -filter_complex "{filter_complex_option}" -map "[a]" {output_file}'
        print('ffmpeg_cmd: '+ ffmpeg_cmd)
        
        command1 = shlex.split(ffmpeg_cmd)
        print(command1)
        
        p1 = subprocess.run(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        s3 = boto3.client('s3')
        s3.upload_file(output_file, bucket, s3_path + '/output.m4a')
        print(f'merged audio file uploaded to s3')
    