from app import app
from app.models import *
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
import json
from sqlalchemy import func


@app.route("/")
def index():
    return render_template("Map.html")

# ---------- SignUp--------------------------------------------------------------------------------
@app.route("/signUp_form", methods=["GET", "POST"])
def signUp_form():
    """show sign up form"""

    form = signUpForm()
    if form.validate_on_submit():
        account = form.account.data
        fullName = form.fullName.data
        password = form.password.data
        email = form.email.data
        NewUser = User(account=account, fullname=fullName, password=password, email=email)
        NewUser.set_password(form.password.data)
        db.session.add(NewUser)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template("signUp_form.html", form=form)


# ---------- Login -----------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(account=form.account.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


# ---------- Logout ---------------------------------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---------- Map -----------------------------------------------------------
@app.route("/map")
def map():
    return render_template("Map.html")


# ---------- current_parcel province API -----------------------------------------------------------
@app.route("/api/v1/current_parcel")
def current_parcel_get_API():
    """Return feature in polygon table"""
    current_parcels = db.session.query(Current_Parcel.id, Current_Parcel.owner, Current_Parcel.address, Current_Parcel.ward,
    Current_Parcel.district, Current_Parcel.area, Current_Parcel.land_use, Current_Parcel.updated_year,\
    func.ST_AsGeoJSON(Current_Parcel.geom).label('geometry'))
    # Get all daily administrative.
    current_parcel_Features = []  # store all administrative
    for current_parcel in current_parcels:  # generate geojson for each administrative
        current_parcel_temp = {}
        current_parcel_temp["type"] = "Feature"
        current_parcel_temp["properties"] = {
            "id": current_parcel.id,
            "owner": current_parcel.owner,
            "address": current_parcel.address,
            "ward": current_parcel.ward,
            "district": current_parcel.district,
            "area": current_parcel.area,
            "land_use": current_parcel.land_use,
            "updated_year": current_parcel.updated_year,
        }
        current_parcel_temp["geometry"] = json.loads(current_parcel.geometry)
        current_parcel_Features.append(current_parcel_temp)  # add atm geojson to list

    return jsonify({  # convert to geojson format
            "features": current_parcel_Features
        })


# ---------- add new parcel -----------------------------------------------------------
@app.route("/insertParcel", methods=["GET", "POST"])
def insertParcel():
    """add new insertParcel_result"""
    wards = Ward.query.all()
    form = InsertNewParcelForm()
    form.ward.choices = [(ward.ward_name, ward.ward_name) for ward in wards]

    if form.validate_on_submit():
        owner = form.owner.data
        address = form.address.data
        ward = form.ward.data
        area = form.area.data
        land_use = form.land_use.data
        geom = form.geom.data
        geom_input = 'POLYGON((' + geom + '))'
        print(geom_input)
        newParcel = Current_Parcel(owner=owner, address=address, ward=ward, area=area, land_use=land_use,\
        geom=func.ST_GeomFromText(geom_input, 4326))
        db.session.add(newParcel)
        db.session.commit()
        flash('Bạn vừa mới thêm 1 thửa đất mới')
        return redirect(url_for('map'))
    return render_template("insertParcel.html", form=form)


@app.route("/showlist_parcel")
def showlist_parcel():
    # Show List Preschools and search
    search_kw = request.args.get("search_kw")
    if search_kw:
        parcels = Current_Parcel.query.filter(Current_Parcel.address.contains(search_kw) | Current_Parcel.ward.contains(search_kw))
    else:
        parcels = Current_Parcel.query.all()

    return render_template("showlist_parcel.html", parcels=parcels)


# ---------- Edit parcel -----------------------------------------------------------
@app.route("/edit_parcel/<int:parcel_id>", methods=['GET'])
def edit_parcel(parcel_id):
    parcel = Current_Parcel.query.get(parcel_id)
    wards = Ward.query.all()
    return render_template("edit_parcel.html", parcel=parcel, wards=wards)


@app.route("/edit_parcel_result", methods=["POST"])
def edit_parcel_result():
    parcel_id = int(request.form.get("id"))
    parcel = Current_Parcel.query.get(parcel_id)

    parcel_record = Landuse_History_Record(parcel_id=parcel_id, land_use=parcel.land_use)
    db.session.add(parcel_record)

    parcel.owner = request.form.get("owner")
    parcel.address = request.form.get("address")
    parcel.ward = request.form.get("ward")
    parcel.land_use = request.form.get("land_use")
    parcel.area = request.form.get("area")

    db.session.commit()
    return redirect(url_for('showlist_parcel'))


# ---------- delete parcel -----------------------------------------------------------
@app.route("/delete_parcel/<int:parcel_id>", methods=['GET'])
def delete_parcel(parcel_id):
    parcel = Current_Parcel.query.get(parcel_id)
    db.session.delete(parcel)
    db.session.commit()
    return redirect(url_for('showlist_parcel'))


@app.route("/show_landuse_history/<int:parcel_id>", methods=['GET'])
def show_landuse_history(parcel_id):
    # Show List Preschools and search
    parcel = Current_Parcel.query.get(parcel_id)
    landuseHistory = Landuse_History_Record.query.filter_by(parcel_id=parcel_id).all()

    return render_template("show_landuse_history.html", parcel=parcel, landuseHistory=landuseHistory)

#
# @app.route("/insertParcel_result", methods=["GET"])
# def insertParcel_result():
#     """add new insertParcel_result"""
#
#     # Get form information.
#     parcel = Current_Parcel(owner="Long", address="33 phố A", ward="Phường 1", area="500",\
#     land_use="Nhà ở", updated_year=2022,\
#     geom=func.ST_GeomFromText('POLYGON((106.6654224446616 10.59896677990389 , 106.66538307614 10.59852890410886 , 106.6657072806969 10.59852250177184 , 106.6657019322149 10.59895647540645 , 106.6654224446616 10.59896677990389))', 4326))
#     db.session.add(parcel)
#     db.session.commit()
#     return 'New ATM has been added'
