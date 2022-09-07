import boto3

s3 = boto3.resource('s3',
                   aws_access_key_id='AKIA2C2WNLJEUTTGTD6H',
                   aws_secret_access_key='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')
BUCKET = "youtubevideo-anamika"

s3.Bucket(BUCKET).upload_file("/Users/manishsinha/Desktop/Avyan.jpeg", "Avyan2.jpeg")