# import streamlit as st
# import pandas as pd
# import joblib
# import psycopg2
# from psycopg2 import Error
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
# import config  # Assuming you have a config.py file


# # PostgreSQL connection
# def create_connection():
#     connection = None
#     try:
#         connection = psycopg2.connect(
#             host=config.POSTGRES_HOST,
#             user=config.POSTGRES_USER,
#             password=config.POSTGRES_PASSWORD,
#             database=config.POSTGRES_DB 
#             )
#         st.write("Koneksi ke PostgreSQL berhasil")
#     except (Exception, psycopg2.Error) as error:
#         st.write(f"Error saat terhubung ke database: {error}")

#     return connection

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
#             host=config.POSTGRES_HOST,
#             user=config.POSTGRES_USER,
#             password=config.POSTGRES_PASSWORD,
#             database=config.POSTGRES_DB
#         )
#         st.write("Koneksi ke PostgreSQL berhasil")
#     except Error as e:
#         st.write(f"Error: '{e}'")

#     return connection

# def insert_prediction(connection, data):
#     cursor = connection.cursor()
#     insert_query = """
#     INSERT INTO public.prediction_history 
#     ("DURATIONS_PERPROJECT", "TOTAL_PROJECT", "STATUS", "LAMA_KERJA", "DIVISI", "GOL", "Predicted_LEVEL_KEAHLIAN", "Revisian_LEVEL_KEAHLIAN")
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     cursor.execute(insert_query, data)
#     connection.commit()
#     cursor.close()


# # Streamlit UI
# st.title("Model Prediksi Level Keahlian")

# # Input form for new data
# durations_perproject = st.number_input('Kemampuan Waktu Pengerjaan Tiap Project [hour]')
# total_project = st.number_input('Kemampuan Menyelesaikan Project [jumlah]')
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
#     connection = create_connection()
    
#     # Save input and prediction to PostgreSQL (using st.connection)
#     connection = st.connection("postgresql", type= "sql")

#     if connection is not None:
#         # Data to be inserted
#         data_tuple = tuple(data_simpan.values.flatten())
#         try:
#             insert_prediction(connection, data_tuple)
#             st.write("Data berhasil disimpan ke database PostgreSQL")
#         except Exception as e:
#             st.write(f"Error: {e}")
#         finally:
#             connection.close()
#     else:
#         st.write("Gagal terhubung ke database PostgreSQL. Periksa 'secrets.toml'.")


import streamlit as st
import pandas as pd
import joblib
import psycopg2
from psycopg2 import Error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import config 

# Load the pkl files
scaler = joblib.load('scaler.pkl')
le_status = joblib.load('le_status.pkl')
ohe = joblib.load('ohe.pkl')
modela = joblib.load('final_model.pkl')
feature_order = joblib.load('feature_order.pkl')

# PostgreSQL connection
def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host=config.POSTGRES_HOST,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            database=config.POSTGRES_DB
        )
        st.write("Koneksi ke PostgreSQL berhasil")
    except (Exception, psycopg2.Error) as error:
        st.write(f"Error saat terhubung ke database: {error}")

    return connection

def insert_prediction(data):
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO public.prediction_history 
            ("DURATIONS_PERPROJECT", "TOTAL_PROJECT", "STATUS", "LAMA_KERJA", "DIVISI", "GOL", "Predicted_LEVEL_KEAHLIAN", "Revisian_LEVEL_KEAHLIAN")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, data)
        connection.commit()
        st.write("Data berhasil disimpan ke database PostgreSQL")
        cursor.close()
        connection.close()
    else:
        st.write("Gagal terhubung ke database PostgreSQL. Periksa 'secrets.toml'.")

# Streamlit UI
st.title("Model Prediksi Level Keahlian")

# Input form for new data
total_project = st.number_input('Kemampuan Menyelesaikan Project [jumlah]')
durations_perproject = st.number_input('Kemampuan Waktu Pengerjaan Tiap Project [hour]')
status = st.selectbox('Status Kerja', le_status.classes_)
lama_kerja = st.number_input('Lama Kerja [year]')
divisi = st.selectbox('Divisi Impian', ohe.categories_[0])
gol = st.selectbox('Target Gol', ohe.categories_[1])
revisian = st.selectbox('Level Keahlian yang Seharusnya', [
    'Pelaksana Madya', 'Pelaksana Pemula', 'Pelaksana Utama',
    'Perekayasa Madya', 'Perekayasa Magang', 'Perekayasa Muda',
    'Perekayasa Utama', 'Pimpinan Madya', 'Pimpinan Muda',
    'Pimpinan Pemula', 'Pimpinan Utama'])

# Condition for button
if st.button('Prediksi'):
    # Preprocess the new input data
    new_data = pd.DataFrame({
        'DURATIONS_PERPROJECT': [durations_perproject],
        'TOTAL_PROJECT': [total_project],
        'STATUS': [status],
        'LAMA_KERJA': [lama_kerja],
        'DIVISI': [divisi],
        'GOL': [gol]
    })

    data_simpan = new_data.copy()

    # Transforming data
    new_data['STATUSenc'] = le_status.transform(new_data['STATUS'])
    encoded_features_new = ohe.transform(new_data[['DIVISI', 'GOL']])
    encoded_df_new = pd.DataFrame(encoded_features_new, columns=ohe.get_feature_names_out(['DIVISI', 'GOL']))
    new_data = pd.concat([new_data, encoded_df_new], axis=1)
    new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']] = scaler.transform(new_data[['DURATIONS_PERPROJECT', 'TOTAL_PROJECT', 'LAMA_KERJA']])

    # Ensure the input data follows the correct order
    X_new = new_data.reindex(columns=feature_order)

    # Prediction
    prediction = modela.predict(X_new)
    st.write(f'Hasil Prediksi: {prediction[0]}')

    # Add the revisian column
    data_simpan['Predicted_LEVEL_KEAHLIAN'] = prediction[0]
    data_simpan['Revisian_LEVEL_KEAHLIAN'] = revisian

    # Save input and prediction to PostgreSQL
    insert_prediction(tuple(data_simpan.values.flatten()))
