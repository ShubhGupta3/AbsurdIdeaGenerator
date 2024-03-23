from flask import Flask, request, render_template, redirect, url_for
import pathlib
import textwrap
import os
import markdown

import google.generativeai as genai
from dotenv import load_dotenv

app = Flask(__name__)
app.config["DEBUG"] = True

def initialize():
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
    # print("hello", GOOGLE_API_KEY)
    genai.configure(api_key=GOOGLE_API_KEY)

def generate_prompt(domain, stack, time):

    prompt = "Hi Gemini, I want to make an interestingly absurd project. Preferred Domain: " + domain + ". Preferred time range: " + time + " days. Preferred stack: " + stack
    return prompt

# A route to return a response frmo Gemini
@app.route('/idea/<domain>/<stack>/<time>', methods=['GET'])
def idea(domain, stack, time):
    initialize()
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(generate_prompt(domain=domain, stack=stack, time=time))
    html_content =  markdown.markdown(response.text)

    enhanced_html = f"""
        <html>
        <head>
            <title>Idea Page</title>
        </head>
        <body>
            <div id="content">
                {html_content}
            </div>
            <footer>
                <button>Regenerate response</button> <button onclick="goBack()">Edit filters</button>
            </footer>
            <script>
                function goBack() {{
                    window.history.back();
                }}
            </script>
        </body>
        </html>
        """
    return enhanced_html

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        d = request.form.get('domain')
        t = request.form.get('time')
        s = request.form.get('stack')

        if not s:
            s = "any"

        if not d:
            d = "any"
        else:
            strDomain = d

        if not t:
            t = "no time constraint"
        
        return redirect(url_for('idea',domain=d, stack=s, time=t))
        # return f'domain: {domain}, time: {time}, stack: {stack}'
    return render_template('home.html')


app.run()