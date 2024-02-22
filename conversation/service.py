from sqlalchemy.orm import Session

from conversation.models import Conversation, Message, Participant
from conversation.schemas import CreateConversationSchema, SendMessageSchema


def find_private_conversation(db: Session, creator_id, pid):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.is_group == False)
        .join(Participant)
        .filter(
            (Participant.profile_id == creator_id) | (Participant.profile_id == pid)
        )
        .first()
    )

    return conversation


def store_conversation(db: Session, payload):
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
    for profile_id in user_ids:
        participant = Participant(
            profile_id=profile_id, conversation_id=conversation_id
        )
        db.add(participant)
    db.commit()


def store_message(db: Session, creator_id: str, payload):
    message = Message(
        content=payload.content,
        participant_id=creator_id,
        conversation_id=payload.conversation_id,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return message
