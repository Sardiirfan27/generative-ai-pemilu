import os
import ast
import streamlit as st
# import tempfile
# import zipfile
from PIL import Image
import pandas as pd
import create_table as ct
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Konfigurasi API key untuk Gemini
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Fungsi untuk konfigurasi model Gemini
@st.cache_data
def configure_model(system_instruction=None,
                    temperature=1.2, top_p=0.95, top_k=64,
                    model_name='gemini-1.5-flash'):
    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k
    }
    model = genai.GenerativeModel(model_name=model_name,
                                  generation_config=generation_config,
                                  system_instruction=system_instruction)
    return model

# Fungsi untuk membaca file atau folder yang diunggah
# Streamlit UI untuk upload file atau folder
st.header("Aplikasi AI - Analisis Data Pemilu 🇮🇩",divider='rainbow')

# File uploader
uploaded_file = st.file_uploader("Upload file atau folder (ZIP)", type=["jpg", "jpeg", "png", "zip"], accept_multiple_files=False)



if uploaded_file:
    
    #st.write(f"File yang diproses: {len(uploaded_file)}")
    img= Image.open(uploaded_file)
    st.image(img, use_container_width=True)
    
    # Integrasi model Gemini
    model = configure_model()
    with st.spinner("Sedang Menghasilkan Analisis..."):
        response_1 = model.generate_content(['''Anda adalah AI & Data expert untuk data pemilu,
                                            dari hasil response image tersebut buatlah dictionary "data" berisi list nama_calon & jumlah_suara(sah):
                                            - isi nama_calon: Anies,Prabowo atau Ganjar.
                                            - isi jumlah_suara(sah): misalkan 116 dan seterusnya.
                                            contoh: data = {'nama_calon':[Anies, Prabowo, Ganjar],'jumlah_suara(sah)':[116,20,30]}
                                            generate hanya code
                                            ''', img])
        code_py_1 = response_1.text.strip("```python\n").strip("```")
        
        prompt=f'''Dari tabel {response_1},
        buatlah visualisasi bar chart untuk persentase suara (.2f),
        label harus berurutan dan nama pendek misalkan `Anies`,
        gunakan st.plotly_chart(fig) dengan (warna red,gred, blue))',
        generate hanya code'''
        response_2= model.generate_content([prompt])
        code_py_2 = response_2.text.strip("```python\n").strip("```")
        
        prompt=f'''Dari hasil response tersebut buatlah content berita yang menarik,
        berisi penjelasan analisis hasil pemilu pada setiap nama calon :{response_1},
        Jadi markdown yang rapi:
        - Judul Berita menarik dan harus ada wilayahnya
        - Isi Berita menarik dan ada tabelnya.
       '''
        response_3= model.generate_content([prompt,img])
    
    #st.subheader("Hasil Analisis Data Pemilu:")
    # Placeholder untuk loading
    
    #st.write(code_py_1)
    #st.write(response_2.text)
    # Langkah 2: Menjalankan kode
    exec(code_py_2)
    st.write(response_3.text)
    
    #delete table
    # ct.delete_table()

    #buat table
    ct.create_table()

    # insert data
    # data= {
    #     'nama_calon': ['joko','tono'],
    #     'jumlah_pemilih': [10,20],
    # }


    # Dari code_py_1 Ambil bagian setelah tanda "="
    data_string = code_py_1.split('=', 1)[1].strip()

    # Ubah string menjadi dictionary
    data_dict = ast.literal_eval(data_string)
    # st.write(data_dict)

    # Iterasi data dan masukkan ke dalam database
    for nama, jumlah in zip(data_dict['nama_calon'], data_dict['jumlah_suara(sah)']):
        ct.add_data(nama, jumlah)

    # Fungsi untuk mengambil data
    @st.cache_resource
    def get_data():
        conn = ct.create_connection()
        df = pd.read_sql_query("SELECT * FROM pemilu", conn)
        conn.close()
        return df

    print(get_data())
