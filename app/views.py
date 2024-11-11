"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask import jsonify
from app.forms import UserForm
from app.models import User
# import sqlite3

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/users')
def show_users():
    users = db.session.query(User).all() # or you could have used User.query.all()
    return render_template('show_users.html', users=users)

@app.route('/table1')
def table1():
    """Render table simple with alternate rows"""
    return render_template('table1.html', name="Mary Jane")
@app.route('/table2')
def table2():
    """Render table with Search Filter for each column """
    return render_template('table2.html')
@app.route('/table3')
def table3():
    """Render table Export to Excel"""
    return render_template('table3.html')
@app.route('/table4')
def table4():
    """Render table Export to Excel"""
    return render_template('table4.html')
@app.route('/table5')
def table5():
    """Render table Group data Export to Excel"""
    return render_template('table5.html')
@app.route('/table6')
def table6():
    """Render table Group data Export to Excel"""
    return render_template('table6.html')
@app.route('/data1')
def show_data1():
    return render_template('data1.json')
@app.route('/data2')
def show_data2():
    return render_template('data2.json')
@app.route('/data3')
def show_data3():
    return render_template('data3.json')
@app.route('/data4')
def show_data4():
    return render_template('data4.json')
@app.route('/data5')
def show_data5():
    return render_template('data5.json')
@app.route('/data6')
def show_data6():
    return render_template('data6.json')

@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    user_form = UserForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.name.data # You could also have used request.form['name']
            email = user_form.email.data # You could also have used request.form['email']

            # save user to database
            user = User(name, email)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))

    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.route('/data', methods=['GET'])
def get_data():
    # Fetch data from the database
    data = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
    return jsonify(data)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
