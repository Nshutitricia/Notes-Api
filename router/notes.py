from datetime import datetime
from typing import Optional

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, Field
from starlette import status

from util import find_item

router = APIRouter(
    prefix="/notes"
)


class Notes(BaseModel):
    title: str
    content: str
    created_at: datetime


class UpdateNotes(BaseModel):
    title: Optional[str] = Field(None, description="Title of the note")
    content: Optional[str] = Field(None, description="Content of the note")


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime


notes: list[dict[str, int | str]] = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "content": "Practice building APIs",
        "created_at": "2026-03-01"
    }
]


@router.get("/", response_model=list[NoteResponse])
async def get_notes(skip: int = 0, limit: int = 10 , title_contains: Optional[str] = None , content_contains: Optional[str] = None):
    result_notes = notes.copy()
    if title_contains is not None:
        result_notes = [note for note in result_notes if title_contains.lower() in note["title"].lower()]

    if content_contains is not None:
        result_notes = [note for note in result_notes if content_contains.lower() in note["content"].lower()]


    return result_notes[skip: skip + limit]


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    item, idx = find_item(notes, lambda x: x["id"] == note_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note_item: Notes):
    note = {
        "id": len(notes) + 1,
        "title": note_item.title,
        "content": note_item.content,
        "created_at": note_item.created_at
    }
    notes.append(note)

    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note_update: UpdateNotes):
    item, idx = find_item(notes, lambda x: x["id"] == note_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Item not found")
    if note_update.title is not None:
        item["title"] = note_update.title
    if note_update.content is not None:
        item["content"] = note_update.content
    return item


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int):
    item, idx = find_item(notes, lambda x: x["id"] == note_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Item not found")

    notes.pop(idx)

    return
