from flask import Flask, request, jsonify
import pickle
import re
import nltk
import fitz  # PyMuPDF
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows React to talk to Flask

# Load model and vectorizer
clf = pickle.load(open('clf.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

def preprocess(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    words = nltk.word_tokenize(text)
    words = [w for w in words if w not in stopwords.words('english')]
    return ' '.join(words)

def extract_text(file_stream):
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route('/classify', methods=['POST'])
def classify_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    text = extract_text(file)
    clean_text = preprocess(text)
    vector = tfidf.transform([clean_text])
    prediction = clf.predict(vector)[0]

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
