import os
# import secrets

# POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'aws-0-ap-southeast-1.pooler.supabase.com')
# POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres.buekaqirxfuezetbncod')
# POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Gc9SGq2ZLUT9SsUD')  # Ganti dengan placeholder atau nilai default
# POSTGRES_DB = 'postgres'

# Accessing environment variables
# POSTGRES_HOST = os.getenv('POSTGRES_HOST')
# POSTGRES_PORT = os.getenv('POSTGRES_PORT')
# POSTGRES_DB = os.getenv('POSTGRES_DB')
# POSTGRES_USER = os.getenv('POSTGRES_USER')
# POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

# import toml
import streamlit as st

# Set environment variables from secrets.toml
# os.environ['POSTGRES_HOST'] = secrets['connections']['postgresql']['aws-0-ap-southeast-1.pooler.supabase.com']
# os.environ['POSTGRES_PORT'] = secrets['connections']['postgresql']['5432']
# os.environ['POSTGRES_DB'] = secrets['connections']['postgresql']['postgres']
# os.environ['POSTGRES_USER'] = secrets['connections']['postgresql']['postgres.buekaqirxfuezetbncod']
# os.environ['POSTGRES_PASSWORD'] = secrets['connections']['postgresql']['Gc9SGq2ZLUT9SsUD']

# secrets = toml.load('secrets.toml')

# POSTGRES_HOST = secrets['connections']['postgresql']['aws-0-ap-southeast-1.pooler.supabase.com']
# POSTGRES_PORT = secrets['connections']['postgresql']['5432']
# POSTGRES_DB = secrets['connections']['postgresql']['postgres']
# POSTGRES_USER = secrets['connections']['postgresql']['postgres.buekaqirxfuezetbncod']
# POSTGRES_PASSWORD = secrets['connections']['postgresql']['Gc9SGq2ZLUT9SsUD']

# POSTGRES_HOST = st.secrets['connections']['postgresql']['host']
# POSTGRES_PORT = st.secrets['connections']['postgresql']['port']
# POSTGRES_DB = st.secrets['connections']['postgresql']['database']
# POSTGRES_USER = st.secrets['connections']['postgresql']['username']
# POSTGRES_PASSWORD = st.secrets['connections']['postgresql']['password']

SUPABASE_URL = st.secrets['connections']['postgresql']['url']
keSUPABASE_KEYy = st.secrets['connections']['postgresql']['key']

# POSTGRES_HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
# POSTGRES_USER = "postgres.buekaqirxfuezetbncod"
# POSTGRES_PASSWORD = "Gc9SGq2ZLUT9SsUD"
# POSTGRES_DB = "postgres"

# Gunakan variabel ini untuk koneksi database
# print(f"Connecting to database {POSTGRES_DB} on {POSTGRES_HOST}:{POSTGRES_PORT}")