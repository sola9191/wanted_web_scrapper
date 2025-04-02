from flask import Flask, render_template, request, redirect, send_file
import wanted_scrapper as w

app = Flask("__name__")

db = {
    'python' : []
}
@app.route('/')
def home():
    return render_template("home.html", name="sola")
@app.route('/search')
def search():
    keyword = request.args.get("keyword")
    
    if not keyword :
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else : 
        jobs = w.get_job_data(keyword)
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if not keyword:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    w.create_excel_file(keyword)
    return send_file(f"{keyword}.csv", as_attachment=True)
app.run(debug=True)