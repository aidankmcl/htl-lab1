"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""

import os

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

courses = pd.read_csv('./data/olin-courses-16-17.csv')


@app.route('/health')
def health():
    return 'ok'


@app.route('/')
def home_page():
    areas = set(courses.course_area)
    instructors = {}
    for area in areas:
        area_instructors = set([course[1].course_contact for course in courses[courses.course_area == area].iterrows()])
        instructors[area] = area_instructors
    return render_template('index.html', areas=areas, course_instructors=instructors)


@app.route('/area/<course_area>')
def area_page(course_area):
    return render_template('courses.html', areas=set(courses.course_area), courses=courses[courses.course_area == course_area].iterrows(), course_area=course_area)


@app.route('/instructor/<instructor>')
def instructor_page(instructor):
    return render_template('courses.html', areas=set(courses.course_area), courses=courses[courses.course_contact == instructor].iterrows(), instructor=instructor)

if __name__ == '__main__':
    app.run(debug=True)
