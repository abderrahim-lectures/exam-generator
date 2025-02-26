import streamlit as st
from code_editor import code_editor
from streamlit_pdf_viewer import pdf_viewer
import uuid
import os
import glob
from gen_lib import generate_shuffled_images
import shutil

CURRENT_USER_ID = 'current-user-id'
CURRENT_USER_DIR = 'current-user-dir'
UPLOAD_DIR = 'upload'
GENERATED_DIR = 'generated_dir'
MARKDOWN_CODE = 'markdown-code'
MAX_COLUMNS = 5

if CURRENT_USER_ID not in st.session_state:
        current_user_id  = uuid.uuid4()
        st.session_state[CURRENT_USER_ID] = str(current_user_id)
        st.session_state[CURRENT_USER_DIR] = f'/tmp/{current_user_id}'
        st.session_state[MARKDOWN_CODE] = '# Main Section'
        
        os.makedirs(st.session_state[CURRENT_USER_DIR], exist_ok=True)
        os.makedirs(f"{st.session_state[CURRENT_USER_DIR]}/{UPLOAD_DIR}", exist_ok=True)
        os.makedirs(f"{st.session_state[CURRENT_USER_DIR]}/{GENERATED_DIR}", exist_ok=True)

generated_instances = []

st.set_page_config(layout='wide')

st.title('Generate Shuffled Images')
st.divider()
st.markdown(f'USER ID: **{st.session_state[CURRENT_USER_ID]}**'.upper())

page_left_column, page_right_column = st.columns(2)

with page_left_column:
    st.header('Upload Images', divider=True)
    uploaded_files  = st.file_uploader('', accept_multiple_files=True, type=['png', 'jpg'])

    if uploaded_files:
        current_user_dir = st.session_state[CURRENT_USER_DIR]

        for uploaded_file in uploaded_files:
            with open(f'{current_user_dir}/{UPLOAD_DIR}/{uploaded_file.name}', 'bw') as f:
                f.write(uploaded_file.read())

        images = glob.glob(f'{current_user_dir}/{UPLOAD_DIR}/*')
        len_images = len(images)

        st.header('Configurations', divider=True)
        
        st.subheader('Grid Configuration')
        st.markdown(f'N# images: {len_images}.')
        num_columns = st.selectbox('N# Columns', range(1, MAX_COLUMNS + 1 if len_images > MAX_COLUMNS  else len_images + 1))
        num_rows = st.selectbox('N# Rows', range(1, len_images//num_columns + 1 if len_images//num_columns > 1 else 2))

        st.subheader('Instances')
        num_instances = st.slider('N# Instances', min_value=1, max_value=40, value=1)

        st.subheader('Add Markdown', divider=True)
        response_dict = code_editor(st.session_state[MARKDOWN_CODE], lang="markdown", height='300px', response_mode="debounce")

        if st.button('Generate the document', use_container_width=True):
            st.session_state[MARKDOWN_CODE] = response_dict['text']

            document_options = {
                'title' : 'The document title',
                'author': 'The author name',
                'markdown': st.session_state[MARKDOWN_CODE],
            }
            geometry_options = {"rmargin": "1cm", "lmargin": "1cm"}

            for _ in range(num_instances):
                generated_instances.append(
                    generate_shuffled_images(
                        f'{current_user_dir}/{UPLOAD_DIR}/', 
                        num_rows, 
                        num_columns, 
                        document_options, 
                        geometry_options,
                        f'{current_user_dir}/{GENERATED_DIR}/'))
            
            # Zip
            zip_filename = str(uuid.uuid4())
            zip_file = f'{current_user_dir}/archive-{zip_filename}'
            shutil.make_archive(zip_file, 'zip', f'{current_user_dir}/{GENERATED_DIR}/')

            st.header('Download', divider=True)
            with open(f"{zip_file}.zip", 'rb') as fp:
                st.download_button('Download the archive file', fp, f'{zip_filename}.zip', mime='application/zip', use_container_width=True)
            
with page_right_column:
    if generated_instances:
        st.header('Preview', divider=True)
        pdf_viewer(f'{generated_instances[0]}.pdf' )