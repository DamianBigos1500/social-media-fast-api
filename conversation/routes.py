from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import func

from sqlalchemy.orm import Session

from core.database import get_db


from conversation.models import Conversation, Participant
from conversation.schemas import (
    CreateConversationSchema,
    NewConversationSchema,
    SendMessageSchema,
)
from conversation.service import (
    find_private_conversation,
    store_conversation,
    store_message,
    store_participants,
)

from users.models import Profile, User

import json

router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{profile_id}/all/")
def get_conversations(profile_id, db: Session = Depends(get_db)):
    concersations = (
        db.query(Conversation)
        .join(Conversation.participants)
        .filter(Participant.profile_id == profile_id)
        .all()
    )
    return JSONResponse(content={"post": jsonable_encoder(concersations)})


@router.get("/{cid}/")
def get_conversation_by_profile(cid, db: Session = Depends(get_db)):
    creator = db.query(User).first()
    # check if creator is in conversation
    conversation = db.query(Conversation).filter_by(id=cid).first()

    if conversation is None:
        return JSONResponse(content={"message": "Conversation doesn't exists."})
    else:
        return JSONResponse(
            content={
                "message": "Conversation deesn't exists.",
            }
        )


@router.post("/oto/{pid}/")
def create_one_to_one_conversation(pid, db: Session = Depends(get_db)):
    creator = db.query(Profile).first()
    receiver = db.query(Profile).filter_by(id=pid).first()

    conversations = find_private_conversation(db, creator.id, receiver.id)

    return JSONResponse(
        content={
            "message": "Conversation already exists.",
            "convs": jsonable_encoder(conversations),
        }
    )


@router.post("/")
def create_group_conversation(
    payload: NewConversationSchema, db: Session = Depends(get_db)
):
    # get request user
    creator = db.query(User).first()

    # first we gonna create group conversation
    if payload.profile_id is None and (
        payload.user_ids is None or len(payload.user_ids) < 1
    ):
        return JSONResponse(
            content={
                "message": "Cannot create new chat, add more Participants.",
                "ss": payload.profile_id is not None,
            }
        )
    elif payload.profile_id is None and len(payload.user_ids) > 0:
        # create group schema
        user_ids = list(payload.user_ids)

        conversation_schema = CreateConversationSchema(
            is_group=True,
            creator_id=str(creator.id),
            title="Group",
        )
    elif payload.profile_id is not None:
        current_conversation = find_private_conversation(db, creator.id, payload.profile_id)

        if current_conversation is not None:
            return JSONResponse(
                content={
                    "message": "Conversation exists succesfully",
                    "conversation": jsonable_encoder(current_conversation),
                }
            )
        # create ont to one schema
        user_ids = list(payload.profile_id)

        conversation_schema = CreateConversationSchema(
            is_group=False,
            creator_id=str(creator.id),
            title=f"Private message from {creator.id} to user {payload.profile_id}",
        )

    # store it to db
    user_ids.append(str(creator.id))

    # create conv
    conversation = store_conversation(db, conversation_schema)
    store_participants(db, conversation.id, user_ids)

    return JSONResponse(
        content={
            "message": "Conversation created succesfully",
            "conversation": jsonable_encoder(conversation),
        }
    )


@router.post("/add-participant/{conversation_id}")
def add_participant_to_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    user_id=None,
):
    # chcek if conversation exists
    conversation = db.query(Conversation).filter_by(id=conversation_id).first()
    if not conversation:
        return JSONResponse(
            content={"message": "Conversation does not exists"},
            status_code=404,
        )
    # check if participant is in conversation
    participant = (
        db.query(Participant)
        .filter_by(user_id=user_id, conversation_id=conversation_id)
        .first()
    )
    if participant:  # participant currently in conversation
        return JSONResponse(
            content={"message": "Participant currently in conversation"}
        )
    else:  # create participant
        Participant(
            user_id=user_id,
            conversation_id=conversation_id,
        )
        return JSONResponse(
            content={
                "message": "Cannot find participant",
                "post": jsonable_encoder(participant),
            }
        )


@router.post("/remove-participant/{conversation_id}")
def remove_participant_from_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    user_id=None,
):
    # check if participant is in conversation
    participant = (
        db.query(Participant)
        .filter_by(user_id=user_id, conversation_id=conversation_id)
        .first()
    )

    if participant is None:  # participant currently not in conversation
        return JSONResponse(content={"message": "Participant is not in conversation"})
    else:  # remove participant
        return JSONResponse(content={"message": "Participant is not in conversation"})


@router.post("/messages/")
def send_message(
    payload: SendMessageSchema,
    db: Session = Depends(get_db),
):
    creator = db.query(User).first()
    conversation = db.query(Conversation).filter_by(cid=payload.cid).first()

    if conversation is None:  # create new conversation where it will be receiver_id
        return JSONResponse(content={"message": "Cannot find conversation"})

    # conv exists, now check if user is in conversation
    participant = (
        db.query(Participant)
        .filter_by(user_id=creator.id, conversation_id=conversation.id)
        .first()
    )

    if participant:
        payload = SendMessageSchema(
            content=payload.content, conversation_id=str(conversation.id)
        )

        message = store_message(db, str(creator.id), payload)
        conversation.last_message_id = message.id
        db.commit()

        return JSONResponse(
            content={
                "message": "Message send succesfully",
                "new_message": jsonable_encoder(message),
                "conversation": jsonable_encoder(conversation),
            }
        )
    else:
        return JSONResponse(content={"message": "You are not in conversation"})
