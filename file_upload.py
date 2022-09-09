import boto3
from pytube import YouTube as yt_youtube

s3 = boto3.resource('s3',
                   aws_access_key_id='AKIA2C2WNLJEUTTGTD6H',
                   aws_secret_access_key='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')
BUCKET = "youtubevideo-anamika"

# s3.Bucket(BUCKET).upload_file("/Users/manishsinha/Desktop/Avyan.jpeg", "Avyan2.jpeg")


def download_upload_video(link, s3, BUCKET):
    yt = YouTube(link)
    file_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    file_name1 = file_path.replace(' ', '')
    file_name = file_name1.split('/')[-1]
    s3_url = f'https://youtubevideo-anamika.s3.amazonaws.com/{file_name}'
    s3.Bucket(BUCKET).upload_file(file_path, file_name)
    if os.path.isfile(file_path):
      os.remove(file_path)
      print("File has been deleted")
    else:
      print("File does not exist")
    return s3_url



# https://youtubevideo-anamika.s3.amazonaws.com/ANACONDATutorialforPythonHowtoInstallAnacondaonMacOSandHowtouseAnacondaforPython.mp4