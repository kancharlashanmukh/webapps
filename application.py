from flask import Flask,render_template, request
import requests
import json
import psycopg2
app = Flask(__name__)


DATABASE_URL =  'postgres://noxthjmjrdzasn:76ff1ab5fd7f09c73f6fe82ee4a7a2b5fa8920f75f3ef32679a1186ea743f359@ec2-107-21-122-38.compute-1.amazonaws.com:5432/defdshlvvo279k'
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

print("Connection established")
cursor = conn.cursor()
# home page direct
@app.route("/")
def hello():
   return render_template('index.html')
@app.route("/update",methods = ['POST'])
def update():
   return render_template('update.html')
@app.route("/add",methods = ['POST'])
def add():
   return render_template('add.html')
@app.route("/delete",methods = ['POST'])
def delete():
   return render_template('delete.html')

# new record method
@app.route('/adddata',methods = ['POST'])
def adddata():
    
    try:

        collegename = request.form['cname']
        webpage = request.form['webpage']
        code = request.form['code']
        country = request.form['country']

        DATABASE_URL =  'postgres://noxthjmjrdzasn:76ff1ab5fd7f09c73f6fe82ee4a7a2b5fa8920f75f3ef32679a1186ea743f359@ec2-107-21-122-38.compute-1.amazonaws.com:5432/defdshlvvo279k'
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        print("Connection established")
        cursor = conn.cursor()
        data=requests.get('http://universities.hipolabs.com/search?country=canada')
        data=data.json()
        for rows in data:
            cname=rows["name"]
            webpage=rows["web_pages"][0]
            country=rows["country"]    
            code=rows["alpha_two_code"]
            cursor.execute("INSERT INTO universitylist(cname, webpage, country, code) VALUES (%s, %s,%s, %s);", (cname,webpage,country,code))
            print("inserted")
            conn.commit()  
        return render_template("index.html",)
    except IOError:
        return print("Please contatct admin")
# Insert data method
@app.route('/insertdata',methods = ['POST'])
def insertdata():
    
    try:
        print("in")
        collegename = request.form['cname']
        webpage = request.form['webpage']
        code = request.form['code']
        country = request.form['country']

        cursor.execute("INSERT INTO universitylist(cname, webpage, country, code) VALUES (%s, %s,%s, %s);", (collegename,webpage,country,code))
        print("inserted")
        conn.commit()  
        msg="Record Inserted"
        return render_template("add.html",msg=msg)
    except IOError:
        return print("Please contatct admin")
# list data method
@app.route('/getdata',methods = ['POST'])
def getdata():
    
    try:                       
        
        cursor.execute("select * from universitylist")
        getdata1=cursor.fetchall()
        collegenamelist=[]
        webpagelist=[]
        countrylist=[]
        codelist=[]
        for chr1 in getdata1:
            collegenamelist.append(chr1[0])
            webpagelist.append(chr1[1])
            countrylist.append(chr1[2])
            codelist.append(chr1[3])
        conn.commit()
        zipp=zip(collegenamelist,webpagelist,countrylist,codelist)
        
        return render_template("index.html",zipp=zipp)
    except IOError:
        return print("Please contatct admin")
# update data method
@app.route('/updatedata',methods = ['POST'])
def updatedata():
    print("in update")
    collegename = request.form['cname']
    webpage = request.form['webpage']
    code = request.form['code']
    country = request.form['country']
    wherecollegename = request.form['cuname']
    cursor.execute("UPDATE public.universitylist SET cname='"+collegename+"', webpage='"+webpage+"', country='"+country+"', code='"+code+"' WHERE cname='"+wherecollegename+"'")
    msg="Record Updated"
    return render_template("update.html",msg=msg)
# delete data method
@app.route('/deletedata',methods = ['POST'])
def deletedata():
    print("in delete")
    collegename = request.form['cname']
    
    cursor.execute("DELETE FROM universitylist	WHERE cname='"+collegename+"'")
    msg="Record Deleted"
    return render_template("delete.html",msg=msg)

if __name__ == '__main__':
    app.run()