# convert_docx_to_pdf.py

from pathlib import Path
import comtypes.client

script_dir = Path(__file__).parent
docx_files = list(script_dir.glob("*.docx"))

if not docx_files:
    print("⚠️ No .docx files found in folder.")
    exit()

# Initialize Word app (Windows-only, requires MS Word installed)
word = comtypes.client.CreateObject("Word.Application")
word.Visible = False

for docx_file in docx_files:
    pdf_file = docx_file.with_suffix(".pdf")
    doc = word.Documents.Open(str(docx_file))
    doc.SaveAs(str(pdf_file), FileFormat=17)  # 17 = wdFormatPDF
    doc.Close()
    print(f"✅ Converted: {docx_file.name} → {pdf_file.name}")

word.Quit()


#python #docxtopdf #pdfconversion #automation #documenttools #businessdataanalyst #traceability #documentationtools #batchprocessing #reportingautomation #documentconversion #workflowtools

#aiposbuilt #fromukrainianswithlovetohumankind 🇺🇦

youtube: https://youtube.com/shorts/C9vmmUVgi4s

github: https://github.com/TK51/aipos-public-eng/blob/main/tools/tools-03-convert_docx_to_pdf.py
