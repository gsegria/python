from flask import Flask, render_template, request

app = Flask(__name__)

# 首頁
@app.route('/')
def home():
    return render_template('index.html')

# 關於我們
@app.route('/about')
def about():
    return render_template('about.html')

# 聯絡我們（GET 顯示表單，POST 處理表單資料）
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        return render_template('contact.html', name=name, message=message, submitted=True)
    return render_template('contact.html', submitted=False)

if __name__ == '__main__':
    app.run(debug=True)
