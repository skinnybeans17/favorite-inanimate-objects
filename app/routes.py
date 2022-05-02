from flask import Blueprint, request, render_template, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Collection, Object, User
from app.forms import CollectionForm, ObjectForm, SignUpForm, LoginForm
from app import bcrypt

# Create your routes here.

from app.extensions import app, db

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

@main.route('/')
def homepage():
    all_collections = Collection.query.all()
    print(current_user)
    return render_template('home.html', all_collections=all_collections)

@main.route('/new_collection', methods=['GET', 'POST'])
@login_required
def new_collection():
    form = CollectionForm()
    if form.validate_on_submit():
        new_collection = Collection(
            title = form.title.data,
            created_by = current_user
        )
        db.session.add(new_collection)
        db.session.commit()
        flash('A new collection has been created.')
        return redirect(url_for('main.collection_detail', collection_id=new_collection.id))

    return render_template('new_collection.html', form=form)

@main.route('/new_object', methods=['GET', 'POST'])
@login_required
def new_object():
    form = ObjectForm()
    if form.validate_on_submit():
        new_object = Object(
            name=form.name.data,
            category=form.category.data,
            image_url=form.image_url.data,
            collection=form.collection.data,
            created_by = current_user
        )
        print(new_object)
        db.session.add(new_object)
        db.session.commit()
        flash('New object has been added.')
        return redirect(url_for('main.object_detail', object_id=new_object.id))
    return render_template('new_object.html', form=form)

@main.route('/collection/<collection_id>', methods=['GET', 'POST'])
@login_required
def collection_detail(collection_id):
    collection = Collection.query.filter_by(id=collection_id).one()
    form = CollectionForm(obj=collection)

    if form.validate_on_submit():
        collection.title = form.title.data
        print(collection)
        print(collection.title)
        db.session.add(collection)
        db.session.commit()
        flash('The collection has been updated successfully.')
        return redirect(url_for('main.collection_detail', collection_id=collection.id))

    collection = Collection.query.filter_by(id=collection_id).one()
    return render_template('collection_detail.html', collection=collection, form=form)

@main.route('/object/<object_id>', methods=['GET', 'POST'])
@login_required
def object_detail(object_id):
    object = Object.query.filter_by(id=object_id).one()
    form = ObjectForm(obj=object)

    if form.validate_on_submit():
        object.name = form.name.data
        object.category = form.category.data
        object.image_url = form.image_url.data
        object.collection = form.collection.data
        print(object)
        print(object.category)
        db.session.add(object)
        db.session.commit()
        flash("The object has been updated successfully.")
        return redirect(url_for('main.object_detail', object_id=object.id))
    object = Object.query.filter_by(id=object_id).one()
    return render_template('object_detail.html', object=object, form=form)

@main.route('/add_to_favorites/<object_id>', methods=['GET', 'POST'])
@login_required
def add_to_favorites(object_id):
    object = Object.query.get(object_id)
    print(object)
    current_user.favorite_objects.append(object)
    db.session.add(current_user)
    db.session.commit()
    flash(f'The object, {object.name} has been added to your favorites')
    return redirect(url_for('main.object_detail', object_id=object.id))

@main.route('/remove_from_favorites/<object_id>', methods=['GET', 'POST'])
@login_required
def remove_from_favorites(object_id):
    object = Object.query.get(object_id)
    print(object)
    current_user.favorite_objects.remove(object)
    db.session.add(current_user)
    db.session.commit()
    flash(f'The object, {object.name} has been removed from your favorites')
    return redirect(url_for('main.object_detail', object_id=object.id))

@main.route('/favorites')
@login_required
def favorites():
    favorites = current_user.favorite_objects
    return render_template('favorites.html', favorites=favorites)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))