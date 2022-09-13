import decimal
import os
from PyPDF2 import PdfMerger, PdfFileWriter,PaperSize

def scale_to_size(writer,page, unit_size):
  input_unit_size = page.mediaBox.upperRight

  factors = [decimal.Decimal(a) / decimal.Decimal(b) for a, b in zip(unit_size, input_unit_size)]
  if factors[0] <= factors[1]:
    # Use x-factor for scaling if this is lowest, or equal to, y-factor
    factor = factors[0]
  else:
    # Otherwise, use the y-factor
    factor = factors[1]

  out_page = writer.addBlankPage(unit_size[0], unit_size[1])
  out_page.mergeScaledPage(page, factor, expand=True)


writer = PdfFileWriter()
target_path = './source'
pdf_lst = [f for f in os.listdir(target_path) if f.endswith('.pdf')]
pdf_lst = [os.path.join(target_path, filename) for filename in pdf_lst]

file_merger = PdfMerger()
for pdf in pdf_lst:
    file_merger.append(pdf)

for merge_page in file_merger.pages:
  page = merge_page.pagedata
  scale_to_size(writer,page,PaperSize.A4)


writer.write('./merge12.pdf')
