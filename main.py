#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re


page_header = '''
<html>
<head>

<title>Caesar</title>
</head>
<body>
'''

form="""
    <h1>Please Register an Account:</h1>

    <form method="post">

    <table>
        <tr>
            <td>
                <label for="username">Username</label>
            </td>
            <td>
                <input type="text" name="username" value="{0}">
            </td>
            <td>
                <label style="color:red;">{2}</label>
            </td>
        </tr>

        <tr>
            <td>
                <label for="password">Password</label>
            </td>
            <td>
                <input type="password" name="password" value="">
            </td>
            <td>
                <label style="color:red;">{3}</label>
            </td>
        </tr>

        <tr>
            <td>
                <label for="verify">Verify Password</label>
            </td>
            <td>
                <input type="password" name="verify" value=""
            </td>
            <td>
                <label style="color:red;">{4}</label>
            <td>
        </tr>

        <tr>
            <td>
                <label for="email">Email (optional)</label>

            </td>
            <td>
                <input type="text" name="email" value="{1}">
            </td>
            <td>
                <label style="color:red;">{5}</label>
            </td>

        </tr>

    </table>

    <input type="submit">
    </form>
"""
originalForm = form.format("","","","","","","","")
page_footer = '''
</body></html>
'''

def escape_html(s):
    return cgi.escape(s, quote = True)


class MainHandler(webapp2.RequestHandler):

    def writeForm(self):
        self.response.write(page_header + originalForm + page_footer)

    def get(self):
        self.writeForm()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASS_RE = re.compile("^.{3,20}$")
        EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
        error_user = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        flag = False

        if not USER_RE.match(username):
            username = ""
            error_user = "That's not a valid username"
            flag = True
        if not PASS_RE.match(password):
            error_password = "That's not a valid password."
            flag = True
        elif not password == verify:
            error_verify = "Passwords don't match."
            flag = True
        if email:
            if not EMAIL_RE.match(email):
                error_email = "There's something wrong with your email address."
                flag = True

        newform = form.format(username, email, error_user, error_password, error_verify, error_email)

        if flag == True:
            self.response.write(page_header + newform + page_footer)
        else:
            self.redirect("/welcome?username=" + username)

class welcomeHandler(webapp2.RequestHandler):
    def get(self):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        username = self.request.get("username")
        if USER_RE.match(username):
            self.response.write("<h1>Welcome, " + username + "!</h1>")

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/welcome', welcomeHandler)
], debug=True)
