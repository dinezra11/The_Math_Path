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


def deleteUser(entryId):
    """ Delete a user from the database.
    Make sure to delete this user from the parent's list too. """
    deleteRef = db.reference("users/{}".format(entryId))
    if deleteRef.get() is None:
        return

    parentId = deleteRef.get().get("parent")
    if parentId is not None:
        # Delete the child's entry from the parent's children list
        parentId = parentId.split("(")[1].split(")")[0]
        print(parentId)
        parentRef = db.reference("users/{}/children".format(parentId))
        for key, info in parentRef.get().items():
            if info["id"] == str(entryId):
                parentRef.child(key).delete()
                break

    # Delete scores
    infoRef = db.reference("scores/{}".format(entryId))
    if infoRef.get() is not None:
        infoRef.delete()

    # Delete messages
    infoRef = db.reference("messages/{}".format(entryId))
    if infoRef.get() is not None:
        infoRef.delete()

    # Delete the actual user
    deleteRef.delete()


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
    """ Add a feedback message for the system's developers.

    :param text:            The actual message
    :param entryFrom:       Sender's name
    """
    dbObj = db.reference('feedback')
    dbObj.push({
        'from': entryFrom,
        'text': text
    })


def addTips(text, entryFrom):
    """ Add a tip message for the system's developers.

    :param text:            The actual message
    """
    dbObj = db.reference('tips')
    dbObj.push({
        'from': entryFrom,
        'text': text
    })


def addPrivateNotes(text, entryFrom, childID):
    """ Add a tip message for the system's developers.

    :param text:            The actual message
    """
    dbObj = db.reference('private notes')
    dbObj.push({
        'from': entryFrom,
        'text': text,
        'childID': childID
    })


def addChildToParent(childID, linkPass, parentID, parentName):
    """ Check if ID and link pass are valid, and if so -> add the child to the parent.
    Return True if child has been added successfully. Return False if operation failed.

    :param childID:             The child's ID to add.
    :param linkPass:            The unique link password of the child.
    :param parentID:            The parent's ID.
    :param parentName           The parent's name.
    """
    # Check if child already linked to the parent
    dbObj = db.reference("users/{}/children".format(parentID)).get()
    if dbObj is not None:
        for _, childDict in dbObj.items():
            if childDict["id"] == childID:
                return False

    # Validate the link password and add the child if input is valid
    dbObj = db.reference("users").get()
    for userId, userDetail in dbObj.items():
        if userId == childID:
            if userDetail['passlink'] == linkPass and userDetail['type'] == "Child":
                try:
                    # Update child's parent
                    dbObj = db.reference("users/{}".format(childID))
                    dbObj.update({
                        'parent': parentName
                    })

                    # Add the child to the parent's database
                    dbObj = db.reference('users/{}/children'.format(parentID))
                    dbObj.push({
                        'full_name': "{} {}".format(userDetail['name'], userDetail['last']),
                        'id': userId,
                        'password': userDetail['password']
                    })
                    return True
                except Exception as e:
                    return False
            else:
                break

    return False


def getUser(searchID: str):
    """ Find and return user's details according to a specific ID.

    :param searchID:          The user's ID to search.
    """
    dbObj = db.reference("users").get()
    for item in dbObj.items():
        if item[0] == searchID:
            return item


def getAllUsers():
    """ Return all of the users in the system. """
    dbObj = db.reference("users").get()
    return dbObj


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

    :param loginId:                 User's ID.
    :param loginPass:               User's password.
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
