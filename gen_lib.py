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


def generate_shuffled_images(dirname, num_rows, num_cols, document_options, geometry_options, output_dir):
    images = glob.glob(f'{dirname}/*')

    assert len(images) >= num_rows * num_cols, 'The number of images of images is less than the expected table.'

    random.shuffle(images)

    # Document default filename
    filename = f'{output_dir}/{uuid.uuid4()}'
    
    # Document object
    doc = Document(filename, geometry_options=geometry_options)

    doc.preamble.append(Command("title", document_options['title']))
    doc.preamble.append(Command("author", document_options['author']))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))

    with doc.create(Markdown()):
            doc.append(document_options['markdown'])
    print(num_rows, num_cols)

    with doc.create(Figure(position='hbt!')):
            doc.append(Command('centering'))
            for i in range(num_rows):
                for j in range(num_cols):
                    with doc.create(SubFigure(position='t', width=NoEscape(f"{1/(num_cols + 1)}\\linewidth"))) as fig:
                        fig.add_image(images[i * num_cols + j], width=NoEscape(r"\linewidth"))
                        fig.add_caption('')
                doc.append(NoEscape(r'\hspace{\fill}'))
    
    doc.generate_pdf(compiler_args=['--shell-escape'])
    doc.generate_tex()

    return filename

if __name__ == '__main__':
    dirname = os.path.abspath('./downloads/trainingSample/')
    num_rows = 5
    num_cols = 5
    document_options = {
        'title' : 'The document title',
        'author': 'The author name',
        'markdown': '# First section',
    }
    geometry_options = {"rmargin": "1cm", "lmargin": "1cm"}
    output_dir = 'build'
    generate_shuffled_images(dirname, num_rows, num_cols, document_options, geometry_options, output_dir)









