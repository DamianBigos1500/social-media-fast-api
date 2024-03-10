from sqlmodel import Session
from friend.models import FriendAssociation


def get_friend_list(db: Session, user_id):
    requested_friends = (
        db.query(FriendAssociation.user_id)
        .filter(FriendAssociation.friend_id == user_id)
        .filter(FriendAssociation.status == 0)
    )
    received_friends = (
        db.query(FriendAssociation.friend_id)
        .filter(FriendAssociation.user_id == user_id)
        .filter(FriendAssociation.status == 0)
    )

    return requested_friends.union(received_friends).all()


def friend_data(db: Session, user_id, friend_id):
    requested_friends = db.query(FriendAssociation).filter(
        (FriendAssociation.friend_id == user_id)
        & (FriendAssociation.user_id == friend_id)
    )
    received_friends = db.query(FriendAssociation).filter(
        (FriendAssociation.user_id == user_id)
        & (FriendAssociation.friend_id == friend_id)
    )

    return requested_friends.union(received_friends).first()


def add_new_friend(db: Session, user_id, friend_id):
    association_exists = False

    if association_exists is False:
        friend = FriendAssociation(user_id=user_id, friend_id=friend_id)
        db.add(friend)
        db.commit()

        return friend
