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
            
            gr.Markdown('## Enter You Markdown Code')
            markdown_code = gr.Code('# Main Section', language='markdown', show_line_numbers=True, interactive=True)

            gr.Markdown('## Grid Configuration')
            num_rows = gr.Number(minimum=1, value=1, label='Number of rows')
            num_cols = gr.Number(minimum=1, value=1, label='Number of columns')

            gr.Markdown('## Instances Configuration')
            num_instances = gr.Number(minimum=1, value=1, step=1, label='Number of instances')
            doc_title = gr.Textbox(label='Title', value='The document title')
            doc_author = gr.Textbox(label='Author', value='Author name')

            gr.Markdown('---')
            generate_btn = gr.Button('Generate', variant='primary')
            
        with gr.Column():
            gr.Markdown('## Preview')
            gallery = gr.Gallery(columns=1)

            gr.Markdown('## Download')
            download_button = gr.DownloadButton('Download the archive', interactive=False)

        def generate_listener(images, markdown_code, num_rows, num_cols, num_instances, title, author):
            instance_id = str(uuid.uuid4())
            output_dir = f'/tmp/gsi/{instance_id}'
            os.makedirs(output_dir, exist_ok=True)
            
            genereted_items = []
            for _ in range(num_instances):
                result = generate_shuffled_images(
                    images=images, 
                    num_cols=num_cols, 
                    num_rows=num_rows, 
                    output_dir=output_dir,
                    geometry_options=geometry_options,
                    document_options={
                    'title' : title,
                    'author': author,
                    'markdown': markdown_code,
                })
                genereted_items.append(result)

            zip_filename = str(uuid.uuid4())
            zip_file = f'/tmp/gsi/archive-{zip_filename}'
            shutil.make_archive(zip_file, 'zip', output_dir)

            return {
                download_button: gr.DownloadButton('Download the archive', interactive=True, value=f'{zip_file}.zip', variant='primary'),
                gallery: convert_from_path(f'{genereted_items[0]}.pdf')
            }
        
        generate_btn.click(generate_listener, inputs=[file_output, markdown_code, num_rows, num_cols, num_instances, doc_title, doc_author], outputs=[download_button, gallery])
if __name__ == "__main__":
    demo.launch(share=True)