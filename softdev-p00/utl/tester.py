#Team Bits Please
#SoftDev 1 pd1
#P00 -- Da Art of Storytellin'
#2019-10-28

import sqlite3
import random
import sys
from utl.db_builder import exec

#for creating randomly generated id numbers
limit = sys.maxsize
#==========================user functions===========================

#helper function for addUser
def addUserHelper(username, password, data):
    rand = random.randrange(limit)
    while (rand in data):
        #if the id is already in use
        rand = random.randrange(limit)
    #print(rand)
    command = "INSERT INTO user_tbl VALUES(" + str(rand) + ",\"" + username + "\",\"" + password + "\")"
    #print(command)
    exec(command)


#takes in username/password, generates user_id, adds them to user_tbl
def addUser(username, password):
    q = "SELECT * FROM user_tbl WHERE username = '%s';" % username
    data = exec(q).fetchone()
    if (data is None):
        q = "SELECT user_id FROM user_tbl;"
        data = exec(q).fetchall()
        addUserHelper(username,password,data)
        return True
    return False #if username already exists


#helper function for verifyUser
def verifyUserHelper(username, password, data):
    myEntry = (username, password)
    #print(myEntry)
    if (myEntry in data):
        #if user is in database
        return True
    return False


#takes in username/password, checks them to user_tbl
def verifyUser(username, password):
    q = "SELECT username,password FROM user_tbl;"
    data = exec(q).fetchall()
    return verifyUserHelper(username,password,data)

#==========================user get methods===========================

#takes in username, returns user_id from user_tbl
def getUserID(username):
    q = "SELECT user_id FROM user_tbl WHERE username = '%s';" % username
    data = exec(q).fetchone()
    return data


#str instead of tuple output of getUserID
def getUserIDStr(username):
    user_id = getUserID(username)
    return str(user_id[0])


#takes in user_id, returns username from user_tbl
def getUserInfo(user_id):
    q = "SELECT username FROM user_tbl WHERE user_id = '%s';" % user_id
    data = exec(q).fetchone()
    return data

#returns a tuple of all blogs in blog_tbl
def getAllUsers():
    q = "SELECT username, user_id FROM user_tbl"
    data = exec(q).fetchall()
    return data

#==========================user tests===========================

#addUser("Elizabeth","wow")
#addUser("Emily","this")
#addUser("Jackie","actually")
#addUser("Yaru","works")

#==========================blog functions===========================

#joins user_id for user_tbl and blog_tbl
#command="SELECT user_tbl.user_id FROM user_tbl LEFT JOIN blog_tbl ON user_tbl.user_id = blog_tbl.user_id"
#exec(command)


#helper function for addBlog
def addBlogHelper(user_id, title, data):
    rand = random.randrange(limit)
    while (rand in data):
        #if the id is already in use
        rand = random.randrange(limit)
    #print(rand)
    #print(command)
    command = "INSERT INTO blog_tbl VALUES(%s, %s, '%s')" % (rand, user_id, title)
    #print(command)
    exec(command)
    return rand


#takes in user_id/title, generates blog_id, adds them to blog_tbl, returns blog_id
def addBlog(user_id, title):
    title = title.strip()
    user_id = int(user_id)
    q = "SELECT * FROM blog_tbl WHERE user_id = %d AND title = '%s'" % (user_id, title)
    data = exec(q).fetchone()
    if (data is not None):
        return None
    q = "SELECT blog_id FROM blog_tbl WHERE user_id = %d;" % user_id
    data = exec(q).fetchall()
    return addBlogHelper(user_id, title, data)

#==========================blog get methods===========================

#takes in username/title, returns blog_id from blog_tbl
def getBlogID(username, title):
    user_id = getUserIDStr(username)
    q = "SELECT blog_id FROM blog_tbl WHERE user_id =" + user_id + " AND title=" + title + ";"
    data = exec(q).fetchone()
    return data


#str instead of tuple output of getBlogID
def getBlogIDStr(username, title):
    blog_id = getBlogID(username, title)
    return str(user_id[0])


#takes in blog_id, returns title from blog_tbl
def getBlogTitle(blog_id):
    q = "SELECT title FROM blog_tbl WHERE blog_id ='%s';" % blog_id
    data = exec(q).fetchone()
    return data

#str instead of tuple output of getBlogTitle
def getBlogTitleStr(blog_id):
    title = getBlogTitle(blog_id)
    if (title is None):
        return ""
    return str(title[0])

#takes in blog_id, returns user_id from blog_tbl
def getUserfromBlog(blog_id):
    q = "SELECT user_id FROM blog_tbl WHERE blog_id = '%s'" % blog_id
    data = exec(q).fetchone()
    return data

#str instead of tuple output of getUserfromBlog
def getUserfromBlogStr(blog_id):
    user = getUserfromBlog(blog_id)
    return str(user[0])

#takes in user_id, returns all blogs created by a user from blog_tbl
def getUserBlogs(user_id):
    q = "SELECT title, blog_id FROM blog_tbl WHERE user_id= '%s'" % user_id
    data = exec(q).fetchall()
    return data
#==========================blog tests===========================

#addBlog(1311963876, "Dogs")
#addBlog(2039603925, "Lions")
#addBlog(526656026, "Turtle")
#addBlog(389070385, "LionCity")
#addBlog(2039603925, "Greatest Lion")

#==========================entry functions===========================

#joins blog_id for blog_tbl and entry_tbl
#command="SELECT blog_tbl.blog_id FROM blog_tbl LEFT JOIN entry_tbl ON blog_tbl.blog_id = entry_tbl.blog_id"
#exec(command)

#helper function for addEntry
def addEntryHelper(blog_id, title, content, data):
    rand = random.randrange(limit)
    while (rand in data):
        #if id is already in use
        rand = random.randrange(limit)
    command = "INSERT INTO entry_tbl VALUES(%s, %s, '%s', '%s')" % (rand, blog_id, title, content)
    #print(command)
    return exec(command)

#takes in blog_id/title/content, generates entry_id, adds them to entry_tbl, returns entry_id
def addEntry(blog_id, title, content):
    title = title.strip()
    blog_id = int(blog_id)
    q = "SELECT * FROM entry_tbl WHERE blog_id = %d AND title='%s'" % (blog_id, title)
    data = exec(q).fetchone()
    print(data)
    if (data is not None):
        return None
    q = "SELECT blog_id FROM blog_tbl"
    data = exec(q).fetchall()
    return addEntryHelper(blog_id, title, content, data)

#takes in entry_id/title/content, adds them to entry_tbl for that entry
def editEntry(entry_id, blog_id, title, content):
    title = title.strip()
    entry_id = int(entry_id)
    blog_id = int(blog_id)
    q = "SELECT * FROM entry_tbl WHERE entry_id != %d AND title='%s' AND blog_id = %d" % (entry_id, title, blog_id)
    data = exec(q).fetchall()
    print(data)
    #print(len(data))
    if (len(data) > 0):
        return False
    q = "UPDATE entry_tbl SET title = '%s', content = '%s' WHERE entry_id = %d" % (title, content, entry_id)
    exec(q)
    return True

#takes in entry_id, deletes them from entry_tbl
def deleteEntry(entry_id):
    entry_id = int(entry_id)
    q = "DELETE FROM entry_tbl WHERE entry_id = %d" % entry_id
    data = exec(q)

#==========================entry get methods===========================

#takes in blog_id/title, returns entry_id from entry_tbl
def getEntryID(blog_id, title):
    q = "SELECT entry_id FROM entry_tbl WHERE blog_id ='%s' AND title='%s';" % (blog_id, title)
    data = exec(q).fetchone()
    return data

#str instead of tuple output of getEntryID
def getEntryIDStr(blog_id, title):
    entry_id = getEntryID(blog_id, title)
    return str(user_id[0])

#takes in entry_id, returns title from entry_tbl
def getEntryTitle(entry_id):
    q = "SELECT title FROM entry_tbl WHERE entry_id ='%s';" % entry_id
    data = exec(q).fetchone()
    if (data is None):
        return ""
    return str(data[0])

#takes in entry_id, returns content from entry_tbl
def getEntryContent(entry_id):
    q = "SELECT content FROM entry_tbl WHERE entry_id ='%s';" % entry_id
    data = exec(q).fetchone()
    if (data is None):
        return ""
    return str(data[0])

#takes in blog_id, returns all entries for that blog from entry_tbl
def getAllEntries(blog_id):
    q = "SELECT title, content, entry_id FROM entry_tbl WHERE blog_id= '%s'" % blog_id
    data = exec(q).fetchall()
    return data

#takes in entry_id, returns blog_id from entry_tbl
def getBlogfromEntry(entry_id):
    q = "SELECT blog_id FROM entry_tbl WHERE entry_id = '%s'" % entry_id
    data = exec(q).fetchone()
    return str(data[0])

#==========================entry tests===========================

#addEntry(230029172, "Dogs wow!", "Dogs are really cute!")
#addEntry(1216538388, "Lions > all", "Lions are really fierce!")

#==========================search function===========================

#returns a tuple of all blogs in blog_tbl
def getAllBlogs():
    q = "SELECT title, blog_id FROM blog_tbl"
    data = exec(q).fetchall()
    return data

#takes in search phrase, searches for all instances of that phrase from blog_tbl
#non case-sensitive
def findBlog(search):
    search = search.lower().strip()
    data = getAllBlogs()
    blogsList = []
    #creates a list of blogs with acceptable titles
    for blogT, blogID in data:
        title = str(blogT)
        #print(title)
        titleSmall = title.lower().strip()
        if search in titleSmall:
            blogsList.append(blogID)
            #print(blogsList)
    blogIDList = []
    #creates a list of tuples containing blog_id, title, user_id, and username
    for id in blogsList:
        q = "SELECT blog_id, title, user_id FROM blog_tbl WHERE blog_id=%d" % id
        data = exec(q).fetchone()
        data = data + getUserInfo(getUserfromBlog(str(data[0])))
        blogIDList.append(data)

    return blogIDList   #list of tuples

#list of str not list of tuples of findBlog
def findBlogStr(search):
    blogIDList = findBlog(search)
    strBlogIDS = []
    for blog_ids in blogIDList:
        newID = str(blog_ids[0])
        strBlogIDS.append(newID)
    return strBlogIDS

#==========================search tests===========================
#print(findBlogStr("LION"))
#print(findBlog("LION"))
