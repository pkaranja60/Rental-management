from rental import app, db
from flask import render_template, redirect, url_for, flash, session, request, make_response
from flask_login import login_user, logout_user, login_required, current_user
from rental.forms import RegistrationForm, LoginForm, TenantsForm, RentForm
from rental.models import User, Tenant, Rent
import pdfkit


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = RentForm()
    if form.validate_on_submit():
        user_create = Rent(house_no=form.house_no.data,
                           rent=form.rent.data,
                           message=form.message.data,
                           date=form.date.data,
                           )
        db.session.add(user_create)
        db.session.commit()
        return redirect(url_for('rent'))
    else:
         return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('accounts/login.html', msg='Username or Password is incorrect ! Please try again', form=form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_create = User(username=form.username.data,
                           email=form.email.data,
                           password=form.password.data)
        db.session.add(user_create)
        db.session.commit()

        return redirect(url_for('login'),
                        )
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'{err_msg}', category='danger')
    return render_template('accounts/register.html',
                           msg='Please create an account',
                           form=form)


@app.route('/tenants', methods=['GET', 'POST'])
@login_required
def tenants():
    tenant = Tenant.query.all()
    return render_template('table.html', tenant=tenant)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = TenantsForm()
    if form.validate_on_submit():
        user_create = Tenant(name=form.name.data,
                             phone_no=form.phone_no.data,
                             house_no=form.house_no.data,
                             )
        db.session.add(user_create)
        db.session.commit()
        return redirect(url_for('tenants'))
    else:
        return render_template('tenant.html', form=form)


@app.route('/rent_paid', methods=['GET', 'POST'])
@login_required
def rent():
    rent = Rent.query.all()
    return render_template('rent.html', rent=rent)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('profile.html')


@app.route('/delete/<int:id>')
def delete(id):
    user_delete = Tenant.query.get_or_404(int(id))
    db.session.delete(user_delete)
    db.session.commit()
    return redirect(url_for('tenants'))


@app.route('/update/<int:id>', methods=['PUT', 'POST'])
def update(id):
    user_to_update = Tenant.query.get_or_404(int(id))
    form = TenantsForm()
    if form.validate_on_submit():
        user_to_update = Tenant(name=form.name.data,
                                phone_no=form.phone_no.data)
        db.session.commit()
        return redirect(url_for('tenants'))
    else:
        return render_template('table.html', user_to_update=user_to_update)


@app.route('/logout')
def logout():
    logout_user()
    flash(f'logged out succesfully', category='info')
    return redirect(url_for('index'))


@app.route('/pdf/<tenant>', methods=['POST'])
def get_pdf(tenant):
    if request.method == 'POST':
        tenant = Tenant.query.all()
    rendered = render_template(
        'pdf.html', user=tenant, tenant=tenant)
    pdf = pdfkit.form_string(rendered, False)
    response = make_response(pdf)
    response.headers['content=Type'] = 'application/pdf'
    response.headers['content=Disposition'] = 'inline: filename=' + \
        rent_statement+'.pdf'
    return response



