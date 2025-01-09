import streamlit as st
import sounddevice as sd
import numpy as np
import pandas as pd
import wave
import os
import time
import base64
from datetime import datetime
import zipfile

    
def get_base64_of_image(image_path):
    absolute_path = os.path.join(os.getcwd(), image_path)
    with open(absolute_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

image_base64 = get_base64_of_image("background/voice_background.jpeg")


background_css = f'''
<style>
.stApp {{
    background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.4)), url("data:image/jpeg;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    animation: fadeIn 3s ease-in-out, scaleUp 3s ease-in-out;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

@keyframes scaleUp {{
    from {{ transform: scale(1.1); }}
    to {{ transform: scale(1); }}
}}
</style>
'''

st.markdown(background_css, unsafe_allow_html=True)


def record_audio(duration):
    st.write("Voice Recording started...")
    recording = sd.rec(int(duration * 44100), samplerate=44100, channels=2, dtype='float64')
    return recording



def stop_audio():
    sd.stop()



def save_audio(filename, data):
    wav_file = filename + ".wav"
    wf = wave.open(wav_file, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(b''.join(np.int16(data * 32767)))
    wf.close()
    
    return wav_file



def save_to_csv(name,gender, filepath, created_by, language, user_type):
    data = {"Name": [name], "Gender" : [gender], "File_Path": [filepath], "CreatedBy": [created_by], "Language": [language], "User_Type" : [user_type]} 
    df = pd.DataFrame(data)

    if not os.path.isfile('Voice_Records.csv'):
        df.to_csv('Voice_Records.csv', index=False)
    else:
        df.to_csv('Voice_Records.csv', mode='a', header=False, index=False)



def check_existing_record(name,gender ,created_by, language):
    if os.path.isfile('Voice_Records.csv'):
        df = pd.read_csv('Voice_Records.csv')
        filtered_df = df[(df['Name'] == name) & (df['Gender'] == gender) & (df['CreatedBy'] == created_by) & (df['Language'] == language)]
        return not filtered_df.empty
    return False



def record_page():
    st.markdown(
        """
        <style>
        .big-title {
            font-size: 70px;
            font-weight: bold;
            text-align: center; 
            font-family: 'Brush Script MT'; 
            background: linear-gradient(90deg, #FF5733, #FFC300, #DAF7A6); 
            color: transparent;
            -webkit-background-clip: text; 
            background-clip: text;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="big-title">Voice Recording Application</h1>', unsafe_allow_html=True)

    creators_list =  ["Select"] + ["Ahmet Yasin Aydın", "Ramazan Tetik", "Dilan Nihadioğlu", "Gökhan Ergül", "Ahmet Muhammed Aydın", 
                     "Burak Cankurt", "Azime Şimşek", "Esra Aydın", "Sadık Can Barut", "Ali Kaynakçı", "Other"]
    language_list = ["Select", "Turkish", "English"]

    created_by = st.selectbox("Recording person:", creators_list)
    if created_by == "Other":
        other_person = st.text_input("Please Enter Your Name: ")
    
    genders = ["Select"] + ["Male" , "Female"]
    user_gender = st.selectbox("Select Your Gender : " , genders)
    language = st.selectbox("Select Language:", language_list)
    word = st.text_input("Enter the word:")
    name = word.strip()
    
    user_type = "Other" if created_by == "Other" else "Team Member"
    created_by = other_person  if created_by == "Other" else created_by

    if not created_by or created_by == "Select":
        st.warning("Please select the person making the recording.")
        return
    

    if not language or language == "Select":
        st.warning("Please select the language for the recording.")
        return

    if not name:
        st.warning("Please enter the word to be recorded.")
        return

    max_duration = 5
    st.info("Maximum duration is **5 seconds**.")
                
    if 'recording' not in st.session_state:
        st.session_state['recording'] = False
        st.session_state['start_time'] = None
        st.session_state['stop_requested'] = False
        st.session_state['refresh_allowed'] = True 

    if st.button("Start recording") and not st.session_state['recording']:
        if check_existing_record(name,user_gender ,created_by, language):
            st.warning(f"The record for **{name}** by **{created_by}** in **{language}** already exists.")
        else:
            st.session_state['recording'] = True
            st.session_state['start_time'] = time.time()
            st.session_state['stop_requested'] = False
            st.session_state['refresh_allowed'] = True 
            st.session_state['recorded_data'] = record_audio(max_duration)


    if st.session_state['recording']:
        elapsed_time = time.time() - st.session_state['start_time']
        remaining_time = max(0, max_duration - elapsed_time)

        st.warning(f"Recording in progress... Remaining time: {int(remaining_time)} seconds")

        if st.button("Stop recording"):
            st.session_state['stop_requested'] = True
            stop_audio()
            st.session_state['recording'] = False
            recorded_data = st.session_state['recorded_data'][:int(elapsed_time * 44100)]

            if not os.path.exists('Voice_Records'):
                os.makedirs('Voice_Records')
            current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = os.path.join('Voice_Records', f"{name}_{current_date}_audio")
            mp3_filepath = save_audio(filepath, recorded_data)
            
            save_to_csv(name, user_gender , mp3_filepath, created_by, language, user_type)
            st.success(f"Recording saved successfully as {mp3_filepath}")
            st.session_state['refresh_allowed'] = False 

        if remaining_time <= 0 and not st.session_state['stop_requested']:
            stop_audio()
            st.session_state['recording'] = False
            st.warning("Time is up! The recording was stopped automatically and was not saved.")
            st.session_state['refresh_allowed'] = False 
        
        if st.session_state['refresh_allowed'] and elapsed_time < 5 :
            time.sleep(1)
            st.rerun()
      
     
           

def delete_record(file_path, df, index):
    try:
    
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success(f"**{file_path}** was deleted successfully.")
        else:
            st.warning(f"{file_path} not found.")

        df.drop(index, inplace=True)
        df.to_csv('Voice_Records.csv', index=False)
        st.rerun()

    except PermissionError:
        st.error(f"PermissionError: {file_path} is in use by another process.")



def playback_page():
    st.markdown(
        """
        <style>
        .big-title {
            font-size: 70px;
            font-weight: bold;
            text-align: center; 
            font-family: 'Brush Script MT'; 
            background: linear-gradient(90deg, #FF5733, #FFC300, #DAF7A6); 
            color: transparent;
            -webkit-background-clip: text; 
            background-clip: text;
        }

        .download-button {
            display: inline-block;
            padding: 10px 20px;
            margin: 20px 0;
            color: #fff; 
            border: none;
            border-radius: 15px; 
            text-align: center;
            text-decoration: none;
            font-size: 16px; 
            font-weight: bold; 
        }
        .download-button:hover {
            background-color: transparent;
            color: #fff;
            border: 2px solid #5DADE2; 
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="big-title">Voice Recording Application</h1>', unsafe_allow_html=True)

    creators_list_playback =  ["Select"] + ["Ahmet Yasin Aydın", "Ramazan Tetik", "Dilan Nihadioğlu", 
                          "Gökhan Ergül", "Ahmet Muhammed Aydın",
                          "Burak Cankurt", "Azime Şimşek", "Esra Aydın", 
                          "Sadık Can Barut", "Ali Kaynakçı", "Other"]

    language_list_playback =  ["Select", "Turkish", "English"]

    creator_playback = st.selectbox("Select A Person:", creators_list_playback, key="creator_playback")
    if creator_playback == "Other":
        other = st.text_input("Please Enter Your Name :")
        creator_playback = other
    language_playback = st.selectbox("Select Language:", language_list_playback, key="language_playback")

    if creator_playback != "Select" and language_playback != "Select":
        if os.path.isfile('Voice_Records.csv'):
            df = pd.read_csv('Voice_Records.csv', sep=',')
            filtered_df = df[(df['CreatedBy'] == creator_playback) & (df['Language'] == language_playback)]

            if not filtered_df.empty:
                with zipfile.ZipFile('filtered_records.zip', 'w') as zf:
                    filtered_df.to_csv('filtered_records.csv', index=False)
                    zf.write('filtered_records.csv')

                    for index, row in filtered_df.iterrows():
                        audio_file_path = row['File_Path']
                        zf.write(audio_file_path, os.path.join('Voice_Records', os.path.basename(audio_file_path)))

                with open('filtered_records.zip', 'rb') as f:
                    st.markdown(
                        f'<a href="data:application/zip;base64,{base64.b64encode(f.read()).decode()}" '
                        f'download="filtered_records.zip" class="download-button">Download Filtered Records</a>',
                        unsafe_allow_html=True
                    )
                    
                st.write(f"### **RECORDED BY:** {creator_playback.upper()}")
                st.write(f"### **USER TYPE:** {filtered_df.iloc[0]['User_Type'].upper()}")

                for index, row in filtered_df.iterrows():
                    st.write(f"**Word:** {row['Name']}")

                    if os.path.exists(row['File_Path']):
                        with open(row['File_Path'], 'rb') as audio_file:
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format='audio/wav')
                        st.write(f"**Language:** {row['Language']}")
                        timestamp = os.path.getmtime(row['File_Path'])
                        registration_date = datetime.fromtimestamp(timestamp).strftime('%m/%d/%Y %H:%M')
                        st.write(f"**Registration Date:** {registration_date}")
                    else:
                        st.warning(f"File not found: {row['File_Path']}")

                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        if st.button(f"Delete Record: {row['Name']}", key=f"delete_{index}"):
                            delete_record(row['File_Path'], df, index)

                    with col2:
                        if st.button(f"Edit Record: {row['Name']}", key=f"edit_{index}"):
                            st.session_state[f"editing_{index}"] = True

                    if st.session_state.get(f"editing_{index}", False):
                        new_name = st.text_input(f"Update Name for {row['Name']}", value=row['Name'], key=f"new_name_{index}")
                        current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
                        new_filepath = os.path.join('Voice_Records', f"{new_name}_{current_date}_audio")
                        new_language = st.selectbox("Update  Language:", language_list_playback, key="language_update")

                        col3, col4 = st.columns([1, 1])
                        with col3:
                            if st.button(f"Update: {row['Name']}", key=f"update_{index}"):
                                old_filepath = row['File_Path']  
                                new_filepath = os.path.join('Voice_Records', f"{new_name}_{current_date}_audio.wav")  
                                try:
                                    os.rename(old_filepath, new_filepath)
                                    df.at[index, 'Name'] = new_name
                                    df.at[index, 'File_Path'] = new_filepath
                                    df.at[index, 'Language'] = new_language if new_language != "Select" else row["Language"]
                                    df.to_csv('Voice_Records.csv', index=False)
                                    st.session_state[f"editing_{index}"] = False
                                    st.success(f"Record {new_name} updated successfully.")
                                    st.rerun()
                                except FileNotFoundError:
                                    st.error(f"File not found: {old_filepath}")
                                except Exception as e:
                                    st.error(f"An error occurred: {e}")              

                        with col4:
                            if st.button(f"Cancel: {row['Name']}", key=f"cancel_{index}"):
                                st.session_state[f"editing_{index}"] = False
                                st.rerun()

                    st.write("---")
            else:
                st.warning(f"There is no recording in **{language_playback}** saved by **{creator_playback}**.")
        else:
            st.warning("Record file not found.")




def check_existing_words_in_sentence(sentence, creator, language):
    words = sentence.split() 
    if os.path.isfile('Voice_Records.csv'):
        df = pd.read_csv('Voice_Records.csv')
        filtered_df = df[(df['CreatedBy'] == creator) & (df['Language'] == language)]
        missing_words = []
        existing_audio_files = []

        for word in words:
            word_row = filtered_df[filtered_df['Name'].str.lower() == word.lower()]
            if not word_row.empty:
                audio_file_path = word_row.iloc[0]['File_Path']
                existing_audio_files.append(audio_file_path)
            else:
                missing_words.append(word)
                
        return missing_words, existing_audio_files

    else:
        st.warning("No recordings file found.")
        return words, []  



def sentence_check_page():
    st.markdown(
        """
        <style>
        .big-title {
            font-size: 70px;
            font-weight: bold;
            text-align: center; 
            font-family: 'Brush Script MT'; 
            background: linear-gradient(90deg, #FF5733, #FFC300, #DAF7A6); 
            color: transparent;
            -webkit-background-clip: text; 
            background-clip: text;
        }
        .download-button {
            display: inline-block;
            padding: 10px 20px;
            margin: 20px 0;
            color: #fff; 
            border: none;
            border-radius: 15px; 
            text-align: center;
            text-decoration: none;
            font-size: 16px; 
            font-weight: bold;
        }
        .download-button:hover {
            background-color: transparent;
            color: #fff;
            border: 2px solid #5DADE2; 
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="big-title">Separate Sentence</h1>', unsafe_allow_html=True)

    creators_list = ["Select"] + [
        "Ahmet Yasin Aydın", "Ramazan Tetik", "Dilan Nihadioğlu", "Gökhan Ergül", 
        "Ahmet Muhammed Aydın", "Nihat Kepkan", "Burak Cankurt", 
        "Azime Şimşek", "Esra Aydın", "Sadık Can Barut", "Ali Kaynakçı"
    ]
    language_list = ["Select", "Turkish", "English"]


    creator = st.selectbox("Select Creator:", creators_list, key="sentence_creator")
    language = st.selectbox("Select Language:", language_list, key="sentence_language")

    if creator != "Select" and language != "Select":
        sentence = st.text_input("Enter a sentence:")

        if sentence:

            words_in_sentence = sentence.split()
            
            missing_words, existing_audio_files = check_existing_words_in_sentence(sentence, creator, language)
            if missing_words:
                st.warning(f"No record was created by **{creator}** for the following words in **{language}**: {', '.join(missing_words)}")
            
      
            if existing_audio_files:
                st.success("The following words are found and playable:")
                for i, audio_file in enumerate(existing_audio_files):
                    word = words_in_sentence[i]
                    st.markdown(f"- **{word}**")
                    if st.button(f"Play '{word}'", key=f"play_{word}"):
                        with open(audio_file, 'rb') as f:
                            audio_bytes = f.read()
                            st.audio(audio_bytes, format='audio/wav')
            else:
                st.error("No words were found in the database.")
    else:
        st.info("Please select both a creator and a language.")


tab1, tab2, tab3 = st.tabs(["Record Audio", "Listen to Audio Recordings", "Separate Sentence"])


with tab1:
    record_page()

with tab2:
    playback_page()
    
with tab3:
    sentence_check_page()