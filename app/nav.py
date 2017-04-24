from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator

from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION

# To keep things clean, we keep our Flask-Nav instance in here. We will define
# frontend-specific navbars in the respective frontend, but it is also possible
# to put share navigational items in here.

nav = Nav()

# Menu / navbar
nav.register_element('frontend_top', Navbar(
    View('Home', 'frontend.index'),
    Link('GitHub','https://github.com'),
    Subgroup(
        'Tropo',
        Link('My Tropo Apps', 'https://www.tropo.com/applications'),
        Link('My Tropo Logs', 'https://www.tropo.com/mylogs'),
        Link('Python Module', 'https://github.com/rsp2k/ciscotropowebapi'),
        Link('SparkLog4Tropo', 'https://gist.github.com/ObjectIsAdvantag/b73db0cffcedb1152a2d6669cb3d27b0'),
        Link('WebAPI Docs', 'https://www.tropo.com/docs/webapi'),
        Link('Forums', 'https://support.tropo.com/hc/en-us/community/topics'),
        Link('IRC Chat', 'https://www.tropo.com/help/irc-chat/'),
        Link('Coding Tips', 'https://www.tropo.com/docs/coding-tips'),
        Link('Developer Network', 'https://www.tropo.com/tropo-developer-network/'),
    ),
    Subgroup(
        'Spark',
        Link('My Spark Apps', 'https://developer.ciscospark.com/apps.html'),
        Link('Python Module', 'https://github.com/CiscoDevNet/ciscosparkapi'),
        Link('Quick Reference', 'https://developer.ciscospark.com/quick-reference.html'),
        Link('WebHooks', 'https://developer.ciscospark.com/webhooks-explained.html'),
        Link('Bots', 'https://developer.ciscospark.com/bots.html'),
        Link('Admin API', 'https://developer.ciscospark.com/admin-api.html'),
        Link('JS SDK Download', 'https://www.npmjs.com/package/ciscospark'),
        Link('JS SDK Docs', 'https://ciscospark.github.io/spark-js-sdk/api/'),
        Link('Innovation Fund', 'https://developer.ciscospark.com/fund/'),
    ),
   Subgroup(
       'Python',
       Link('Beginners Guide', 'https://wiki.python.org/moin/BeginnersGuide/'),
       Link('Awesome Python', 'https://github.com/vinta/awesome-python'),
       Link('WSGI', 'https://www.python.org/dev/peps/pep-3333/'),
       Link('v3.6 Docs', 'https://docs.python.org/3/'),
       Link('Learn Python the Hard Way', 'https://learnpythonthehardway.org/book/'),
       Link('PyVideo', 'http://pyvideo.org/'),
    ),
    Subgroup(
        'Flask',
        Link('Discover Flask', 'https://github.com/realpython/discover-flask'),
        Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
        Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
        Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
        Link('Flask-DebugToolbar', 'https://flask-debugtoolbar.readthedocs.io'),
    ),
    Subgroup(
       'Bootstrap',
       Link('Getting started', 'http://getbootstrap.com/getting-started/'),
       Link('CSS', 'http://getbootstrap.com/css/'),
       Link('Components', 'http://getbootstrap.com/components/'),
       Link('Javascript', 'http://getbootstrap.com/javascript/'),
       Link('Customize', 'http://getbootstrap.com/customize/'), ),
    Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)), ))
