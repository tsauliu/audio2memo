# combine the summary and detailed news into a docx file
# %%
from docx import Document

doc = Document('memo_template.docx')
summary_md=open(f'summary.md', 'r', encoding='utf-8').read()
lines = summary_md.strip().split('\n')
for line in lines:
    if line.startswith('# '):
        doc.add_paragraph(line[2:], style='title1')
    elif line.startswith('## '):
        doc.add_paragraph(line[3:], style='title2')
    elif line.startswith('### '):
        doc.add_paragraph(line[4:], style='contentlist')
    elif len(line) > 10:
        doc.add_paragraph(line, style='sublist')

doc.add_page_break()
doc.add_paragraph('Full Discussion',style='section')


raw_md=open(f'raw.md', 'r', encoding='utf-8').read()

lines = raw_md.strip().split('\n')
for line in lines:
    if line.startswith('# '):
        doc.add_paragraph(line[2:], style='title1')
    elif line.startswith('## '):
        doc.add_paragraph(line[3:], style='title2')
    elif len(line) > 20:
        doc.add_paragraph(line, style='contentlist')

doc.save(f'raw.docx')
