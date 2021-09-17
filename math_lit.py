import random

from datetime import datetime
from flask import render_template_string
from logging import getLogger
from pdflatex import PDFLaTeX

log = getLogger(__name__)


def generate_pdf(tex_string: str) -> (str, bytes):
    """
    This function generates the PDF
    """
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d:%H:%M:%S')
    filename = 'mathematics-literacy-practise-{}.pdf'.format(timestamp)
    file_path = './documents/{}'.format(filename)
    pdfl = PDFLaTeX.from_binarystring(
        bytes(tex_string, 'utf-8'),
        filename
    )
    pdf, log, cp = pdfl.create_pdf()
    with open(file_path, 'wb') as fw:
        fw.write(pdf)
    fw.close()
    return filename, pdf


def generate_template(template: str, data: dict) -> str:
    """
    This function renders a html string from the html file and populates it with the data
    """
    with open('./templates/{}.tex'.format(template), 'r') as f:
        tex_raw_string = f.read()

    # populate the document
    tex_string = render_template_string(tex_raw_string, **data)

    log.info(tex_string)
    return tex_string


def generate_data() -> dict:
    """
    This function is to generate all the random data for the file
    """
    m = {
        '1': [num(1, 13)],
        '2': [num(1, 13)],
        '3': [num(1, 13)],
        '4': [num(1, 13)],
        '5': [num(1, 13), num(1, 13)],
        '6': [num(1, 13)],
        '7': [num(1, 13), num(1, 13)],
        '8': [num(1, 13), num(1, 13)],
        '9': [num(1, 13), num(1, 13)],
        '10': [num(1, 13)],
    }
    return {
        'addition': [num(0, 100) for _ in range(24)],
        'subtraction': [num(0, 100) for _ in range(24)],
        'multiplication': [num(0, 13) for _ in range(24)],
        'division': [
            num(0, 13) * m['1'][0], m['1'][0],
            num(0, 13) * m['2'][0], m['2'][0],
            num(0, 13) * m['3'][0], m['3'][0],
            num(0, 13) * m['4'][0], m['4'][0],
            num(0, 13) * m['5'][0] * m['5'][1], m['5'][0], m['5'][1],
            num(0, 13) * m['6'][0], m['6'][0],
            num(0, 13) * m['7'][0] * m['7'][1], m['7'][0], m['7'][1],
            num(0, 13) * m['8'][0] * m['8'][1], m['8'][0], m['8'][1],
            num(0, 13) * m['9'][0] * m['9'][1], m['9'][0], m['9'][1],
            num(0, 13) * m['10'][0], m['10'][0],
        ],
        'round_decimals': [
            num(0, 100, divisor=10), 'number',
            num(0, 100, divisor=10), 'number',
            num(0, 1000, divisor=100), 'number',
            num(0, 1000, divisor=100), 'number',
            num(0, 1000, divisor=100), 'ten',
            num(0, 1000, divisor=100), 'ten',
            num(0, 100, divisor=100), 'tenth',
            num(0, 1000, divisor=100), 'tenth',
            num(0, 1000, divisor=10000), 'one hundredth',
            num(0, 1000, divisor=10000), 'one hundredth',
        ],
        'decimal_to_frac': [num(0, 1000, divisor=1000) for _ in range(10)],
        'frac_to_decimal': [num(0, 20) for _ in range(20)]
    }


def num(range_min, range_max, divisor=1):
    """
    This function generates random numbers from the ranges provided.
    """
    return random.randint(range_min, range_max) / divisor
