import os

from pylatex import (
    Document,
    Command,
    Figure,
    SubFigure,
    NoEscape,
    Package,
)
from pylatex.base_classes import Environment
import glob
import random
import uuid


class Markdown(Environment):
    """A class to wrap LaTeX's markdown environment."""

    packages = [Package('markdown', ['hashEnumerators', 'smartEllipses'])]
    escape = False
    content_separator = "\n"


def generate_shuffled_images(num_instances=1, images=None, dirname=None, num_rows=1, num_cols=1, document_options=None, geometry_options=None, output_dir=None):
    if images is None and dirname is not None:
        images = glob.glob(f'{dirname}/*')

    assert len(images) >= num_rows * num_cols, f'The number of images of images is less than the expected grid (num_rows={num_rows}, num_cols={num_cols}).'

    # Document default filename
    filename = f'{output_dir}/{uuid.uuid4()}'
    
    # Document object
    doc = Document(filename, geometry_options=geometry_options)

    for _ in range(num_instances):
        random.shuffle(images)

        with doc.create(Figure(position='hbt!')):
                doc.append(Command('centering'))
                for i in range(num_rows):
                    for j in range(num_cols):
                        with doc.create(SubFigure(position='t', width=NoEscape(f"{1/(num_cols + 1)}\\linewidth"))) as fig:
                            fig.add_image(images[i * num_cols + j], width=NoEscape(r"0.95\linewidth"))
                            doc.append(NoEscape(r'\hfill\hspace{0.5em}'))
                    doc.append(NoEscape(r'\hspace{\fill}'))
        
        doc.append(NoEscape(r'\newpage'))
        
    doc.generate_pdf(compiler_args=['--shell-escape'])
    doc.generate_tex()

    return filename
