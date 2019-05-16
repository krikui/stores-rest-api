
from resources.user import UserModel
from werkzeug.security import safe_str_cmp

# users = [
#         UserModel(1, 'bob', 'asdf'),
#         UserModel(2, 'beth', 'qwerty'),
# ]
#
#
# # username_mapping = {'bob': users[0]}
# # userid_mapping = {1: users[0]}
#
# username_mapping = {u.username: u for u in users}  #dict comprehension
# user_id_mapping = {u.id: u for u in users}




# def authenticate (username, password):
#     user = username_mapping.get(username, None)
#     if user and user['password'] == password:
#         return user
def authenticate(username, password):
    #user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    #return user_id_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)
