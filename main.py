# # Libraries
# import streamlit as st
# import pandas as pd
# import joblib
# import psycopg2
# from psycopg2 import Error
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
# import config 
# from supabase import create_client, Client

# # Load the pkl files
# scaler = joblib.load('scaler.pkl')
# le_status = joblib.load('le_status.pkl')
# ohe = joblib.load('ohe.pkl')
# modela = joblib.load('final_model.pkl')
# feature_order = joblib.load('feature_order.pkl')

# # PostgreSQL connection
# def create_connection():
#     connection = None
#     try:
#         connection = psycopg2.connect(
#             # host=config.POSTGRES_HOST,
#             # user=config.POSTGRES_USER,
#             # password=config.POSTGRES_PASSWORD,
#             # database=config.POSTGRES_DB  
#             # host=st.secrets["POSTGRES_HOST"],
#             # user=st.secrets["POSTGRES_USER"],
#             # password=st.secrets["POSTGRES_PASSWORD"],
#             # database=st.secrets["POSTGRES_DB"]
#             host=st.secrets["connections"]["postgresql"]["host"],
#             user=st.secrets["connections"]["postgresql"]["username"],
#             password=st.secrets["connections"]["postgresql"]["password"],
#             database=st.secrets["connections"]["postgresql"]["database"]
#         )
#         st.write("Koneksi ke PostgreSQL berhasil")
#     except (Exception, psycopg2.Error) as error:
#         st.write(f"Error saat terhubung ke database: {error}")

#     return connection

# def insert_prediction(data):
#     connection = create_connection()
#     if connection is not None:
#         cursor = connection.cursor()
#         insert_query = """
#             INSERT INTO public.prediction_history 
#             ("DURATIONS_PERPROJECT", "TOTAL_PROJECT", "STATUS", "LAMA_KERJA", "DIVISI", "GOL", "Predicted_LEVEL_KEAHLIAN", "Revisian_LEVEL_KEAHLIAN")
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(insert_query, data)
#         connection.commit()
#         st.write("Data berhasil disimpan ke database PostgreSQL")
#         cursor.close()
#         connection.close()
#     else:
#         st.write("Gagal terhubung ke database PostgreSQL. Periksa 'secrets.toml'.")

# # Streamlit UI
# st.title("Model Prediksi Level Keahlian")

# # Input form for new data
# total_project = st.number_input('Kemampuan Menyelesaikan Project [jumlah]')
# durations_perproject = st.number_input('Kemampuan Waktu Pengerjaan Tiap Project [hour]')
# status = st.selectbox('Status Kerja', le_status.classes_)
# lama_kerja = st.number_input('Lama Kerja [year]')
# divisi = st.selectbox('Divisi Impian', ohe.categories_[0])
# gol = st.selectbox('Target Gol', ohe.categories_[1])
# revisian = st.selectbox('Level Keahlian yang Seharusnya', [
#     'Pelaksana Madya', 'Pelaksana Pemula', 'Pelaksana Utama',
#     'Perekayasa Madya', 'Perekayasa Magang', 'Perekayasa Muda',
#     'Perekayasa Utama', 'Pimpinan Madya', 'Pimpinan Muda',
#     'Pimpinan Pemula', 'Pimpinan Utama'])

# # Condition for button
# if st.button('Prediksi'):
#     # Preprocess the new input data
#     new_data = pd.DataFrame({
#         'DURATIONS_PERPROJECT': [durations_perproject],
#         'TOTAL_PROJECT': [total_project],
#         'STATUS': [status],
#         'LAMA_KERJA': [lama_kerja],
#         'DIVISI': [divisi],
#         'GOL': [gol]
#     })

#     data_simpan = new_data.copy()

#     # Transforming data
#     new_data['STATUSenc'] = le_status.transform(new_data['STATUS'])
#     encoded_features_new = ohe.transform(new_data[['DIVISI', 'GOL']])
#     encoded_df_new = pd.DataFrame(encoded_features_new, columns=ohe.get_feature_names_out(['DIVISI', 'GOL']))
#     new_data = pd.concat([new_data, encoded_df_new], axis=1)
#     new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']] = scaler.transform(new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']])

#     # Ensure the input data follows the correct order
#     X_new = new_data.reindex(columns=feature_order)

#     # Prediction
#     prediction = modela.predict(X_new)
#     st.write(f'Hasil Prediksi: {prediction[0]}')

#     # Add the revisian column
#     data_simpan['Predicted_LEVEL_KEAHLIAN'] = prediction[0]
#     data_simpan['Revisian_LEVEL_KEAHLIAN'] = revisian

#     # Save input and prediction to PostgreSQL
#     insert_prediction(tuple(data_simpan.values.flatten()))



# # Load the pkl files
# scaler = joblib.load('scaler.pkl')
# le_status = joblib.load('le_status.pkl')
# ohe = joblib.load('ohe.pkl')
# modela = joblib.load('final_model.pkl')
# feature_order = joblib.load('feature_order.pkl')

# # Supabase connection
# SUPABASE_URL = st.secrets["supabase"]["url"]
# SUPABASE_KEY = st.secrets["supabase"]["key"]
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# def insert_prediction(data):
#     try:
#         response = supabase.table("prediction_history").insert(data).execute()
#         if response.status_code == 201:
#             st.write("Data berhasil disimpan ke database Supabase")
#         else:
#             st.write(f"Error saat menyimpan data: {response}")
#     except Exception as e:
#         st.write(f"Error saat terhubung ke Supabase: {e}")

# # Streamlit UI
# st.title("Model Prediksi Level Keahlian")

# # Input form for new data
# total_project = st.number_input('Kemampuan Menyelesaikan Project [jumlah]')
# durations_perproject = st.number_input('Kemampuan Waktu Pengerjaan Tiap Project [hour]')
# status = st.selectbox('Status Kerja', le_status.classes_)
# lama_kerja = st.number_input('Lama Kerja [year]')
# divisi = st.selectbox('Divisi Impian', ohe.categories_[0])
# gol = st.selectbox('Target Gol', ohe.categories_[1])
# revisian = st.selectbox('Level Keahlian yang Seharusnya', [
#     'Pelaksana Madya', 'Pelaksana Pemula', 'Pelaksana Utama',
#     'Perekayasa Madya', 'Perekayasa Magang', 'Perekayasa Muda',
#     'Perekayasa Utama', 'Pimpinan Madya', 'Pimpinan Muda',
#     'Pimpinan Pemula', 'Pimpinan Utama'])

# # Condition for button
# if st.button('Prediksi'):
#     # Preprocess the new input data
#     new_data = pd.DataFrame({
#         'DURATIONS_PERPROJECT': [durations_perproject],
#         'TOTAL_PROJECT': [total_project],
#         'STATUS': [status],
#         'LAMA_KERJA': [lama_kerja],
#         'DIVISI': [divisi],
#         'GOL': [gol]
#     })

#     data_simpan = new_data.copy()

#     # Transforming data
#     new_data['STATUSenc'] = le_status.transform(new_data['STATUS'])
#     encoded_features_new = ohe.transform(new_data[['DIVISI', 'GOL']])
#     encoded_df_new = pd.DataFrame(encoded_features_new, columns=ohe.get_feature_names_out(['DIVISI', 'GOL']))
#     new_data = pd.concat([new_data, encoded_df_new], axis=1)
#     new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']] = scaler.transform(new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']])

#     # Ensure the input data follows the correct order
#     X_new = new_data.reindex(columns=feature_order)

#     # Prediction
#     prediction = modela.predict(X_new)
#     st.write(f'Hasil Prediksi: {prediction[0]}')

#     # Add the revisian column
#     data_simpan['Predicted_LEVEL_KEAHLIAN'] = prediction[0]
#     data_simpan['Revisian_LEVEL_KEAHLIAN'] = revisian

#     # Prepare data for Supabase
#     data_simpan_dict = data_simpan.to_dict(orient='records')[0]

#     # Save input and prediction to Supabase
#     insert_prediction(data_simpan_dict)

# # Libraries
# import streamlit as st
# import pandas as pd
# import joblib
# from supabase import create_client, Client
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

# # Load the pkl files
# scaler = joblib.load('scaler.pkl')
# le_status = joblib.load('le_status.pkl')
# ohe = joblib.load('ohe.pkl')
# modela = joblib.load('final_model.pkl')
# feature_order = joblib.load('feature_order.pkl')

# # Accessing the Supabase URL and Key from Streamlit secrets
# SUPABASE_URL = st.secrets["supabase"]["url"]
# SUPABASE_KEY = st.secrets["supabase"]["key"]

# # Initialize the Supabase client
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # Function to insert prediction into Supabase
# def insert_prediction(data):
#     try:
#         response = supabase.table("prediction_history").insert(data).execute()
#         if response.status_code == 201:
#             st.write("Data berhasil disimpan ke database Supabase")
#         else:
#             st.write(f"Error saat menyimpan data: {response}")
#     except Exception as e:
#         st.write(f"Error saat terhubung ke Supabase: {e}")

# # Streamlit UI
# st.title("Model Prediksi Level Keahlian")

# # Input form for new data
# total_project = st.number_input('Kemampuan Menyelesaikan Project [jumlah]')
# durations_perproject = st.number_input('Kemampuan Waktu Pengerjaan Tiap Project [hour]')
# status = st.selectbox('Status Kerja', le_status.classes_)
# lama_kerja = st.number_input('Lama Kerja [year]')
# divisi = st.selectbox('Divisi Impian', ohe.categories_[0])
# gol = st.selectbox('Target Gol', ohe.categories_[1])
# revisian = st.selectbox('Level Keahlian yang Seharusnya', [
#     'Pelaksana Madya', 'Pelaksana Pemula', 'Pelaksana Utama',
#     'Perekayasa Madya', 'Perekayasa Magang', 'Perekayasa Muda',
#     'Perekayasa Utama', 'Pimpinan Madya', 'Pimpinan Muda',
#     'Pimpinan Pemula', 'Pimpinan Utama'])

# # Condition for button
# if st.button('Prediksi'):
#     # Preprocess the new input data
#     new_data = pd.DataFrame({
#         'DURATIONS_PERPROJECT': [durations_perproject],
#         'TOTAL_PROJECT': [total_project],
#         'STATUS': [status],
#         'LAMA_KERJA': [lama_kerja],
#         'DIVISI': [divisi],
#         'GOL': [gol]
#     })

#     data_simpan = new_data.copy()

#     # Transforming data
#     new_data['STATUSenc'] = le_status.transform(new_data['STATUS'])
#     encoded_features_new = ohe.transform(new_data[['DIVISI', 'GOL']])
#     encoded_df_new = pd.DataFrame(encoded_features_new, columns=ohe.get_feature_names_out(['DIVISI', 'GOL']))
#     new_data = pd.concat([new_data, encoded_df_new], axis=1)
#     new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']] = scaler.transform(new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']])

#     # Ensure the input data follows the correct order
#     X_new = new_data.reindex(columns=feature_order)

#     # Prediction
#     prediction = modela.predict(X_new)
#     st.write(f'Hasil Prediksi: {prediction[0]}')

#     # Add the revisian column
#     data_simpan['Predicted_LEVEL_KEAHLIAN'] = prediction[0]
#     data_simpan['Revisian_LEVEL_KEAHLIAN'] = revisian

#     # Save input and prediction to Supabase
#     insert_prediction(data_simpan.to_dict(orient='records'))


import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from st_supabase_connection import SupabaseConnection

# Load the pkl files
scaler = joblib.load('scaler.pkl')
le_status = joblib.load('le_status.pkl')
#le_lokasi = joblib.load('le_lokasi.pkl')
ohe = joblib.load('ohe.pkl')
modela = joblib.load('final_model.pkl')
feature_order = joblib.load('feature_order.pkl')

# Initialize Supabase connection
# supabase = SupabaseConnection(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
# supabase = SupabaseConnection(
#     st.secrets["supabase"]["SUPABASE_URL"],
#     st.secrets["supabase"]["SUPABASE_KEY"]
# )

# # Initialize Supabase connection
# supabase = SupabaseConnection(connection_name="MySupabaseConnection")
# # Later in the code, when using the connection
# supabase.connect(st.secrets["supabase"]["SUPABASE_URL"], st.secrets["supabase"]["SUPABASE_KEY"])

# Initialize Supabase connection with the required parameters
supabase = SupabaseConnection(
    connection_name="MySupabaseConnection", 
    url=st.secrets["supabase"]["SUPABASE_URL"], 
    key=st.secrets["supabase"]["SUPABASE_KEY"]
)

# Streamlit UI
st.title("Model Prediksi Level Keahlian")

# Input form for new data
durations_perproject = st.number_input('Kemampuan Waktu Pengerjaan Tiap Project [hour]')
total_project = st.number_input('Kemampuan Menyelesaikan Project [jumlah]')
status = st.selectbox('Status Kerja', le_status.classes_)
lama_kerja = st.number_input('Lama Kerja [year]')
divisi = st.selectbox('Divisi Impian', ohe.categories_[0])
gol = st.selectbox('Target Gol', ohe.categories_[1])
revisian= st.selectbox('Level Keahlian yang Seharusnya', ['Pelaksana Madya', 'Pelaksana Pemula', 'Pelaksana Utama', 'Perekayasa Madya', 'Perekayasa Magang', 'Perekayasa Muda', 'Perekayasa Utama', 'Pimpinan Madya', 'Pimpinan Muda', 'Pimpinan Pemula', 'Pimpinan Utama' ])

# Condition for button
if st.button('Prediksi'):
    # Preprocess the new input data
    new_data = pd.DataFrame({
        'DURATIONS_PERPROJECT': [durations_perproject],
        'TOTAL_PROJECT': [total_project],
        'STATUS': [status],
        'LAMA_KERJA': [lama_kerja],
        'DIVISI': [divisi],
        #'LOKASI': [lokasi],
        'GOL': [gol]
    })
    
    data_simpan= new_data
    
    # Transforming data
    new_data['STATUSenc'] = le_status.transform(new_data['STATUS'])
    #new_data['LOKASIenc'] = le_lokasi.transform(new_data['LOKASI'])
    encoded_features_new = ohe.transform(new_data[['DIVISI', 'GOL']])
    encoded_df_new = pd.DataFrame(encoded_features_new, columns=ohe.get_feature_names_out(['DIVISI', 'GOL']))
    new_data = pd.concat([new_data, encoded_df_new], axis=1)
    new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']] = scaler.transform(new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']])
    
    # Unused columns
    #X_new = new_data.drop(columns=['STATUS', 'DIVISI', 'GOL'])
    # Ensure the input data follows the correct order
    X_new = new_data.reindex(columns=feature_order)
    
    # Prediction
    prediction = modela.predict(X_new)
    st.write(f'Hasil Prediksi: {prediction[0]}')
    
    # # Save prediction result with the input data to Supabase
    # data_simpan['Predicted_Keahlian'] = prediction[0]
    # data_simpan['Revisian'] = revisian
    
    # Prepare the data for saving
    data_simpan = {
        "DURATIONS_PERPROJECT": durations_perproject,
        "TOTAL_PROJECT": total_project,
        "STATUS": status,
        "lAMA KERJA": lama_kerja,
        "DIVISI": divisi,
        "GOL": gol,
        "Predicted_LEVEL_KEAHLIAN": prediction[0],
        "Revisian_LEVEL_KEAHLIAN": revisian
    }
    
    # Insert the record into Supabase table (e.g., "prediction_history")
    try:
        supabase.insert("prediction_history", data_simpan.to_dict(orient='records')[0])
        st.success("Data has been saved to Supabase.")
    except Exception as e:
        st.error(f"Error saving data to Supabase: {e}")
