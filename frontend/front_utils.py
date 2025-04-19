import pdfplumber
import docx


def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")
    elif file_type == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file_type == "docx":
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return None


def format_score_label(score):
    if score >= 0.75:
        return f"🟢 Candidate #{i + 1} — Score: {score:.3f}"
    elif score < 0.4:
        return f"🔴 Candidate #{i + 1} — Score: {score:.3f}"
    else:
        return f"🟡 Candidate #{i + 1} — Score: {score:.3f}"
