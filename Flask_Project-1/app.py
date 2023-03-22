from flask import Flask,render_template,request
import re
app=Flask(__name__)

@app.route('/')
def home_fun():
    return render_template('home.html')

@app.route('/match',methods=['GET','POST'])
def match_fun():
    if request.method=='POST':
        text_string=request.form.get('text_string',False)
        regex=request.form.get('regex')
        matches=re.findall(str(regex),str(text_string))
        return render_template('matcher.html',text_string=text_string,regex=regex,matches=matches)
    else:
        return render_template('matcher.html')

if __name__=='__main__':
    app.run(debug=True)
    
