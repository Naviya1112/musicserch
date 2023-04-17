import streamlit as st
import spotipy
import spotipy.oauth2 as oauth2
import lyricsgenius
import requests

# กำหนด Spotify API credentials
sp_client_id = 'd88327528b8043fd8efb87df125fbdd6'
sp_client_secret = '414eb05ea4d94249b7f418772cca0c67'
credentials = oauth2.SpotifyClientCredentials(client_id=sp_client_id, client_secret=sp_client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# กำหนด Genius API key
genius = lyricsgenius.Genius('sQAmLv1EIJebcRoj_pTbFw-v93TVWf2w20S6DIvuGGoMAkFkDR5UAb663g88mL0p')

# สร้าง streamlit app
st.title('ค้นหาชื่อเพลง')
st.write('พิมพ์เนื่อเพลงที่ต้องการค้นหา')

# รับ input จากผู้ใช้
query = st.text_input('ใส่ชื่อเพลงหรือเนื้อร้องบางส่วน')

# ค้นหาเพลงจาก Spotify ด้วยเนื้อร้องบางส่วน
def search_spotify(query):
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['total'] > 0:
        track = results['tracks']['items'][0]
        return track
    else:
        return None

# ค้นหาเนื้อเพลงจาก Genius ด้วยชื่อเพลงและศิลปิน
def search_genius(title, artist):
    song = genius.search_song(title, artist)
    return song

# แสดงผลการค้นหา
if st.button('ค้นหา'):
    try:
        # ค้นหาเพลงจาก Spotify
        track = search_spotify(query)
        if track:
            st.write(f"**{track['name']}** by {track['artists'][0]['name']} from the album {track['album']['name']}")
            # แสดงเนื้อเพลงจาก Genius
            song = search_genius(track['name'], track['artists'][0]['name'])
            if song:
                st.write(song.lyrics)
            else:
                st.write('ไม่พบเนื้อเพลงที่ต้องการค้นหา')
        else:
            st.write('ไม่พบชื่อเพลงที่ต้องการค้นหา')
    except requests.exceptions.HTTPError as e:
        st.warning(f"An HTTP error occurred: {e}")
    except requests.exceptions.Timeout as e:
        st.warning(f"The request timed out: {e}")
    except requests.exceptions.RequestException as e:
        st.warning
