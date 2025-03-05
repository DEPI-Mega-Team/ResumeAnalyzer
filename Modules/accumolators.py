import io
import re

import zipfile
import pymupdf
from datetime import datetime
from dateutil import relativedelta
from.extractors import handle_io_bytes

def get_number_of_pages(resume, ext):
    if ext == 'pdf':
        return get_number_of_pages_pdf(resume)

    elif ext == 'docx':
        return get_number_of_pages_docx(resume)

@handle_io_bytes
def get_number_of_pages_pdf(pdf_file):
    with pymupdf.open(stream= pdf_file, filetype="pdf") as doc:
        page_count = len(doc)
    
    return page_count

def get_number_of_pages_docx(docx_file: str | io.BytesIO) -> int:
    
    archive = zipfile.ZipFile(docx_file, "r")
    ms_data = archive.read("docProps/app.xml")
    archive.close()
    
    app_xml = ms_data.decode("utf-8")

    regex = r"<(Pages)>(\d+)</(Pages)>"

    matches = re.findall(regex, app_xml, re.MULTILINE)
    match = matches[0] if matches[0:] else [0, 0]
    page_count = match[1]

    return page_count


def get_total_experience(experience_list):
    '''
    Wrapper function to extract total months of experience from a resume

    :param experience_list: list of experience text extracted
    :return: total months of experience
    '''
    assert isinstance(experience_list, list), "Input experience_list must be a list"

    exp_ = []
    for line in experience_list:
        assert isinstance(line, str), "Each item in experience_list must be a string"
        
        experience = re.search(
            r'(?P<fmonth>\w+. ?\d+)\s*(\D|to)\s*(?P<smonth>\w+. ?\d+|present)',
            line,
            re.I
        )
        if experience:
            exp_.append(experience.groups())

    total_exp = sum(
        [abs(get_number_of_months_from_dates(i[0], i[2])) for i in exp_]
    )
    total_experience_in_months = total_exp

    assert isinstance(total_experience_in_months, int), "Output total_experience_in_months must be an integer"
    return total_experience_in_months


def get_number_of_months_from_dates(date1, date2):
    '''
    Helper function to extract total months of experience from a resume

    :param date1: Starting date
    :param date2: Ending date
    :return: months of experience from date1 to date2
    '''
    if date2.lower() == 'present':
        date2 = datetime.now().strftime('%b %Y')
    try:
        if len(date1.split()[0]) > 3:
            date1 = date1.split()
            date1 = date1[0][:3] + ' ' + date1[1]
        if len(date2.split()[0]) > 3:
            date2 = date2.split()
            date2 = date2[0][:3] + ' ' + date2[1]
    except IndexError:
        return 0
    try:
        date1 = datetime.strptime(str(date1), '%b %Y')
        date2 = datetime.strptime(str(date2), '%b %Y')
        months_of_experience = relativedelta.relativedelta(date2, date1)
        months_of_experience = (months_of_experience.years
                                * 12 + months_of_experience.months)
    except ValueError:
        return 0
    return months_of_experience