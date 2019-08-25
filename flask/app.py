#!/usr/bin/env python2.7

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import SQLAlchemyError, DataError, IntegrityError
#from psycopg2 import DataError,IntegrityError
from flask import Flask, request, render_template, g, redirect, Response, session, escape, url_for
import json



#define template directory
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=tmpl_dir,static_folder=static_dir)

app.config.update()

#######################################################################################

#DATABASE ENGINE SETUP

#URI for database access
DATABASEURI = "postgresql://bsk2133:chrds156932%@104.196.135.151/proj1part2"

engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback; traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
    try:
        g.conn.close()
    except Exception as e:
        pass

#########################################################################################

@app.route('/')
def index():
    # DEBUG: this is debugging code to see what request looks like
    print(request.args)

    if 'email' in session:
        username = session['email']
    else:
        username = ""

    context = dict(username=username,message="")
    return render_template("index.html",**context)


@app.route('/register', methods=['GET','POST'])
def register():
    if 'email' in session:
        username = session['email']
    else:
        username = ""

    context = dict(username=username,message="")

    if request.method == 'GET':

        pass

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        name = request.form['name']
        university = request.form['university']

        try:
            g.conn.execute('INSERT INTO student_attends VALUES (%s,%s,%s,%s,%s)',email,name,gender,university,password)
            context['message'] ="Registration Succesful."
        except DataError:
            context['message'] ="Sorry, input exceeds allowed length. Please try again."
        except IntegrityError:
             context['message'] ="Sorry, that email is already taken. Please try again or go to the login page to login."
        except SQLAlchemyError:
             context['message'] ="Database Error. Please try again."
 
    #load list of university names from database
    cursor = g.conn.execute("SELECT uname FROM Universities")
    universities = []
    for result in cursor:
        universities.append(result['uname'])
    cursor.close()
    context['universities'] = universities

    return render_template("register.html",**context)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'email' in session:
        username = session['email']
    else:
        username = ""

    context = dict(username=username)

    if request.method == 'POST':

        cursor = g.conn.execute(
                "SELECT stemail,stpass FROM student_attends WHERE stemail=%s"
                ,request.form['email'])
        login_info = cursor.fetchone()
        cursor.close()

        if login_info is None:
            context['message'] = "Sorry, no user with that email found. Please try again."
            return render_template("login.html",**context)
        else:
            if request.form['password'] != login_info[1]:
                context['message'] = "Sorry, wrong password. Please try again."
                return render_template("login.html",**context)
            else:
                session['email'] = request.form['email']
                context['message'] = "Login Successful."
                return redirect(url_for("profile"))

    if request.method == 'GET':
        return render_template("login.html",**context)


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if 'email' in session:
        username = session['email']
    else:
        return redirect(url_for("return_home"))

    uname = g.conn.execute("SELECT uname FROM student_attends WHERE student_attends.stemail=%s",username).fetchone()['uname']

    context = dict(username=username, message='')

    if request.method == 'GET':
        cursor = g.conn.execute("SELECT gname FROM member_of WHERE stemail=%s",username)
        groups = []
        for result in cursor:
            groups.append(result['gname'])
        cursor.close()

        context['groups'] = groups

        print(groups)

        all_groups_data = dict()

        if groups:
            for gname in groups:

                x = dict()

                cursor = g.conn.execute("SELECT votes.stitle,votes.sartist,songs.syear,SUM(votes.vscore) FROM votes,songs WHERE votes.gname=%s AND votes.uname=%s AND songs.stitle=votes.stitle AND songs.sartist=votes.sartist GROUP BY votes.stitle,votes.sartist,songs.syear ORDER BY SUM(votes.vscore) DESC  LIMIT 5", gname,uname)
                top_songs = []
                for result in cursor:
                    top_songs.append((result['stitle'],result['sartist'],result['syear'],result[3]))  # can also be accessed using result[0]
                cursor.close()

                x["top_songs"] = top_songs

                print(x)

                cursor = g.conn.execute("SELECT stitle,sartist,vtimestamp,vscore FROM votes WHERE votes.gname=%s AND votes.uname=%s ORDER BY vtimestamp DESC LIMIT 10", gname,uname)
                recent_votes = []
                for result in cursor:
                    recent_votes.append((result['stitle'],result['sartist'],result['vtimestamp'],result['vscore']))  # can also be accessed using result[0]
                cursor.close()

                x["recent_votes"] = recent_votes

                all_groups_data[gname] = x

                context['all_groups_data'] = all_groups_data

                print(type(all_groups_data))

        else:
            context['message'] = "You're currently not in any groups."
            context['all_groups_data'] = dict()

        print(type(all_groups_data))
        print(context['message'])

        return render_template("profile.html",**context)

@app.route('/groups', methods=['GET', 'POST'])
def groups():

    if 'email' in session:
        username = session['email']
    else:
        return redirect(url_for("return_home"))

    uname = g.conn.execute("SELECT uname FROM student_attends WHERE student_attends.stemail=%s",username).fetchone()['uname']

    context = dict(username=username, message='')

    if request.method == 'GET':
    
        pass

    if request.method == 'POST':

        date = request.form['date']

        if request.form['mode'] == "join":
            gname = request.form['join_group']
            role = request.form['join_group_role']

            try:
                g.conn.execute('INSERT INTO member_of VALUES (%s,%s,%s,%s,%s)',username,gname,uname,role,date)
                context['message']="Successfully joined group " + gname + " as " + role + "."
            except DataError:
                context['message'] ="Sorry, input exceeds allowed length. Please try again."
            except IntegrityError:
                 context['message'] ="You are already part of this group."
            except SQLAlchemyError:
                 context['message'] ="Database Error. Please try again."
     
        elif request.form['mode'] == "leave":
            gname = request.form['leave_group']

            g.conn.execute(
                    'DELETE FROM member_of WHERE gname=%s AND stemail=%s',gname,username)

            context['message']="Successfully removed from group " + gname + "."

        else:
            if request.form['group_type'] == "club":
                gname = request.form['club_name']
                ctype = request.form['club_type']

                try:
                    g.conn.execute('INSERT INTO group_part_of VALUES (%s,%s,%s)',gname,uname,date)
                    g.conn.execute('INSERT INTO clubs VALUES (%s,%s,%s)',gname,uname,ctype)
                    g.conn.execute('INSERT INTO playlist_for_group VALUES (%s,%s)',gname,uname)
                    context['message']="Successfully created club " + gname + "."
                except DataError:
                    context['message'] ="Sorry, input exceeds allowed length. Please try again."
                except IntegrityError:
                    context['message'] ="Sorry, group already exists."
                except SQLAlchemyError:
                    context['message'] ="Database Error. Please try again."
                
            elif request.form['group_type'] == "major":
                gname = request.form['major_name']
                mtype = request.form['major_type']
                
                try:
                    g.conn.execute('INSERT INTO group_part_of VALUES (%s,%s,%s)',gname,uname,date)
                    g.conn.execute('INSERT INTO majors VALUES (%s,%s,%s)',gname,uname,mtype)
                    g.conn.execute('INSERT INTO playlist_for_group VALUES (%s,%s)',gname,uname)
                    context['message']="Successfully created major " + gname + "."
                except DataError:
                    context['message'] ="Sorry, input exceeds allowed length. Please try again."
                except IntegrityError:
                    context['message'] ="Sorry, group already exists."
                except SQLAlchemyError:
                    context['message'] ="Database Error. Please try again."
                

            elif request.form['group_type'] == "residence":
                gname = request.form['residence_name']
                rtype = request.form['residence_type']
    
                try:
                    g.conn.execute('INSERT INTO group_part_of VALUES (%s,%s,%s)',gname,uname,date)
                    g.conn.execute('INSERT INTO residences VALUES (%s,%s,%s)',gname,uname,rtype)
                    g.conn.execute('INSERT INTO playlist_for_group VALUES (%s,%s)',gname,uname)
                    context['message']="Successfully created residence " + gname + "."
                except DataError:
                    context['message'] ="Sorry, input exceeds allowed length. Please try again."
                except IntegrityError:
                    context['message'] ="Sorry, group already exists."
                except SQLAlchemyError:
                    context['message'] ="Database Error. Please try again."
 
            elif request.form['group_type'] == "class":
                gname = "Class of " + request.form['class_year']

                try:
                    g.conn.execute('INSERT INTO group_part_of VALUES (%s,%s,%s)',gname,uname,date)
                    g.conn.execute('INSERT INTO classes VALUES (%s,%s)',gname,uname)
                    g.conn.execute('INSERT INTO playlist_for_group VALUES (%s,%s)',gname,uname)
                    context['message']="Successfully created class " + gname + ", " + uname + "."
                except DataError:
                    context['message'] ="Sorry, input exceeds allowed length. Please try again."
                except IntegrityError:
                    context['message'] ="Sorry, group already exists."
                except SQLAlchemyError:
                    context['message'] ="Database Error. Please try again."
            
            else:
                gname = request.form['group_name']

                try:
                    g.conn.execute('INSERT INTO group_part_of VALUES (%s,%s,%s)',gname,uname,date)
                    g.conn.execute('INSERT INTO playlist_for_group VALUES (%s,%s)',gname,uname)
                    context['message']="Successfully created group " + gname + "."
                except DataError:
                    context['message'] ="Sorry, input exceeds allowed length. Please try again."
                except IntegrityError:
                    context['message'] ="Sorry, group already exists."
                except SQLAlchemyError:
                    context['message'] ="Database Error. Please try again."
            

    cursor = g.conn.execute("SELECT gname FROM member_of WHERE stemail=%s",username)
    possible_leave_groups = []
    for result in cursor:
        possible_leave_groups.append(result['gname'])
    cursor.close()

    context['possible_leave_groups'] = possible_leave_groups

    cursor = g.conn.execute("SELECT DISTINCT gname FROM group_part_of WHERE uname=%s AND gname NOT IN (SELECT gname FROM member_of WHERE stemail=%s)" ,uname,username)

    possible_join_groups = []
    for result in cursor:
        possible_join_groups.append(result['gname'])
    cursor.close()

    context['possible_join_groups'] = possible_join_groups

    return render_template("groups.html",**context)

@app.route('/songs', methods=['GET', 'POST'])
def songs():

    if 'email' in session:
        username = session['email']
    else:
        return redirect(url_for("return_home"))

    uname = g.conn.execute("SELECT uname FROM student_attends WHERE student_attends.stemail=%s", username).fetchone()['uname']
    context = dict(username=username, message='')

    cursor = g.conn.execute("SELECT gname FROM member_of WHERE member_of.stemail=%s", username)
    gname_lst = []
    for result in cursor:
        gname_lst.append(result['gname'])
    cursor.close()

    if request.method == 'GET':

        pass

    elif request.method == 'POST':

        date = request.form['date']

        if request.form['mode'] == "vote":

            stitle_artist = request.form['vote_song']
            l = stitle_artist.split(" by ")
            stitle = l[0]
            sartist = l[1]

            score = request.form['score']

            for gname in gname_lst:

                cursor = g.conn.execute("SELECT * FROM is_on WHERE gname=%s AND uname=%s AND stitle=%s AND sartist=%s", gname,uname,stitle,sartist)
                s = cursor.fetchone()
                cursor.close()

                if s is None:
                    g.conn.execute('INSERT INTO is_on VALUES (%s,%s,%s,%s)',gname,uname,stitle,sartist)

                g.conn.execute('INSERT INTO votes VALUES (%s,%s,%s,%s,%s,%s,%s)',username,stitle,sartist,gname,uname,score,date)

                if score == "1":
                    context['message']="Successfully liked " + stitle + " by " + sartist + "."
                elif score == "-1":
                    context['message']="Successfully disliked " + stitle + " by " + sartist + "."

            if not gname_lst:
                context['message'] = "Sorry, you're not in any groups. Go to the manage groups page to join new groups before voting."

        elif request.form['mode'] == "play":
            
            stitle_artist = request.form['play_song']
            l = stitle_artist.split(" by ")
            stitle = l[0]
            sartist = l[1]

            for gname in gname_lst:

                cursor = g.conn.execute("SELECT * FROM is_on WHERE gname=%s AND uname=%s AND stitle=%s AND sartist=%s", gname,uname,stitle,sartist)
                s = cursor.fetchone()
                cursor.close()

                if s is None:
                    g.conn.execute('INSERT INTO is_on VALUES (%s,%s,%s,%s)',gname,uname,stitle,sartist)

                g.conn.execute('INSERT INTO plays VALUES (%s,%s,%s,%s,%s,%s)',username,stitle,sartist,gname,uname,date)

                context['message']="Successfully played " + stitle + " by " + sartist + "."
 
            if not gname_lst:
                context['message'] = "Sorry, you're not in any groups. Go to the manage groups page to join new groups before playing."

        else:
            stitle = request.form['stitle']
            sartist = request.form['sartist']
            syear = request.form['syear']

            try:
                g.conn.execute('INSERT INTO songs VALUES (%s,%s,%s)',stitle,sartist,syear)
                context['message']="Successfully added " + stitle + " by " + " to the list. It is now available to vote on and play!"
            except DataError:
                context['message'] ="Sorry, input exceeds allowed length. Please try again."
            except IntegrityError:
                context['message'] ="Song already exists."
            except SQLAlchemyError:
                context['message'] ="Database Error. Please try again."

    cursor = g.conn.execute("SELECT DISTINCT stitle, sartist FROM songs")
    possible_choose_songs = []
    songs_artists = []
    for result in cursor:
        possible_choose_songs.append(result['stitle'] + " by " + result['sartist'])
        songs_artists.append((result['stitle'],result['sartist']))
    cursor.close()

    context['possible_choose_songs'] = possible_choose_songs
    context['songs_artists'] = songs_artists

    return render_template("songs.html",**context)

@app.route('/explore', methods=['GET', 'POST'])
def explore():

    if 'email' in session:
        username = session['email']
    else:
        return redirect(url_for("return_home"))

    context = dict(username=username, message='')

    #load list of university names from database
    cursor = g.conn.execute("SELECT uname FROM Universities")
    universities = []
    for result in cursor:
        universities.append(result['uname'])  # can also be accessed using result[0]
    cursor.close()

    context['universities'] = universities

    options = dict()

    for u in universities:
        cursor = g.conn.execute("SELECT gname FROM group_part_of WHERE uname=%s",u)
        groups = []
        for result in cursor:
            groups.append(result['gname'])  # can also be accessed using result[0]
        options[u] = groups
        cursor.close()

    context['options'] = options

    if request.method == 'GET': 

        pass

    if request.method == 'POST':

        uname = request.form['university']
        gname = request.form['group']

        context['university_name'] = uname
        context['group_name'] = gname

        cursor = g.conn.execute("SELECT votes.stitle,votes.sartist,songs.syear,SUM(votes.vscore) FROM votes,songs WHERE votes.gname=%s AND votes.uname=%s AND songs.stitle=votes.stitle AND songs.sartist=votes.sartist GROUP BY votes.stitle,votes.sartist,songs.syear ORDER BY SUM(votes.vscore) DESC  LIMIT 5", gname,uname)
        top_songs = []
        for result in cursor:
            top_songs.append((result['stitle'],result['sartist'],result['syear'],result[3]))  # can also be accessed using result[0]
        cursor.close()
        context['top_songs'] = top_songs

        cursor = g.conn.execute("SELECT stitle,sartist,vtimestamp,vscore FROM votes WHERE votes.gname=%s AND votes.uname=%s ORDER BY vtimestamp DESC LIMIT 10", gname,uname)
        recent_votes = []
        for result in cursor:
            recent_votes.append((result['stitle'],result['sartist'],result['vtimestamp'],result['vscore']))  # can also be accessed using result[0]
        cursor.close()
        context['recent_votes'] = recent_votes

    return render_template("explore.html",**context)

@app.route('/return_home',methods=['GET'])
def return_home():
    return render_template("return.html")

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()