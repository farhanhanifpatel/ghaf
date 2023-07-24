from flask import Blueprint, render_template, request, session, g, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

authentication_bp = Blueprint('auth', __name__)


@authentication_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # try:
            email = request.form.get('email')
            password = request.form.get('password')
            cursor=g.db.cursor(dictionary=True)
            cursor.execute('SELECT id,prefix,firstname,lastname,email,phone_code,phone_number,gender,dob,nationality FROM tbl_users WHERE user_type="admin"')
            admin=cursor.fetchone()
            session['email'] = admin
            # print(password,phone) 
            if not email:
                empty_message="Please Enter Email"
                return render_template('login.html', error_phone=empty_message)
                # return jsonify({"massage":"phone number or email missing required for login"})
            
            if not password:
                empty_password="Please Enter Password"
                return render_template('login.html', error_password=empty_password)
                # return jsonify({"massage":"password missing password required"})
            
            cursor=g.db.cursor()
            cursor.execute('select * from tbl_users where  email = %s and is_active = 1 and is_delete = 0 AND user_type="admin"',(email,))
            admin = cursor.fetchone()
            
            if admin:
                # print("i am adkmadsf=============>",admin)
                check_pass = check_password_hash(admin[9],password)
                if check_pass:
                    if admin[14] == True:
                        
                        return redirect(url_for('admin.dashboard'))
                    else:
                        return jsonify({
                            "massage":"Admin is not verified",
                            "email":admin[4]
                        })
                error_data="wrong credential"
                return render_template('login.html',error_data=error_data)
                # else:
                #     return({
                #         "error":"wrong credential"
                #     })
            else:
                error_admin = "Only Admin Can Login"
                return render_template('login.html', error=error_admin)
                # return jsonify({"Mesage":"Only Admin Can Login"})
        # return render_template('login.html')
        
    else:
        return render_template('login.html')


@authentication_bp.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('auth.admin_login'))
