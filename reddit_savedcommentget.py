import praw,time,myhtmllib

def addcommenttodoc(s,doc):
    doc.add('<font face="verdana">')
    
    doc.addlink(s.link_url,s.link_title)
    doc.add(" by ")
    if s.link_author != "[deleted]":
        doc.addlink("http://www.reddit.com/user/"+s.link_author,
                    s.link_author)
    else:
        doc.add(s.link_author)
    doc.add(" in ")
    doc.addlink("http://www.reddit.com/r/"+s.subreddit.display_name,
                s.subreddit.display_name)
    doc.add('</font>')
    doc.addreturn()
    doc.addline("<blockquote>")
    if s.author != None:
        if s.author.name != "[deleted]":
            doc.addlink("http://www.reddit.com/user/"+s.author.name,
                        s.author.name)
        else:
            doc.add(s.author.name)
    else:
        doc.add('[deleted]')
        
    doc.add("<b> "+str(s.score)+" points</b>")
    doc.add(" "+str(time.time()-s.created_utc)+
            " seconds"+" ago")
    doc.addreturn()
    doc.add(s.body_html)
    doc.addreturn()
    doc.addlink(s.permalink,"permalink")
    doc.add(" ")
    doc.addlink(s.permalink+"?context=3","context")
    doc.add(" ")
    doc.addlink(s.submission.permalink,
                "full comments ("+str(s.submission.num_comments)+")")
    doc.addline("</blockquote>")
    
def addsubmissiontodoc(s,doc):
    doc.add('<h3 style="float:left">'+str(s.score)+'</h3>')
    if s.thumbnail == 'self':
        doc.addlink(s.url,
                    '<img src="redditselfthumbnail.png" height= "70" width="70" style="float:left;"/>')
    elif s.thumbnail == 'default' or s.thumbnail == '':
        # reddit seems to dump thumbnails older than ~1600 days
        doc.addlink(s.url,
                    '<img src="redditdefaultthumbnail.png" height= "70" width="70" style="float:left;"/>')
    else:
        doc.addlink(s.url,
                    '<img src="'+s.thumbnail+'" height= "70" width="70" style="float:left;"/>')

    doc.add('<font face="verdana">')
    try:
        doc.addlink(s.url,s.title)
    except:
        # this is currently catching unicode bullshit
        doc.addlink(s.url,
                    ''.join([i if ord(i) < 128 else '*' for i in s.title])) 
    doc.add('</font>')
    doc.add(' ')
    if "self." in s.domain:
        doc.addlink('http://www.reddit.com/r/'+s.domain.replace('self.',''),
                    '('+s.domain+')')
    else:
        doc.addlink('http://www.'+s.domain,
                    '('+s.domain+')')
    doc.addreturn()
    doc.addlinebreak()

    if s.author != None:
        if s.author.name == 'redditads':
            doc.add(' promoted by ')
            doc.addlink('http://www.reddit.com/user/redditads','redditads')
        else:
            doc.add(' submitted '+str(time.time()-s.created_utc)+' seconds'+' ago')
            doc.add(' by ')
            doc.add('<a href="http://www.reddit.com/user/'+s.author.name+
                    '" >'+s.author.name+'</a>')
            doc.add(' to ')
            doc.add('<a href="http://www.reddit.com/r/'+s.subreddit.display_name+
                    '" >'+s.subreddit.display_name+'</a>')
    else:
        doc.add(' submitted '+str(time.time()-s.created_utc)+' seconds'+' ago')
        doc.add(' by ')
        doc.add('[deleted]')
        doc.add(' to ')
        doc.add('<a href="http://www.reddit.com/r/'+s.subreddit.display_name+
                '" >'+s.subreddit.display_name+'</a>')

    doc.addreturn()
    doc.addlinebreak()
    
    doc.addlink(s.permalink,
                str(s.num_comments)+" comments")
    
    doc.addreturn()
    doc.addlinebreak()
    doc.addreturn()
    doc.addlinebreak()

def main_saveunsavemethod(username,password):
    r = praw.Reddit(user_agent=username+"'s saved comment getter")

    # note that Reddit login won't work this way anymore
    # ...at some point
    # Pass ``disable_warning=True`` to ``login`` to disable the warning

    # if limit is greater than or equal to 1000, only 1000
    # saved posts will be returned
    allsaves = []
    while True:
        r.login(username,password,
                disable_warning=True)
        saved = list(r.user.get_saved(limit=1000))
        print len(saved)
        if len(saved) == 0:
            break
        for s in saved:
            allsaves.append(s)
            s.unsave()
        r.clear_authentication()
        
    r.login(username,password,
            disable_warning=True)
    doc = myhtmllib.document()
    for s in allsaves:
        if type(s).__name__ == "Comment":
            addcommenttodoc(s,doc)
        elif type(s).__name__ == "Submission":
            addsubmissiontodoc(s,doc)
        doc.addhorizontalrule()
        doc.addhorizontalrule()
    # you're still getting unicode errors while writing
    doc.write("dump.html")
    
    allsaves.reverse()
    for s in allsaves:
        s.save()

def getlogindetailsfromfile():
    f = open('redditlogindetails.txt','r')
    details = f.read().split('\n')
    f.close()
    return details[0].replace('username:',''),details[1].replace('password:','')

main_saveunsavemethod(*getlogindetailsfromfile())

print "Done"


