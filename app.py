#   IMPORT THE NEEDED MODULES
import hmac

from database_connection import *
from flask_cors import CORS
from datetime import timedelta
from flask_mail import Mail, Message
from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity


class User:
    def __init__(self, id, first_name, last_name, username, address, password, email_address):
        self.id = id
        self.address = address
        self.password = password
        self.username = username
        self.last_name = last_name
        self.first_name = first_name
        self.email_address = email_address


def send_email(email_address, first_name):
    email_to_send = Message('Welcome to the Radical Store.', sender='notbrucewayne71@gmail.com',
                            recipients=[email_address])
    email_to_send.body = f"Congratulations {first_name} on a successful registration. \n\n" \
                         f"Welcome to the Radical Store. family, browse around and make sure to enjoy the " \
                         f"experience. "

    mail.send(email_to_send)


def fetch_users():
    new_data = []
    db_users = get_users()

    for user in db_users:
        new_data.append(User(user[0], user[1], user[2], user[3], user[4], user[5], user[6]))

    return new_data


#   LOGS IN THE USER AND RETURNS THE USER OBJECT. JWT ALSO USES THIS TO CREATE A JWT TOKEN
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


#   THIS FUNCTION IS USED ON ALL THE ROUTES THAT NEED THE JWT TOKEN. JWT DECODES THE TOKEN AND GETS THE USER DETAILS
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
app.debug = True

app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['SECRET_KEY'] = "super-secret"
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PASSWORD'] = "notBruceWayne"
app.config['MAIL_USERNAME'] = "notbrucewayne71@gmail.com"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)

CORS(app)
mail = Mail(app)
jwt = JWT(app, authenticate, identity)

#   CREATE THE USER TABLE IF IT DOESNT EXIST
create_user_table()
#   CREATE THE PRODUCT TABLE IF IT DOESNT EXIST
create_product_table()
#   GET ALL THE USERS IN THE DATABASE
users = fetch_users()

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


#   ROUTE WILL BE USED TO REGISTER A NEW USER, ROUTE ONLY ACCEPTS A POST METHOD
@app.route('/user-registration/', methods=["POST"])
def user_registration():
    #   CREATE AN EMPTY OBJECT THAT WILL HOLD THE response OF THE PROCESS
    response = {}

    # WRAP IN TRY...CATCH
    #   MAKE SURE THE request.method IS A POST
    if request.method == "POST":
        #   GET THE FORM DATA TO BE SAVED
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        address = request.form['address']
        password = request.form['password']
        email_address = request.form['email_address']

        #   CALL THE register_user FUNCTION TO REGISTER THE USER
        register_user(first_name, last_name, username, address, password, email_address)
        #   SEND THE USER AN EMAIL INFORMING THEM ABOUT THEIR REGISTRATION
        send_email(email_address, first_name)
        #   GET THE NEWLY REGISTERED USER
        user = get_user(username, password)
        #   UPDATE THE response
        response["status_code"] = 201
        response["current_user"] = user
        response["message"] = "registration successful"
        response["email_status"] = "Email was successfully sent"

        #   RETURN A JSON VERSION OF THE response
        return jsonify(response)


#   ROUTE WILL BE USED TO LOG A REGISTERED USER IN, ROUTE ONLY ACCEPTS A POST METHOD
@app.route("/user-login/", methods=["POST"])
def login():
    #   CREATE AN EMPTY OBJECT THAT WILL HOLD THE response OF THE PROCESS
    response = {}

    # WRAP IN TRY...CATCH
    #   MAKE SURE THE request.method IS A POST
    if request.method == "POST":
        #   GET THE FORM DATA TO BE SAVED
        username = request.form['username']
        password = request.form['password']

        #   CALL THE login_user FUNCTION TO REGISTER THE USER
        user = get_user(username, password)
        print(user)

        #   UPDATE THE response
        response["status_code"] = 201
        response["current_user"] = user
        response["message"] = "login successful"

        #   RETURN A JSON VERSION OF THE response
        return jsonify(response)


#   ROUTE WILL BE USED TO ADD A NEW PRODUCT, ROUTE ONLY ACCEPTS A POST METHOD
@app.route('/add-product/', methods=["POST"])
#   AN AUTHORISATION TOKEN IS NEEDED TO ACCESS THIS ROUTE
@jwt_required()
def add_product():
    #   CREATE AN EMPTY OBJECT THAT WILL HOLD THE response OF THE PROCESS
    response = {}

    # WRAP IN TRY...CATCH
    #   MAKE SURE THE request.method IS A POST
    if request.method == "POST":
        #   GET THE FORM DATA TO BE SAVED
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        review = request.form['review']

        #   CALL THE save_product FUNCTION TO SAVE THE PRODUCT TO THE DATABASE
        save_product(name, description, price, category, review)

        #   UPDATE THE response
        response["status_code"] = 201
        response['description'] = "Product successfully added"

        #   RETURN A JSON VERSION OF THE response
        return jsonify(response)


#   ROUTE WILL BE USED TO VIEW ALL PRODUCTS, ROUTE ONLY ACCEPTS A GET METHOD
@app.route('/show-products/', methods=["GET"])
def show_products():
    #   CREATE AN EMPTY OBJECT THAT WILL HOLD THE response OF THE PROCESS
    response = {}

    #   MAKE SURE THE request.method IS A GET
    if request.method == "GET":
        #   GET ALL THE PRODUCTS FROM THE DATABASE
        products = get_all_products()

        #   UPDATE THE response
        response['status_code'] = 200
        response['products'] = products
    # render_template('index.html')

    #   RETURN A JSON VERSION OF THE response
    return jsonify(response)


#   ROUTE WILL BE USED TO VIEW A SINGLE PRODUCT, ROUTE ONLY ACCEPTS A GET METHOD
@app.route('/view-product/<int:product_id>/', methods=["GET"])
def view_product(product_id):
    #   CREATE AN EMPTY OBJECT THAT WILL HOLD THE response OF THE PROCESS
    response = {}

    #   MAKE SURE THE request.method IS A GET
    if request.method == "GET":
        #   GET A PRODUCT FROM THE DATABASE
        product = get_one_product(product_id)

        #   UPDATE THE response
        response["status_code"] = 200
        response["product"] = product
        response["description"] = "Product retrieved successfully"

    #   RETURN A JSON VERSION OF THE response
    return jsonify(response)


#   ROUTE WILL BE USED TO EDIT A PRODUCT, ROUTE ONLY ACCEPTS A PUT METHOD
@app.route('/edit-product/<int:product_id>/', methods=["PUT"])
#   AN AUTHORISATION TOKEN IS NEEDED TO ACCESS THIS ROUTE
@jwt_required()
def edit_product(product_id):
    #   CREATE AN EMPTY OBJECT THAT WILL HOLD THE response OF THE PROCESS
    response = {}

    #   MAKE SURE THE request.method IS A PUT
    if request.method == "PUT":
        #   TURN THE INCOMING DATA TO A DICTIONARY TO MAKE IT EASIER TO USE
        incoming_data = dict(request.json)
        updated_data = {}

        #   CHECK IF WE ARE UPDATING THE PRODUCT name
        if incoming_data.get("name") is not None:
            #   UPDATE THE updated_data
            updated_data["name"] = incoming_data.get("name")

            #   CALL THE edit_product AND PASS IN THE COLUMN TO BE UPDATED, THE NEW DATA AND THE product_id
            update_product("name", updated_data["name"], product_id)

            #   UPDATE THE response
            response['status_code'] = 200
            response['message'] = "name update was successful"

        #   CHECK IF WE ARE UPDATING THE PRODUCT name
        if incoming_data.get("description") is not None:
            #   UPDATE THE updated_data
            updated_data['description'] = incoming_data.get('description')

            #   CALL THE edit_product AND PASS IN THE COLUMN TO BE UPDATED, THE NEW DATA AND THE product_id
            update_product("description", updated_data['description'], product_id)

            #   UPDATE THE response
            response["status_code"] = 200
            response['message'] = "description update was successful"

        #   CHECK IF WE ARE UPDATING THE PRODUCT name
        if incoming_data.get("price") is not None:
            #   UPDATE THE updated_data
            updated_data['price'] = incoming_data.get('price')

            #   CALL THE edit_product AND PASS IN THE COLUMN TO BE UPDATED, THE NEW DATA AND THE product_id
            update_product("price", updated_data['price'], product_id)

            #   UPDATE THE response
            response["status_code"] = 200
            response['message'] = "price update was successful"

        #   CHECK IF WE ARE UPDATING THE PRODUCT name
        if incoming_data.get("category") is not None:
            #   UPDATE THE updated_data
            updated_data['category'] = incoming_data.get('category')

            #   CALL THE edit_product AND PASS IN THE COLUMN TO BE UPDATED, THE NEW DATA AND THE product_id
            update_product("category", updated_data['category'], product_id)

            #   UPDATE THE response
            response["status_code"] = 200
            response['message'] = "category update was successful"

        #   CHECK IF WE ARE UPDATING THE PRODUCT name
        if incoming_data.get("review") is not None:
            #   UPDATE THE updated_data
            updated_data['review'] = incoming_data.get('review')

            #   CALL THE edit_product AND PASS IN THE COLUMN TO BE UPDATED, THE NEW DATA AND THE product_id
            update_product("review", updated_data['review'], product_id)

            #   UPDATE THE response
            response["status_code"] = 200
            response['message'] = "review update was successful"

    return response


#   ROUTE WILL BE USED TO EDIT A PRODUCT, ROUTE ONLY ACCEPTS A PUT METHOD
@app.route("/delete-product/<int:product_id>", methods=["GET"])
#   AN AUTHORISATION TOKEN IS NEEDED TO ACCESS THIS ROUTE
@jwt_required()
def delete_product(product_id):
    #   CREATE AN EMPTY OBJECT THAT WILL HOLD THE response OF THE PROCESS
    response = {}

    #   CALL THE delete_product AND PASS IN THE product_id
    delete_product(product_id)

    #   UPDATE THE response
    response['status_code'] = 200
    response['message'] = "product deleted successfully."

    return response
