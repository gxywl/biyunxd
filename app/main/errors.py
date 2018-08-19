from flask import render_template
from . import main


@main.app_errorhandler(413)
def file_too_large(e):
    return render_template('413.html'), 413