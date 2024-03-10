from sqlalchemy import desc
from sqlalchemy.orm import Session

from conversation.models import Conversation, Message, Participant


def get_user_conversations(db: Session, user_id):
    convs = (
        db.query(Conversation)
        .filter(Conversation.participants.any(Participant.user_id == user_id))
        .order_by(desc(Conversation.updated_at))
        .all()
    )

    return convs


def get_private_conversation(db: Session, user_id, pid):
    private_conv = (
        db.query(Conversation)
        .filter(Conversation.is_group == False)
        .filter(Conversation.profile_id == pid)
        .filter(Conversation.participants.any(Participant.user_id == user_id))
        .first()
    )
    return private_conv


def get_group_conversation(db: Session, user_id, pid):
    group_conv = (
        db.query(Conversation)
        .filter(Conversation.is_group == True)
        .filter(Conversation.id == pid)
        .filter(Conversation.participants.any(Participant.user_id == user_id))
        .first()
    )
    return group_conv


def get_conversation_by_id(db: Session, user_id, pid):
    conv = get_private_conversation(db, user_id, pid)
    if conv is not None:
        return conv

    conv = get_group_conversation(db, user_id, pid)
    return conv


def store_profile_conversation(db: Session, creator_id, pid):
    conversation = Conversation(
        is_group=False,
        creator_id=creator_id,
        profile_id=pid,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def store_group_conversation(db: Session, payload):
    conversation = Conversation(
        id=payload.id,
        title=payload.title,
        is_group=payload.is_group,
        creator_id=payload.creator_id,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def store_participants(db: Session, conversation_id, user_ids):
    for user_id in user_ids:
        participant = Participant(user_id=user_id, conversation_id=conversation_id)
        db.add(participant)
    db.commit()


def store_message(db: Session, user_id: str, cid: str, payload):
    message = Message(
        content=payload.content,
        participant_id=user_id,
        conversation_id=cid,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return message
