#Team Bits Please
#SoftDev1 pd1
#P00: Da Art of Storytellin'
#2019-10-28

from flask import Flask, render_template, session, url_for, request, redirect, flash
from utl import db_builder, tester
import os
from datetime import date

app = Flask(__name__)
#session secret key, code from Stack Overflow
app.secret_key = '\xa1\xafO[\xddQ\xb2\x94@\x16\xcb@3\x92#B'
DIR = os.path.dirname(__file__) or '.'
DIR += '/'

@app.route("/")
def root():
    if ("userid" in session): #if signed in, go to profile
        return redirect(url_for('profile'))
    return redirect(url_for('sign')) #else go to sign-in options

#welcome page with sign-in options
@app.route("/welcome")
def sign():
    if ("userid" in session): #if signed in, go to profile
        return redirect(url_for('profile'))
    return render_template('welcome.html')

#register for an account
@app.route("/register")
def register():
    if ("userid" in session): #if signed in, go to profile
        return redirect(url_for('profile'))
    return render_template('register.html')

#process register form
@app.route("/adduser", methods=['POST'])
def adduser():
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    if (username == '' or password == ''):
        flash('Fields cannot be left empty', 'red')
        return redirect(url_for('register'))
    if (textError(username) or textError(password)):
        flash('Please input values without quotes!', 'red')
        return redirect(url_for('register'))
    #print(request.method)
    #print(username)
    #print(password)
    if (password != confirm): #passwords do not match
        flash('Passwords do not match!', 'red')
        return redirect(url_for('register'))
    added = tester.addUser(username, password) #returns True if added successfully, false if username take
    if (added):
        flash('You have been registered successfully. Please log in.', 'green')
        return redirect(url_for('login'))
    flash('Username already taken.', 'red')
    return redirect(url_for('register'))

#log in to account
@app.route("/login")
def login():
    if ("userid" in session): #if signed in, go to profile
        return redirect(url_for('profile'))
    return render_template('login.html')

#process login form
@app.route("/auth", methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    verified = tester.verifyUser(username, password) #returns True if logged in successfully, false if otherwise
    if (verified):
        id = tester.getUserIDStr(username)
        session["userid"] = id
        flash('You have logged in successfully.', 'green')
        return redirect(url_for('profile', id=id))
    flash('Error with logging in', 'red')
    return redirect(url_for('login'))

## USER MAY NOT PROCEED PAST HERE WITHOUT BEING LOGGED IN ##

#user profile page
@app.route("/user")
def profile():
    #this code is reused throughout all the functions to check if user is logged in
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    username = tester.getUserInfo(session['userid'])[0]
    #print(request.args['id'])
    if (request.args): #if url has query string
        if ('id' in request.args): #if url has id
            id = request.args['id']
            name = tester.getUserInfo(id) #get username from id query
            if (name): #if id is valid user id
                name = name[0] #retrieve username from tuple
                isOwner = False #checks if logged in user "owns" the profile
                isOwner = False #checks if logged in user "owns" the profile
                isOwner = False #checks if logged in user "owns" the profile
                if (id == session['userid']): #if logged in user matches owner of blog
                    isOwner = True
                blogs = tester.getUserBlogs(id) #get all blogs based on id query
                return render_template('profile.html', username=username, owner=name, isOwner=isOwner, blogs=blogs) #success!
            flash('No profile was found for the given url. You have been redirected back to your own profile.', 'red') #if id is not valid user_id
        else:
            flash('No profile was found for the given url. You have been redirected back to your own profile.', 'red') #if url does not have id query
    return redirect(url_for('profile', id=session["userid"])) #if url does not have querystring, return to "My Profile"

#about page with instructions on running the site
@app.route("/about")
def about():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    username = tester.getUserInfo(session['userid'])[0]
    users = tester.getAllUsers()
    return render_template('about.html', username=username, users=users)

#search page with search bar
@app.route("/search")
def search():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    username = tester.getUserInfo(session['userid'])[0]
    results = [] #when user first visits search page, no results are displayed
    if (request.args): #if user has made a search
        if ('query' in request.args):
            query = request.args['query'] #search keyword
            results = tester.findBlog(query) #results of search
            #print(results)
    return render_template('search.html', username=username, results=results)

#process search query
@app.route("/query", methods=['POST'])
def query():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    query = request.form['keyword']
    return redirect(url_for('search', query=query)) #display results on search page

#form to create a blog
@app.route("/createblog")
def createblog():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    username = tester.getUserInfo(session['userid'])[0]
    return render_template('createblog.html', username=username)

#process form to create a blog
@app.route("/updateblog", methods=['POST'])
def updateblog():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    title = request.form['title']
    if (textError(title)):
        flash("Please enter a title without quotes!", 'red')
        return redirect(url_for('createblog'))
    if (title == ''): #if no title entered
        flash('Fields cannot be empty', 'red')
        return redirect(url_for('createblog'))
    #print(title)
    id = tester.addBlog(session['userid'], title) #returns None if blog title used already by that user, else ID of blog created
    if (id == None):
        flash('You have already used this title', 'red')
        return redirect(url_for('createblog'))
    return redirect(url_for('blog', id=id))

#blog page which also displays all entries in the blog
@app.route("/blog")
def blog():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    if (request.args): #if querystring exists
        if ('id' in request.args): #if id query exists
            id = request.args['id']
            name = tester.getBlogTitleStr(id) #get blog title from ID, returns None if ID is not associated with any blog
            if (name): #if blog_id is associated with valid blog
                session['blogid'] = id #store current blog that is being visited in session, useful for knowing where to add entries later without using queries
                isOwner = False #default value
                user_id = tester.getUserfromBlog(id)[0] #get user_id associated with blog_id
                ownername = tester.getUserInfo(user_id)[0] #get username from user_id
                if (int(user_id) == int(session['userid'])): #if owner of blog matches logged in user
                    isOwner = True
                userlink = "/user?id=%s" % user_id #click link to access user profile from blog
                entries = tester.getAllEntries(id) #get all entries from blog based on blog_id
                username = tester.getUserInfo(session['userid'])[0]
                return render_template('blog.html', username=username, ownername=ownername, isOwner=isOwner, title=name, userlink=userlink, entries=entries)
            else: #blog_id given in query is not valid
                flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
        else: #no id query found
            flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
    else: #no querystring
        flash('No blog was found for the given URL. You have been redirected back to your own profile.', 'red')
    return redirect(url_for('profile', id=session['userid']))

#form to create a blog entry
@app.route("/editentry")
def editentry():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    username = tester.getUserInfo(session['userid'])[0]
    temp_title = "" #if starting a new entry, blank title
    temp_content = "" #if starting a new entry, blank content
    link = "/updateentry" #link to process form
    if (request.args): #if query string exists (editing an entry)
        if ('id' in request.args): #if id query exists
            id = request.args['id'] #if editing an entry, URl will contain ID querystring
            temp_title = tester.getEntryTitle(id) #pre-fill title box with current title
            temp_content = tester.getEntryContent(id) #pre-fill content box with current content
            link = link + "?id=%s" % id #generate link to go to process form
    return render_template('createentry.html', username=username, temp_title=temp_title, temp_content=temp_content, link=link)

#process form to create a blog entry
@app.route("/updateentry", methods=['POST'])
def updateentry():
    if ("userid" not in session):
      flash('You must log in to access this page!', 'red')
      return redirect(url_for('login'))
    title = request.form['title']
    content = request.form['content']
    id = session['blogid']
    if (request.args): #if query string exists (editing an entry)
        if ('id' in request.args): #if id query exists
            entry_id = request.args['id']
            if (textError(title) or textError(content)): #if quotes found
                flash("Please input values without quotes!", 'red')
                return redirect(url_for('editentry', id=entry_id))
            if (title == '' or content == ''): #if empty submission
                flash('Fields cannot be empty', 'red')
                return redirect(url_for('editentry', id=entry_id))
            entry = tester.editEntry(entry_id, id, title, content) #edit entry, returns False if name is already being used
            if (not entry):
                flash("Title is already being used for another post", 'red')
                return redirect(url_for('editentry', id=entry_id))
    else: #if creating a new entry
        if (textError(title) or textError(content)): #if quotes found
            flash("Please input values without quotes!", 'red')
            return redirect(url_for('editentry'))
        if (title == '' or content == ''): #if empty submission
            flash('Fields cannot be empty', 'red')
            return redirect(url_for('editentry'))
        entry = tester.addEntry(id, title, content) #returns None if title is already used for that blog
        if (entry == None):
            flash("You have already used this heading", 'red')
            return redirect(url_for('editentry'))
    return redirect(url_for('blog', id=id))

@app.route('/deleteentry')
def deleteentry():
    if ("userid" not in session):
        flash('You must log in to access this page!', 'red')
        return redirect(url_for('login'))
    id = session['blogid']
    if (request.args):
        if ('id' in request.args):
            entry_id = request.args['id']
            tester.deleteEntry(entry_id)
    return redirect(url_for('blog', id=id))

#logout page
@app.route("/logout")
def logout():
    session.clear() #clear info stored in session
    flash('You have been successfully logged out.', 'green')
    return redirect(url_for('root'))

def textError(string):
    if ("'" in string or "\"" in string):
        return True
    return False

if __name__ == "__main__":
    db_builder.build_db()
    app.debug = True
