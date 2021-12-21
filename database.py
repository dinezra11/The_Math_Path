import firebase_admin
from firebase_admin import db
from datetime import datetime
from string import ascii_letters, digits
from random import choice

cred_obj = firebase_admin.credentials.Certificate('dbKey.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://discaproject-95553-default-rtdb.europe-west1.firebasedatabase.app/'
})


def addUser(entryName, entryLast, entryId, entryPass, entryType):
    """ Add a user entry to the database.

    :param entryId:             User's ID
    :param entryName:           User's name
    :param entryLast:           User's last name
    :param entryPass:           User's password
    :param entryType:           User's type
    """

    def randomPassword():
        """ Generate a random password for linking child user to parent user. """
        linkPass = ""
        for i in range(10):  # Length of random password = 10
            linkPass += choice(ascii_letters + digits)  # Add one letter or digit

        return linkPass

    dbObj = db.reference('users')
    dbObj.update({
        entryId: {
            'name': entryName,
            'last': entryLast,
            'password': entryPass,
            'type': entryType,
            'passlink': randomPassword()
        }
    })


def addScore(gameType, score, userId):
    """ Add a score entry to the database.

    :param gameType:        Game's type
    :param score:           Player's score on this game
    :param userId           User's ID that played in this game
    """
    dbObj = db.reference('scores/{}'.format(userId))
    dbObj.push({
        'type': gameType,
        'score': score,
        'time': str(datetime.now())
    })


def addMessage(entryFrom, entryInfo, entryTo):
    """ Add a message entry to the database.

    :param entryFrom:        Sender's name
    :param entryInfo:        The actual message
    :param entryTo:          Receiver's ID
    """
    dbObj = db.reference('messages/{}'.format(entryTo))
    dbObj.push({
        'from': entryFrom,
        'info': entryInfo,
        'date': str(datetime.now().date())
    })


def addFeedback(text, entryFrom):
    dbObj = db.reference('feedback')
    dbObj.push({
        'from': entryFrom,
        'text': text
    })


# צריך לסיים את הפונקציה של מחיקת ההודעה!!!
'''def deleteMessage(userID: str, msgID: str):
    """ Delete a message from the database. """
    dbObj = db.reference("messages/{}".format(userID)).get()
    if dbObj is None:
        return None

    # Make a list of the records, and return it reversed. (Sorted by date and time)
    result = []
    for key, record in dbObj.items():
        result.insert(0, (key, record))

    return result'''


def getUser(searchID: str):
    """ Find and return user's details according to a specific ID.

    :param searchID:          The user's ID to search.
    """
    dbObj = db.reference("users").get()
    for item in dbObj.items():
        if item[0] == searchID:
            return item


def getScore(searchID: str):
    """ Find and return user's scores according to a specific ID. (Return a list of the scores)

    :param searchID:          The user's ID to find his game's scores.
    """
    dbObj = db.reference("scores/{}".format(searchID)).get()
    if dbObj is None:
        return None

    # Make a list of the records, and return it reversed. (Sorted by date and time)
    result = []
    for _, record in dbObj.items():
        result.insert(0, record)

    return result


def getMessage(searchID: str):
    """ Find and return user's messages according to a specific ID. (Return a list of the messages)
    Each element of the returned list will be a tuple, which the first value is the unique key of the record
    and the second value is a dictionary of the record's data.
    The unique key will be used for deleting messages.

    :param searchID:          The user's ID to find his messages.
    """
    dbObj = db.reference("messages/{}".format(searchID)).get()
    if dbObj is None:
        return None

    # Make a list of the records, and return it reversed. (Sorted by date and time)
    result = []
    for key, record in dbObj.items():
        result.insert(0, (key, record))

    return result


def validateLogin(loginId, loginPass):
    """ Check if ID and password are valid.
    Return True if login confirmed. Return False if login failed.

    :param loginId:
    :param loginPass
    """
    dbObj = db.reference("users").get()
    for userId, userDetail in dbObj.items():
        if userId == loginId:
            if userDetail['password'] == loginPass:
                return True

            break

    return False


def isIdExists(idSearch):
    """ Check if the ID already exists in the database. """
    dbObj = db.reference("users").get()
    for userId, userDetail in dbObj.items():
        if userId == idSearch:
            return True

    return False


def validateName(input):
    """ Check if name is valid. Name must be only letters. """
    return input.isalpha()


def validateId(input):
    """ Check if ID is valid. ID must be only digits. """
    return input.isdigit()


def validateAccountType(input):
    """ Check if account type is valid. Type must be a child, parent or tutor. """
    if input in ("Child", "Tutor", "Parent"):
        return True

    return False
