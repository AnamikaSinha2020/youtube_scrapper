from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from db_connection import cursor, mydb
# from bs4 import BeautifulSoup as bs
# from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")



@app.route('/get_videos',methods=['POST'])  # route to display the home page
@cross_origin()
def get():
    channel_id = request.form['channel_id']
    print("channel_id ==", channel_id)
    # query =f"Select * from YTscraper.Video_tbl where channel_id = '{channel_id}' order by Video_upload_date desc limit 50;"
    query =f"""select vdeo.video_id, vdeo.Channel_id, chnl.Channel_name, vdeo.Video_title, 
    vdeo.Videao_link, vdeo.Video_disc, vdeo.Thumb_nail, vdeo.Likes, vdeo.Video_url, 
    vdeo.Video_upload_date from YTscraper.Video_tbl vdeo
    left join YTscraper.Channel_tble chnl on chnl.channel_id = vdeo.Channel_id
    where vdeo.channel_id = '{channel_id}';"""
    cursor.execute(query)
    response_data = []

    myresult = cursor.fetchall()
    for data in myresult:
        data_dict = {}
        print(data)
        data_dict['video_id'] = data[0]
        data_dict['Channel_id'] = data[1]
        data_dict['Channel_name'] = data[2]
        data_dict['Video_title'] = data[3]
        data_dict['Videao_link'] = data[4]
        data_dict['Video_disc'] = data[5]
        data_dict['Thumb_nail'] = data[6]
        data_dict['Likes'] = data[7]
        data_dict['Video_url'] = data[8]
        data_dict['Video_upload_date'] = data[9]
        # data_dict['Commentor_name'] = data[10]
        # data_dict['Comments'] = data[11]

        response_data.append(data_dict)
    print(response_data)
    return render_template("get_videos.html", response_data=response_data)


@app.route('/get_comments/<video_id>',methods=['POST'])  # route to display the home page
@cross_origin()
def get_cmnt(video_id):
    query = f'select * from YTscraper.Commenter_tbl where video_id ={video_id};'
    cursor.execute(query)
    response_data = []

    myresult = cursor.fetchall()
    for data in myresult:
        dict_comment = {}
        dict_comment['video_id'] = data[0]
        dict_comment['Commentor_name'] = data[1]
        dict_comment['Comments'] = data[2]
        dict_comment['video_title'] = data[3]
        response_data.append(dict_comment)


    return render_template("index.html", response_data=response_data)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
	# app.run(debug=True)
