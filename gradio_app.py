import os
import uuid
import shutil
import gradio as gr
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from gen_lib import generate_shuffled_images

geometry_options = {"rmargin": "1cm", "lmargin": "1cm"}

def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths

def markdown_code_input_listener(text):
    return text

def show_pdf_images():
    return convert_from_path('./build/ad1dbdb9-6a2c-47b5-8b75-b6cdf939a174.pdf')

with gr.Blocks() as demo:
    gr.Markdown('# Generated Shuffled Images')
    gr.Markdown('---')

    with gr.Row():
        with gr.Column():
            gr.Markdown('## Upload Files')
            file_output = gr.File(file_types=["image"], file_count="multiple")
            upload_button = gr.UploadButton("Click to Upload a File", file_types=["image"], file_count="multiple")
            upload_button.upload(upload_file, upload_button, file_output)

            gr.Markdown('## List of words')
            words = gr.TextArea(label='Words (separated by newline)')

            gr.Markdown('## Grid Configuration')
            num_rows = gr.Number(minimum=1, value=1, label='Number of rows')
            num_cols = gr.Number(minimum=1, value=1, label='Number of columns')

            gr.Markdown('## Instances Configuration')
            num_instances = gr.Number(minimum=1, value=1, step=1, label='Number of instances')
            seletcted_mode = gr.Dropdown(['Images', 'Words', 'Both'], label='Select the mode')
            
            gr.Markdown('---')
            generate_btn = gr.Button('Generate', variant='primary')
            
        with gr.Column():
            gr.Markdown('## Preview')
            gallery = gr.Gallery(columns=1)

            gr.Markdown('## Download')
            download_button = gr.DownloadButton('Download the archive', interactive=False)

        def generate_listener(images, num_rows, num_cols, num_instances):
            instance_id = str(uuid.uuid4())
            output_dir = f'/tmp/gsi/{instance_id}'
            os.makedirs(output_dir, exist_ok=True)
            
            result = generate_shuffled_images(
                    num_instances=num_instances,
                    images=images, 
                    num_cols=num_cols, 
                    num_rows=num_rows, 
                    output_dir=output_dir,
                    geometry_options=geometry_options
                    )

            zip_filename = str(uuid.uuid4())
            zip_file = f'/tmp/gsi/archive-{zip_filename}'
            shutil.make_archive(zip_file, 'zip', output_dir)

            return {
                download_button: gr.DownloadButton('Download the archive', interactive=True, value=f'{zip_file}.zip', variant='primary'),
                gallery: convert_from_path(f'{result}.pdf')
            }
        
        try:
            generate_btn.click(generate_listener, inputs=[file_output, num_rows, num_cols, num_instances], outputs=[download_button, gallery])
        except Exception as e:
            gr.Error(str(e))

demo.launch()