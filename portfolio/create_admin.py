from app import app, db, user_datastore, hash_password

with app.app_context():
    admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')

    if not user_datastore.find_user(email="admin@example.com"):
        user = user_datastore.create_user(username="admin", email="admin@example.com",
                                          password=hash_password("adminpass"))
        user_datastore.add_role_to_user(user, admin_role)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

