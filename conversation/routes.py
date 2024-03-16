from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user


from conversation.models import Conversation, Participant
from conversation.schemas import (
    AllConversations,
    CreateConversationSchema,
    GetConversations,
    NewConversationSchema,
    SendMessageSchema,
)
from conversation.service import (
    get_conversation_by_id,
    get_private_conversation,
    get_user_conversations,
    store_group_conversation,
    store_profile_conversation,
    store_participants,
    store_message,
)


from users.models import User

router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[AllConversations])
def get_conversations(db: Session = Depends(get_db), user=Depends(get_current_user)):
    conversations = get_user_conversations(db, user.id)
    return conversations


@router.get("/{pid}/", response_model=GetConversations)
def get_conversation_by_profile_id(
    pid,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    conv = get_conversation_by_id(db, user.id, pid)
    if conv is not None:
        return conv

    else:
        return JSONResponse(
            content={"message": "Conversation doesn't exists."},
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.post("/", status_code=200, response_model=GetConversations)
def create_conversation(
    payload: NewConversationSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # first we gonna create group conversation
    if payload.profile_id is None and (
        payload.user_ids is None or len(payload.user_ids) < 1
    ):
        return JSONResponse(
            content={"message": "Cannot create new chat, add more Participants."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    elif payload.profile_id is None and len(payload.user_ids) > 0:

        # create group schema
        conversation_schema = CreateConversationSchema(
            is_group=True,
            creator_id=str(user.id),
            title="Group",
        )
        # create conv
        new_conversation = store_group_conversation(db, conversation_schema)
        # create list of participants (except creator)
        user_ids = list()
        user_ids.append(str(payload.user_ids))

    elif payload.profile_id is not None:
        # check if user exists
        receiver = db.query(User).get(payload.profile_id)
        if receiver is None:
            return JSONResponse(
                content={"message": "Wrong profile id"},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        current_conversation = get_private_conversation(db, user.id, payload.profile_id)
        if current_conversation is not None:
            return JSONResponse(
                content={"message": "Conversation already exists"},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        new_conversation = store_profile_conversation(db, user.id, payload.profile_id)

        user_ids = list()
        user_ids.append(str(payload.profile_id))

    user_ids.append(str(user.id))
    store_participants(db, new_conversation.id, user_ids)

    return new_conversation


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
        .filter_by(user_id=user_id, conversation_id=conversation_id, is_group=True)
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
    user=Depends(get_current_user),
):
    conversation = get_conversation_by_id(db, user.id, payload.cid)

    if conversation is None:
        return JSONResponse(content={"message": "Cannot find conversation"})

    participant = (
        db.query(Participant)
        .filter(
            (Participant.user_id == user.id)
            & (Participant.conversation_id == conversation.id)
        )
        .first()
    )

    message = store_message(db, participant.id, conversation.id, payload)
    conversation.last_message_id = message.id
    db.commit()

    return message
