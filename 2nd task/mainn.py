import pandas as pd
import json
from pandas import json_normalize

# ==== 1. RAW DATA LOADING ====

print("Loading raw JSON data from Excel...")

# Load raw Excel
df_raw = pd.read_excel('raw_data.xlsx')

print("Data loaded successfully.\n")

# ==== 2. JSON SPLIT AND PARSE FUNCTION ====

def split_and_parse_json(cell_value):
    try:
        # Har bir JSON objectni ajratish uchun
        # Har 2 ta JSON orasidagi '}{' ni '}\n{' ga o‘zgartirib list shaklida olish
        json_objects = cell_value.strip().replace('}{', '}|{').split('|')
        return [json.loads(obj) for obj in json_objects]
    except Exception as e:
        print(f"Error parsing JSON at cell: {e}")
        return None

# ==== 3. SPLIT ALL ROWS ====

print("Parsing JSON column...")

all_json_rows = []

for index, row in df_raw.iterrows():
    parsed_list = split_and_parse_json(row['raw_content'])
    if parsed_list:
        all_json_rows.extend(parsed_list)

print(f"Total parsed JSON rows: {len(all_json_rows)}\n")

# ==== 4. JSON NORMALIZATION ====

df_main = json_normalize(all_json_rows)

print("JSON normalization done.\n")

# ==== 5. DIMENSION TABLES CREATION ====

print("Creating dimension tables...")

# Dimension: Topic (title)
df_topic = df_main[['title']].drop_duplicates().reset_index(drop=True)
df_topic['TopicID'] = df_topic.index + 1

# Dimension: Duration
df_duration = df_main[['duration']].drop_duplicates().reset_index(drop=True)
df_duration['DurationID'] = df_duration.index + 1

# Dimension: Audio (audio_url)
df_audio = df_main[['audio_url']].drop_duplicates().reset_index(drop=True)
df_audio['AudioID'] = df_audio.index + 1

# Dimension: Speaker
# Explode speakers array
df_speakers_list = df_main[['id', 'speakers']].explode('speakers').reset_index(drop=True)
df_speakers_list['speaker_name'] = df_speakers_list['speakers'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
df_speakers_list = df_speakers_list[['id', 'speaker_name']]

df_speaker = df_speakers_list[['speaker_name']].drop_duplicates().reset_index(drop=True)
df_speaker['SpeakerID'] = df_speaker.index + 1

print("Dimension tables created.\n")

# ==== 6. FACT TABLES ====

print("Creating fact table...")

# Fact Meeting table
fact_meeting = df_main[['id', 'title', 'duration', 'audio_url']].copy()

fact_meeting = fact_meeting.merge(df_topic, on='title', how='left')
fact_meeting = fact_meeting.merge(df_duration, on='duration', how='left')
fact_meeting = fact_meeting.merge(df_audio, on='audio_url', how='left')

fact_meeting_final = fact_meeting[['id', 'TopicID', 'DurationID', 'AudioID']]

# Fact_Speaker_Meeting (Many-to-Many)
fact_speaker_meeting = df_speakers_list.merge(df_speaker, on='speaker_name', how='left')
fact_speaker_meeting = fact_speaker_meeting[['id', 'SpeakerID']]

print("Fact tables created.\n")

# ==== 7. EXPORT TO EXCEL ====

print("Exporting to Excel...")

output_filename = 'star_schema_json_output.xlsx'

with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
    df_topic.to_excel(writer, sheet_name='dim_topic', index=False)
    df_duration.to_excel(writer, sheet_name='dim_duration', index=False)
    df_audio.to_excel(writer, sheet_name='dim_audio', index=False)
    df_speaker.to_excel(writer, sheet_name='dim_speaker', index=False)
    fact_meeting_final.to_excel(writer, sheet_name='fact_meeting', index=False)
    fact_speaker_meeting.to_excel(writer, sheet_name='fact_speaker_meeting', index=False)

print(f"Export completed! Output saved as: {output_filename}\n")

print("✅ JSON Star Schema ETL Process finished successfully!")
