from flask import Flask, render_template, request
from text_summary import summarizer
import fitz
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyse():
    if request.method == 'POST':
        pdf_text = ""
        # Check for uploaded PDF
        if 'pdf' in request.files and request.files['pdf'].filename:
            pdf_file = request.files['pdf']
            pdf_text = extract_text_from_pdf(pdf_file)
        
        # Check for raw text input
        if not pdf_text:
            pdf_text = request.form.get('rawtext', "").strip()
            if not pdf_text:
                return "No text provided for summarization", 400
        
        # Validate summary length
        selected_length = request.form.get('summaryLength', "0").strip()
        if not selected_length.isdigit() or int(selected_length) <= 0:
            return "Invalid summary length provided", 400
        selected_length = int(selected_length)

        # Generate summary
        summary, original_text, len_of_orig_text, len_summary, select_len, total_len = summarizer(
            pdf_text, selected_length
        )

        return render_template(
            'summary.html', 
            summary=summary, 
            original_text=original_text, 
            len_of_orig_text=len_of_orig_text, 
            len_summary=len_summary, 
            select_len=select_len, 
            total_len=total_len
        )

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_document = fitz.open(stream=BytesIO(pdf_file.read()))
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        pdf_document.close()  # Ensure the document is closed properly
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text.replace("Ɵ", "ti")

if __name__ == "__main__":
    app.run(debug=True)
