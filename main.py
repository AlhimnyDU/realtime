import os
from flask import Flask, flash, url_for, request, render_template, session
from logging import FileHandler, WARNING
from werkzeug.utils import redirect, secure_filename
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import secrets
from werkzeug.utils import redirect, secure_filename
import datetime
from datetime import datetime
from flaskext.mysql import MySQL
import textwrap




app = Flask(__name__)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)
app.config.from_object(__name__)
UPLOAD_FOLDER = './static/gambar/'
UPLOAD_FOLDER = './static/input/'
app.secret_key = 'any random string'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'tracerstudy_studypk'
app.config['MYSQL_DATABASE_PASSWORD'] = 'T42ngk4l4n'
app.config['MYSQL_DATABASE_DB'] = 'tracerstudy_ts_bka'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'ts_bka'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL(app)
con = mysql.connect()


@app.route('/')
def index():
    print("hallo")
    return "hallo"

@app.route('/piechart/<id_fitur>', methods=['POST', 'GET'])
def piechart(id_fitur):
    atribut = []
    explode = []
    index = []
    # print(id_fitur)
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM fitur WHERE id_fitur=%s", (id_fitur))
    fitur = cur.fetchone()

    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM kuesioner WHERE id_kuesioner=%s", (fitur[5]))
    kuesioner = cur.fetchone()

    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM variabel WHERE id_fitur=%s", (id_fitur))

    variabel = cur.fetchall()
    i = 1
    for a in variabel:
        atribut.append(a[1])
        explode.append(0.05)
        index.append(i)
        i+=1

    fix_atribut = atribut

    excel="../public_html/cdc/excel/kuesioner/"+kuesioner[4]
    # excel="D:/Proyek/xampp/ts_bka/excel/kuesioner/"+kuesioner[4]

    # print(excel)
    df = pd.read_excel(excel)
    # print(df)
    if (df.empty):
        df_olah = df
        jml = 0
    else:
        df_olah = df.dropna(subset=[fitur[1]], axis=0)
        df_olah = df_olah[['NRP', fitur[1]]].groupby([fitur[1]]).count()
        jml = df_olah['NRP'].sum()
        df_olah = df_olah.reset_index()

    print(index)
    print(df_olah[fitur[1]].values)
    if (df_olah[fitur[1]].count() != 0):
        if (df_olah[fitur[1]].count() < len(atribut)):
            cek = array_diff(index,df_olah[fitur[1]].values)
            print(cek)
            if cek is not None:
                for j in cek:
                    # print(j)
                    print(atribut[j-1])
                    fix_atribut.remove(atribut[j-1])
                    explode.pop(0)
    else:
        new_row = {fitur[1]: "NULL", 'NRP': 0}
        df_olah = df_olah.append(new_row, ignore_index=True)
        fix_atribut = ['Kosong']
        explode = [0]

    print(fix_atribut)
    print(len(atribut))
    fix_atribut = [textwrap.TextWrapper(width=40).fill(text=l) for l in fix_atribut]

    # code here
    plt.figure(figsize=(12, 6))
    plt.title("Persentase Mahasiswa "+(fitur[2]), pad=20)
    plt.pie(df_olah['NRP'], labels=fix_atribut, autopct=make_autopct(df_olah['NRP']), labeldistance=1.2, explode=explode)
    nama_file = secrets.token_hex(nbytes=16)+".png"
    plt.savefig("../public_html/cdc/data_olah/"+nama_file)
    # plt.savefig("D:/Proyek/xampp/ts_bka/data_olah/"+nama_file)
    if(fitur[3]!=None):
        rmv='../public_html/cdc/data_olah/'+fitur[3]
        # rmv='D:/Proyek/xampp/ts_bka/data_olah/'+fitur[3]

        os.remove(rmv)

    cur = con.cursor()
    sql = "UPDATE fitur SET gambar=%s, updated=%s WHERE id_fitur=%s"
    record = (nama_file, date, id_fitur)
    cur.execute(sql, record)
    con.commit()

    return redirect("https://tracerstudy.itenas.ac.id/cdc/admin/olah_fitur/"+id_fitur+"/"+str(jml))
    # return redirect("http://localhost/ts_bka/admin/olah_fitur/"+id_fitur+"/"+str(jml))

@app.route('/piechart_non/<id_fitur>', methods=['POST', 'GET'])
def piechart_non(id_fitur):
    atribut = []
    explode = []
    index = []
    # print(id_fitur)
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM fitur WHERE id_fitur=%s", (id_fitur))
    fitur = cur.fetchone()

    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM kuesioner WHERE id_kuesioner=%s", (fitur[5]))
    kuesioner = cur.fetchone()

    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM variabel WHERE id_fitur=%s", (id_fitur))

    variabel = cur.fetchall()
    i = 1
    for a in variabel:
        atribut.append(a[1])
        explode.append(0.05)
        index.append(i)
        i += 1

    fix_atribut = atribut

    excel = "../public_html/cdc/excel/kuesioner/" + kuesioner[4]
    # print(excel)
    df = pd.read_excel(excel)
    # print(df)
    if (df.empty):
        df_olah = df
        jml = 0
    else:
        df_olah = df.dropna(subset=[fitur[1]], axis=0)
        df_olah = df_olah[['NRP', fitur[1]]].groupby([fitur[1]]).count()
        jml = df_olah['NRP'].sum()
        df_olah = df_olah.reset_index()

    print(index)
    print(df_olah[fitur[1]].values)
    if (df_olah[fitur[1]].count() != 0):
        if (df_olah[fitur[1]].count() < len(atribut)):
            cek = array_diff(index, df_olah[fitur[1]].values)
            print(cek)
            if cek is not None:
                for j in cek:
                    # print(j)
                    print(atribut[j - 1])
                    fix_atribut.remove(atribut[j - 1])
                    explode.pop(0)
    else:
        new_row = {fitur[1]: "NULL", 'NRP': 0}
        df_olah = df_olah.append(new_row, ignore_index=True)
        fix_atribut = ['Kosong']
        explode = [0]

    print(fix_atribut)
    print(len(atribut))
    fix_atribut = [textwrap.TextWrapper(width=40).fill(text=l) for l in fix_atribut]

    # code here
    plt.figure(figsize=(12, 6))
    plt.title("Persentase Mahasiswa " + (fitur[2]), pad=20)
    plt.pie(df_olah['NRP'], labels=fix_atribut, autopct=make_autopct(df_olah['NRP']), labeldistance=1.2,explode=explode)
    nama_file = secrets.token_hex(nbytes=16) + ".png"
    plt.savefig("../public_html/cdc/data_olah/" + nama_file)
    if (fitur[3] != None):
        rmv = '../public_html/cdc/data_olah/' + fitur[3]
        os.remove(rmv)

    cur = con.cursor()
    sql = "UPDATE fitur SET gambar=%s, updated=%s WHERE id_fitur=%s"
    record = (nama_file, date, id_fitur)
    cur.execute(sql, record)
    con.commit()

    return redirect("https://tracerstudy.itenas.ac.id/cdc/nonediting/olah_fitur/"+id_fitur+"/"+str(jml))


@app.route('/prodi_piechart/<id_fitur>', methods=['POST', 'GET'])
def prodi_piechart(id_fitur):
    atribut = []
    explode = []
    index = []
    prodi = request.form.get('lembaga')
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM fitur WHERE id_fitur=%s", (id_fitur))
    fitur = cur.fetchone()

    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM kuesioner WHERE id_kuesioner=%s", (fitur[5]))
    kuesioner = cur.fetchone()

    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM variabel WHERE id_fitur=%s", (fitur[0]))

    variabel = cur.fetchall()
    i = 1
    for a in variabel:
        atribut.append(a[1])
        explode.append(0.05)
        index.append(i)
        i+=1

    fix_atribut = atribut

    excel="../public_html/cdc/excel/    kuesioner/"+kuesioner[4]
    df = pd.read_excel(excel)
    df_olah = df.dropna(subset=[fitur[1]], axis=0)
    df_olah = df_olah[['Program Studi', 'NRP', fitur[1]]].groupby(['Program Studi', fitur[1]]).count()
    df_olah = df_olah.reset_index()
    df_olah = df_olah.loc[df_olah['Program Studi'] == prodi]
    jml = df_olah['NRP'].sum()
    # print(jml)
    df_olah = df_olah.reset_index()
    # print(df_olah.info())
    # print(atribut)
    print(index)
    print(df_olah[fitur[1]].values)
    if (df_olah[fitur[1]].count() != 0):
        if (df_olah[fitur[1]].count() < len(atribut)):
            cek = array_diff(index,df_olah[fitur[1]].values)
            # print(cek)
            if cek is not None:
                for j in cek:
                    fix_atribut.remove(atribut[j - 1])
                    explode.pop(0)
    else:
        new_row = {'Program Studi': prodi, fitur[1]: "NULL", 'NRP': 0}
        df_olah = df_olah.append(new_row, ignore_index=True)
        fix_atribut = ['Kosong']
        explode = [0]
            # new_row = {'Program Studi': prodi, fitur[1]: "NULL", 'NRP': 0}
            # df_olah = df_olah.append(new_row, ignore_index=True)

    fix_atribut = [textwrap.TextWrapper(width=40).fill(text=l) for l in atribut]

    # print(df_olah)
    # print(atribut)
    #code here
    plt.figure(figsize=(12, 6))
    plt.title("Persentase Mahasiswa "+prodi+" "+fitur[2], pad=20)
    plt.pie(x=df_olah['NRP'], labels=fix_atribut, autopct=make_autopct(df_olah['NRP']), labeldistance=1.2, explode=explode)
    nama_file = secrets.token_hex(nbytes=16)+".png"
    plt.savefig("../public_html/cdc/data_olah/"+nama_file)

    if (fitur[3] != None):
        rmv = '../public_html/cdc/data_olah/' + fitur[3]
        os.remove(rmv)

    cur = con.cursor()
    sql = "UPDATE fitur SET gambar=%s, updated=%s WHERE id_fitur=%s"
    record = (nama_file, date, id_fitur)
    cur.execute(sql, record)
    con.commit()

    return redirect("https://tracerstudy.itenas.ac.id/cdc/admin/olah_fitur/"+id_fitur+"/"+str(jml))

@app.route('/prodi_piechart_non/<id_fitur>', methods=['POST', 'GET'])
def prodi_piechart_non(id_fitur):
    atribut = []
    explode = []
    index = []
    prodi = request.form.get('lembaga')
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM fitur WHERE id_fitur=%s", (id_fitur))
    fitur = cur.fetchone()

    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM kuesioner WHERE id_kuesioner=%s", (fitur[5]))
    kuesioner = cur.fetchone()

    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM variabel WHERE id_fitur=%s", (fitur[0]))

    variabel = cur.fetchall()
    i = 1
    for a in variabel:
        atribut.append(a[1])
        explode.append(0.05)
        index.append(i)
        i += 1

    fix_atribut = atribut

    excel = "../public_html/cdc/excel/    kuesioner/" + kuesioner[4]
    df = pd.read_excel(excel)
    df_olah = df.dropna(subset=[fitur[1]], axis=0)
    df_olah = df_olah[['Program Studi', 'NRP', fitur[1]]].groupby(['Program Studi', fitur[1]]).count()
    df_olah = df_olah.reset_index()
    df_olah = df_olah.loc[df_olah['Program Studi'] == prodi]
    jml = df_olah['NRP'].sum()
    # print(jml)
    df_olah = df_olah.reset_index()
    # print(df_olah.info())
    # print(atribut)
    print(index)
    print(df_olah[fitur[1]].values)
    if (df_olah[fitur[1]].count() != 0):
        if (df_olah[fitur[1]].count() < len(atribut)):
            cek = array_diff(index, df_olah[fitur[1]].values)
            # print(cek)
            if cek is not None:
                for j in cek:
                    fix_atribut.remove(atribut[j - 1])
                    explode.pop(0)
    else:
        new_row = {'Program Studi': prodi, fitur[1]: "NULL", 'NRP': 0}
        df_olah = df_olah.append(new_row, ignore_index=True)
        fix_atribut = ['Kosong']
        explode = [0]
        # new_row = {'Program Studi': prodi, fitur[1]: "NULL", 'NRP': 0}
        # df_olah = df_olah.append(new_row, ignore_index=True)

    fix_atribut = [textwrap.TextWrapper(width=40).fill(text=l) for l in atribut]

    # print(df_olah)
    # print(atribut)
    # code here
    plt.figure(figsize=(12, 6))
    plt.title("Persentase Mahasiswa " + prodi + " " + fitur[2], pad=20)
    plt.pie(x=df_olah['NRP'], labels=fix_atribut, autopct=make_autopct(df_olah['NRP']), labeldistance=1.2,
            explode=explode)
    nama_file = secrets.token_hex(nbytes=16) + ".png"
    plt.savefig("../public_html/cdc/data_olah/" + nama_file)

    if (fitur[3] != None):
        rmv = '../public_html/cdc/data_olah/' + fitur[3]
        os.remove(rmv)

    cur = con.cursor()
    sql = "UPDATE fitur SET gambar=%s, updated=%s WHERE id_fitur=%s"
    record = (nama_file, date, id_fitur)
    cur.execute(sql, record)
    con.commit()

    return redirect("https://tracerstudy.itenas.ac.id/cdc/nonediting/olah_fitur/" + id_fitur + "/" + str(jml))

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.1f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def array_diff(a, b):
    return [x for x in a if x not in b]

def redirect_url():
    return request.referrer
if __name__ == '__main__':
    app.run()