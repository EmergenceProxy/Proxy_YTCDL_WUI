from flask import Flask, redirect, url_for, request, render_template, session
from pyCode.pageSketchBook import drawHTML
from authlib.integrations.flask_client import OAuth #AWS Cognito library
import os #AWS Cognito library
# from dominate.tags import *
# from dominate import document


app = Flask(__name__)

#AWS Cognito integration
app.secret_key = os.urandom(24)  # Use a secure random key in production
oauth = OAuth(app)

oauth.register(
  name='oidc',
  authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_G2BaxE5ce',
  client_id='9pf0mnv8c2d7tahf5homs3qlu',
  client_secret='<client secret>',
  server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_G2BaxE5ce/.well-known/openid-configuration',
  client_kwargs={'scope': 'phone openid email'}
)

myArtist =  drawHTML()
htmlDir = "/home/proxyApps/appData/ytcData"
workingDir = "/home/proxyApps/appData/ytcData"
    
#################################################Dominate Examples#################################

def drawDominateExample():
    doc = document(title='My Dominate Example')

    with doc.head:
        link(rel='stylesheet', href='login2_style.css')
        script(type='text/javascript', src='script.js')
        style("""
            body {
              background-color: #f0f0f0;
              font-family: sans-serif;
            }
            """)

    with doc:
        h1('Hello from Dominate!')
        p('This is a paragraph generated using the Dominate library.')
        ul(li('Item 1'), li('Item 2'), li('Item 3'))

    # print(doc.render(pretty=True))
    return doc.render(pretty=True)

# @app.route('/')
# def hello():
#         return 'Hello from Flask on EC2!'


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

################################### AWS Cognito integration ###########################
@app.route('/')
def index():
    user = session.get('user')
    print(f"=================index: {user}")
    app.logger.info(f"=================index: {user}") # (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    app.logger.warning(f"=================index: {user}")

    if user:
        return  f'Hello, {user["email"]}. <a href="/logout">Logout</a>'

    else:
        return (f' '
                f'Welcome! Please <a href="/cog_login">Login</a>.'
                f'<p>Or if you\'re leaving =[ <p>Goodbye! Click <a href="/logout">Logout</a>.')

@app.route('/cog_login')
def cog_login():
    print(f"====================Start cog_login.")
    # Alternate option to redirect to /authorize
    redirect_uri = url_for('authorize', _external=True)
    print(f"cog_login: redirect_uri: {redirect_uri}")
    # return oauth.oidc.authorize_redirect(redirect_uri)

    return oauth.oidc.authorize_redirect('https://d84l1y8p4kdic.cloudfront.net')

@app.route('/authorize')
def authorize():
    print(f"Start authorize.")

    token = oauth.oidc.authorize_access_token()
    print(f"authorize: token: {token}")

    user = token['userinfo']
    print(f"authorize: user: {user}")

    session['user'] = user

    return load_youtube(user)
    # return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
    #return redirect("http://18.225.8.106/")

# if __name__ == '__main__':
#     app.run(debug=True)

####################################### Youtube Methods ###################################

@app.route('/<username>/youtube/')
def alt_load_youtube(username):
    print("Start: alt_load_youtube")
    return load_youtube(username)
    # return redirect(url_for('load_youtube', name=username))

@app.route('/<name>/youtube')
def load_youtube(name):
    print("Start: load_youtube")
    youtubeCommentPageHtml = myArtist.drawYoutubeDownloader(name)
    return youtubeCommentPageHtml
    #return 'welcome %s' % name
    
@app.route('/<name>/youtube/view_comments', methods=['GET'])
def load_youtube_comments(name):
    print("Start: load_youtube_comments")
    # user = request.form['nm']
    # userPW = request.form['pw']
    #this file should only: pass the request down to python, or send HTML with data back to user.
    youtubeCommentPageHtml = myArtist.selectPainting(name, request)
    
    return youtubeCommentPageHtml
    #return 'welcome %s' % name

@app.route('/<name>/youtube/search_comments_author', methods=['GET'])
def search_comments_author(name):
    print("Start: search_comments_author")
    youtubeCommentPageHtml = myArtist.selectPainting(name, request)
    return youtubeCommentPageHtml
    pass

@app.route('/<name>/youtube/search_comments_text', methods=['GET'])
def search_comments_text(name):
    print("Start: search_comments_text")
    youtubeCommentPageHtml = myArtist.selectPainting(name, request)
    return youtubeCommentPageHtml
    pass

@app.route('/<name>/youtube/search_comments_cid', methods=['GET'])
def search_comments_cid(name):
    print("Start: search_comments_cid")
    youtubeCommentPageHtml = myArtist.selectPainting(name, request)
    return youtubeCommentPageHtml
    pass

@app.route('/<name>/youtube/sort_most_comments', methods=['GET'])
def sort_most_comments(name):
    print("Start: sort_most_comments")
    youtubeCommentPageHtml = myArtist.selectPainting(name, request)
    return youtubeCommentPageHtml
    pass

@app.route('/<name>/youtube/sort_author_alpha', methods=['GET'])
def sort_author_alpha(name):
    print("Start: sort_author_alpha")
    youtubeCommentPageHtml = myArtist.selectPainting(name, request)
    return youtubeCommentPageHtml
    pass

@app.route('/<name>/youtube/sort_most_common_words', methods=['GET'])
def sort_most_common_words(name):
    print("Start: sort_most_common_words")
    youtubeCommentPageHtml = myArtist.selectPainting(name, request)
    return youtubeCommentPageHtml
    pass

@app.route('/<name>/youtube/tables', methods=['GET'])
def display_tables(name):
    print("Start: display_tables")
    youtubeCommentPageHtml = myArtist.drawYoutubeTables(name)
    return youtubeCommentPageHtml
    pass

###########################################Login Methods##########################################

@app.route('/<name>/pwtool')
def load_pwtool(name):
    pwToolPageHtml = myArtist.drawPWTool()
    return pwToolPageHtml
    #return 'welcome %s' % name


@app.route('/login_Test', methods=['POST', 'GET'])
def login_Test():
    userList = ["proxy", "irf", "gio", "njefferson"]
    print(f"login: request: {request}")
    print(f"login: request.method: {request.method}")
    print(f"login: request.form: {request.form}")
    user = ""
    if request.method == 'POST':
        user = request.form['usrnm']
        userPW = request.form['usrpw']

        print(f"login: user: {user}")
        print(f"login: userPW: {userPW}")
        return redirect(url_for('load_youtube', name=user))
    elif request.method == 'GET':
        return render_template('login2_template.html')

    return '404 error username not authorized %s' % user

@app.route('/login', methods=['POST', 'GET'])
def login():
    userList = ["proxy", "irf", "gio"]
    if request.method == 'POST':
        user = request.form['nm']
        userPW = request.form['pw']
        
        print(f"login: user: {user}")
        print(f"login: userPW: {userPW}")
        
        # if(user in userList):
        if (user):
            MATCH = {
                'youtube': 'load_youtube',
                'pwtool': 'load_pwtool'
            }
            
            try:
                MATCH[userPW]
                return redirect(url_for(MATCH[userPW], name=user))
            except KeyError:
                raise NotImplementedError(f"Running {userPW} page not implemented.")
        else:
            return redirect(url_for('success', name=user))
    else:#GET request
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

###################################################################################################

if __name__ == '__main__':
    app.run(debug=True)