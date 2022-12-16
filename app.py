import streamlit as st
import pandas as pd
import requests
import glob

video_df = pd.read_csv("videos_ids.csv")

INDEX_ID = "639b539f15a11e95e8482853"


def search_with_query(query, search_type):
    API_URL = "https://api.twelvelabs.io/v1"
    API_KEY = st.secrets.tl_key
    SEARCH_URL = f"{API_URL}/search"

    headers = {
        "x-api-key": API_KEY
    }

    data = {
        "query": query,
        "index_id": INDEX_ID,
        "search_options": [search_type],
    }
    response = requests.post(SEARCH_URL, headers=headers, json=data)

    return response.json()


# generate video link and display

# Create Web App Interface
# add tabs for each topic analysis on each api
# clean twelve labs search api

st.title("Topic Analysis using Popular Video Search APIs")

col1, col2, col3 = st.columns(3)

with col1:
    # squid games
    st.header("Squid Games")
    st.video("https://www.youtube.com/watch?v=0e3GPea1Tyg")
with col2:
    # red circle
    st.header("Circle Game")
    st.video("https://www.youtube.com/watch?v=zxYjTTXc-J8")
with col3:
    st.header("Buried Alive")
    st.video("https://www.youtube.com/watch?v=9bqk6ZUsKyA")

tab1, tab2, tab3 = st.tabs(["Twelve Labs + BERTopic", "Symbl AI", "Microsoft Azure Video Indexer"])

with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write(video_df[video_df.filename == "squid_games.mp4"].topics[0])
    with c2:
        st.write(video_df[video_df.filename == "red_circle.mp4"].topics[2])
    with c3:
        st.write(video_df[video_df.filename == "buried_alive.mp4"].topics[1])

with tab2:
    c4, c5, c6 = st.columns(3)
    with c4:
        st.write(video_df[video_df.filename == "squid_games.mp4"].symbl_topics[0])
    with c5:
        st.write(video_df[video_df.filename == "red_circle.mp4"].symbl_topics[2])
    with c6:
        st.write(video_df[video_df.filename == "buried_alive.mp4"].symbl_topics[1])

with tab3:
    c7, c8, c9 = st.columns(3)
    with c7:
        st.write(video_df[video_df.filename == "squid_games.mp4"].azure_topics[0])
    with c8:
        st.write(video_df[video_df.filename == "red_circle.mp4"].azure_topics[2])
    with c9:
        st.write(video_df[video_df.filename == "buried_alive.mp4"].azure_topics[1])


# Select video from dropdown for search
#opt = st.selectbox("Pick a video", ["squid_games.mp4", "red_circle.mp4"])

# report topics per video

# given query, return top three videos that match back


def video_id_to_url(video_id):
    url = video_df[video_df.video_id == video_id].urls.tolist()[0]
    return url

def video_from_search_result(result):
    # given search result, returns video id and start time
    vid = result["video_id"]
    start_time = result["start"]
    return vid, start_time

def filename_to_video_id(filename):
    video_df = pd.read_csv("videos_ids.csv")
    return video_df[video_df.filename == filename].reset_index(drop=True).video_id.tolist()[0]

st.header("Search with Twelve Labs!")


query = st.text_input(label = "Pass Query Here", value = "")
search_option = st.selectbox(label = "Select a type of search here", options=("visual", "conversation"))

if query != "":
    search_results = search_with_query(query=query,
    search_type = search_option)

    results_data = search_results["data"]

    v1, v2, v3 = st.columns(3)

    # for each video, return the highest ranking video and start at timestamp
    st.write()

    # squid games
    st.header("Best Squid Games result")
    sg = list(filter(lambda x: x["video_id"] == filename_to_video_id("squid_games.mp4"), results_data))
    if len(sg) > 0:
        sg_first = sg[0]
        v1_val, v1_startime = video_from_search_result(sg_first)
        v1_url = video_id_to_url(v1_val)
        st.video(data = v1_url, start_time = int(v1_startime))
        st.write(sg)
    else:
        st.write("No results found")

    
    # red circle
    st.header("Best Circle Game result")
    v2id = filename_to_video_id("red_circle.mp4")
    rc = list(filter(lambda x: x["video_id"] == v2id, results_data))
    if len(rc) > 0:
        rc_first = rc[0]
        v2_val, v2_startime = video_from_search_result(rc_first)
        v2_url = video_id_to_url(v2_val)
        st.video(data = v2_url, start_time = int(v2_startime))
        st.write(rc)
    else:
        st.write("No results found")

    # buried alive
    st.header("Best Buried Alive Result")
    ba = list(filter(lambda x: x["video_id"] == filename_to_video_id("buried_alive.mp4"), results_data))
    if len(ba) > 0:
        ba_first = ba[0]
        v3_val, v3_startime = video_from_search_result(ba_first)
        v3_url = video_id_to_url(v3_val)
        st.video(data = v3_url, start_time = int(v3_startime))
        st.write(ba)
    else:
        st.write("No results found")
    # then, just print the results for that video underneath as well




