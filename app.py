from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def load_data():
    try:
        return pd.read_excel("books_data.xlsx")
    except:
        return pd.DataFrame(columns=["title", "price", "rating", "detail_url", "description"])

data = load_data()

@app.route("/", methods=["GET", "POST"])
def index():
    search = (request.form.get("search") or "").strip()
    results = data

    if search:
        mask = (data["title"].str.contains(search, case=False, na=False)) | \
               (data["description"].str.contains(search, case=False, na=False))
        results = data[mask]

    books = results.to_dict(orient="records")
    return render_template("index.html", books=books, search=search, total=len(books))

if __name__ == "__main__":
    app.run(debug=True)
