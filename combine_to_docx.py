# combine the summary and detailed news into a docx file
# %%
from docx import Document
import shutil
import os

def combine_to_docx(project):
    doc = Document('memo_template.docx')
    summary_md=open(next((f'./3_memo/{f}' for f in os.listdir('./3_memo/') if f.startswith(project)), f'./3_memo/{project}.txt'), 'r', encoding='utf-8').read()
    lines = summary_md.strip().split('\n')
    for line in lines:
        if line.startswith('# '):
            doc.add_paragraph(line.replace('# ',''), style='title1')
        elif line.startswith('## '):
            doc.add_paragraph(line.replace('## ',''), style='title2')
        elif line.startswith('### '):
            doc.add_paragraph(line.replace('### ',''), style='contentlist')
        elif len(line) > 10:
            doc.add_paragraph(line, style='sublist')

    doc.add_page_break()
    doc.add_paragraph('Full Discussion',style='section')


    raw_md=open(next((f'./2_wordforword/{f}' for f in os.listdir('./2_wordforword/') if f.startswith(project)), f'./2_wordforword/{project}.txt'), 'r', encoding='utf-8').read()

    lines = raw_md.strip().split('\n')
    for line in lines:
        if line.startswith('# '):
            doc.add_paragraph(line.replace('# ',''), style='title1')
        elif line.startswith('## '):
            doc.add_paragraph(line.replace('## ',''), style='title2')
        elif len(line) > 20:
            doc.add_paragraph(line.replace('### ',''), style='contentlist')

    doc.save(f'./4_docx/{project}.docx')
    shutil.copyfile(f'./4_docx/{project}.docx', f'~/Dropbox/VoiceMemos/{project}.docx')


if __name__ == '__main__':
    project='grab交接'
    combine_to_docx(project)