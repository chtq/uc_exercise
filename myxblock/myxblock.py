"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

import json
import thread
import datetime
import re

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Boolean
from xblock.fragment import Fragment

from config import Config
from lib_util import Util


class MyXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    logger = Util.uc_logger()

    src = String(default="", scope=Scope.content, help="url of the tiku")
    CONFIG = Config.CONFIG
    url = CONFIG["URL"]
 
    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the MyXBlock, shown to students
        when viewing courses.
        """
         # runtime error
        if not hasattr(self.runtime, "anonymous_student_id"):
            return self.message_view("Error  (get anonymous student id)", "Cannot get anonymous_student_id in runtime", context)

        if self.runtime.anonymous_student_id == "student": 
            context_dict = {
            "username": "",
            "email":"",
            "url":self.src
        }

            fragment = Fragment()
            fragment.add_content(Util.render_template('static/html/myxblock.html', context_dict))
            fragment.add_css(Util.load_resource("static/css/myxblock.css"))
            fragment.add_javascript(Util.load_resource("static/js/src/myxblock.js"))
            fragment.initialize_js("MyXBlock")
            return fragment

        student = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        email = student.email
        name = student.first_name + " " + student.last_name
        username = student.username
        
        if name == " ":
            name = username

        context_dict = {
            "username": username,
            "email":email,
            "url":self.src
        }

        fragment = Fragment()
        fragment.add_content(Util.render_template('static/html/myxblock.html', context_dict))
        fragment.add_css(Util.load_resource("static/css/myxblock.css"))
        fragment.add_javascript(Util.load_resource("static/js/src/myxblock.js"))
        fragment.initialize_js("MyXBlock")
        return fragment

    def studio_view(self, context=None):
        context_dict = {
            "title": "",
            "message": self.src
        }

        fragment = Fragment()
        fragment.add_content(Util.render_template('static/html/studio_view_new.html', context_dict))
        fragment.add_css(Util.load_resource("static/css/studio.css"))
        fragment.add_javascript(Util.load_resource("static/js/src/myxblock.js"))
        fragment.initialize_js("MyXBlock")
        return fragment
 

    def message_view(self, title, message, context=None):
        context_dict = {
            "title": title,
            "message": message
        }
        fragment = Fragment()
        fragment.add_content(Util.render_template('static/html/message_view.html', context_dict))
        fragment.initialize_js("MyXBlock")
        return fragment

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def studio_submit(self, data, suffix=""):
        self.logger.info("src"+ data["src"])
        self.src=data["src"]
        self.save()
        return {"result":True}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MyXBlock",
             """<vertical_demo>
                <myxblock/>
                <myxblock/>
                <myxblock/>
                </vertical_demo>
             """),
        ]

