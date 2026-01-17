from fastapi import Body, Depends, FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.adapters.service import GameService
from backend.database.db import Base, SessionLocal, engine
from backend.models.api import (
    ChoiceInfo,
    EndingSummaryResponse,
    ListPlaythroughsResponse,
    PlaythroughSummary,
    StoryAdvanceResponse,
    StoryRecapResponse,
    StoryStartResponse,
)

# create tables if not exists
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# dependency function for database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create game service dependency
def get_game_service(db: Session = Depends(get_db)):
    return GameService(db)


@app.get(
    '/game',
    response_model=ListPlaythroughsResponse,
    summary='Retrieve all playthroughs in database',
)
def list_playthroughs(service: GameService = Depends(get_game_service)):
    service.load_all_sessions()

    # return info for all playthroughs: id, narrative state, if it is "allowed to end", and a one-sentence summary
    response = ListPlaythroughsResponse()
    for id, state in service.states.items():
        response.playthroughs.append(
            PlaythroughSummary(
                playthrough_id=id,
                act=state.narrative.act.name,
                progress=state.narrative.progress,
                can_end=state.narrative.allow_ending,
                summary=service.storyteller.summarize_story(state.history),
            )
        )
    return response


@app.post(
    '/game/start',
    response_model=StoryStartResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Start a new playthrough',
)
def start_story(service: GameService = Depends(get_game_service)):
    return service.start_game()


@app.post(
    '/game/{id}/choose',
    response_model=StoryAdvanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Advance a playthrough based on player choice',
)
def advance_story(
    id: str = Path(..., description='The ID of the playthrough to advance'),
    choice_info: ChoiceInfo = Body(
        ..., description="The player's choice for this turn"
    ),
    service: GameService = Depends(get_game_service),
):
    try:
        return service.advance_game(id, choice_info)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Playthrough {id} not found',
        )


@app.get(
    '/game/{id}',
    response_model=StoryStartResponse,
    summary='Get the state of the requested playthrough',
)
def get_playthrough(
    id: str = Path(..., description='The ID of the playthrough to retrieve'),
    service: GameService = Depends(get_game_service),
):
    try:
        state = service.get_session(id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Playthrough {id} not found'
        )

    return StoryStartResponse(
        playthrough_id=id,
        full=state.story[-1] if state.story else '',
        condensed=state.history[-1].ai if state.history else '',
        choices=state.current_choices,
    )


@app.delete(
    '/game/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete the requested playthrough',
)
def delete_playthrough(
    id: str = Path(..., description='The ID of the playthrough to delete'),
    service: GameService = Depends(get_game_service),
):
    deleted = service.uploader.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f'Playthrough {id} not found.')


@app.get(
    '/game/{id}/story',
    response_model=StoryRecapResponse,
    summary='Get the complete story so far of given playthrough',
)
def get_story_so_far(
    id: str = Path(..., description='The ID of the playthrough to retrieve'),
    service: GameService = Depends(get_game_service),
):
    try:
        state = service.get_session(id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Playthrough {id} not found'
        )

    return StoryRecapResponse(
        playthrough_id=id,
        story=state.story[:-1] if state.story else [],
    )


@app.get(
    '/game/{id}/ending',
    response_model=EndingSummaryResponse,
    summary='Get a summary of the playthrough and its consequences',
)
def get_playthrough_outcome(
    id: str = Path(..., description='The ID of the playthrough to retrieve'),
    service: GameService = Depends(get_game_service),
):
    try:
        return service.summarize_game(id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Playthrough {id} not found',
        )
