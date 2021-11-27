import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('dbKey.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://discaproject-95553-default-rtdb.europe-west1.firebasedatabase.app/'
})


def addUser(entryId, entryName, entryLast, entryPass, entryType):
    """ Add a user entry to the database.

    :param entryId:
    :param entryName:
    :param entryLast:
    :param entryPass:
    :param entryType:
    :return:
    """
    dbObj = db.reference("users")
    dbObj.update({
        entryId: {
            "name": entryName,
            "last": entryLast,
            "password": entryPass,
            "type": entryType
        }
    })


"""
def getUsers():
    dbOjb = db.reference("users").get()
    try:
        for id, detail in obj.items():
            print("{0} {1} - {2}".format(detail['Name'], detail['Last'], id))
    except:
        print("Error")
"""
