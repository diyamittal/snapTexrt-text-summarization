from flask import Flask, render_template, request
from text_summary import summarizer
import PyPDF2
import fitz
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyse():
    if request.method == 'POST':
        if 'pdf' in request.files:
            pdf_file = request.files['pdf']
            pdf_text = extract_text_from_pdf(pdf_file)
            pdf_text = pdf_text.replace("Ɵ", "ti")
        else:
            pdf_text = request.form['rawtext']
            pdf_text = pdf_text.replace("Ɵ", "ti")
        
        selected_length = int(request.form['summaryLength'])

        summary, original_text, len_of_orig_text, len_summary, select_len, total_len = summarizer(pdf_text, selected_length)

    return render_template('summary.html', summary=summary, original_text=original_text, len_of_orig_text=len_of_orig_text, len_summary=len_summary, select_len=select_len, total_len=total_len)

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_document = fitz.open(stream=BytesIO(pdf_file.read()))
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    text = text.replace("Ɵ", "ti")
    return text

if __name__ == "__main__":
    app.run(debug=True)
