from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
#----------------------#
#Initializing databases#
#----------------------#
'''
>>> with app.app_context():
...     db.create_all()
'''

class Toxic(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(15000), nullable=False)
    def __repr__():
        return ''+sno+''

class Blogs(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),unique=True, nullable=False)
    desc = db.Column(db.String(1500), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    auth = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(100), nullable=False)
    def __repr__() -> str:
        return self.title

#----------------------#
# Initializing  routes #
#----------------------#
@app.route('/')
def home():
    blog2=Blogs.query.all()
    return render_template('index.html',blogs=blog2)
    

@app.route('/getPtc',methods=['GET','POST'])
def pic():
    if request.method == 'POST':
        data = request.json['data']
        id = request.json['fata']
        dc = Toxic(data=data)
        db.session.add(dc)
        db.session.commit()
    return jsonify({'kuch':'nehi'})
    
@app.route('/jisanapi/delete/<int:sno>')
def deleteQu(sno):
    qu = Toxic.query.filter_by(sno=sno).first()
    db.session.delete(qu)
    db.session.commit()
    res =jsonify({})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res
        
@app.route('/jisanapi')
def api():
    alldb = Toxic.query.all()
    mur=[]
    for i in alldb:
        mur.append({'data':i.data,'id':i.sno})
    res = jsonify(mur)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/feature')
def feu ():
    return render_template('sample.html')


@app.route('/adminandsiamadmin@keysiam',methods=['GET','POST'])
def admin():
    blog2=Blogs.query.all()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        date = request.form['date']
        auth = request.form['auth']
        img = request.files['image']
        fileName = img.filename
        img.save(os.path.join(os.getcwd()+'/static/images',secure_filename(img.filename)))
        blog = Blogs(title=title,desc=desc,date=date,auth=auth,file=fileName)
        db.session.add(blog)
        db.session.commit()
        blog2=Blogs.query.all()
        return render_template('admin.html',blogs=blog2)
    else:
       return render_template('admin.html',blogs=blog2)

@app.route('/admpcvdelete/<int:id>')
def delete_q(id):
    blog = db.get_or_404(Blogs,id)
    fileName = blog.file
    os.remove(os.getcwd()+'/static/images/'+fileName)
    db.session.delete(blog)
    db.session.commit()
    return redirect('/adminandsiamadmin@keysiam')
@app.route('/adminandsiamlog',methods=['GET','POST'])
def admin_log():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email=='mdsiamca@gmail.com' and password=='admin@keysiam':
            return redirect('adminandsiamadmin@keysiam')
        else:
            return redirect('/')
    else:
        return render_template('log.html')
    
if __name__ == '__main__':
    app.run(port = 8000, debug = True)