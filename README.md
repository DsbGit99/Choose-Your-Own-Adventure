# Choose Your Own Adventure AI (Spring 2026)

A RESTful web API allowing users to interact with an LLM (OpenAI GPT, via LangChain) to generate adventures.
Uses a React frontend and a FastAPI backend, connecting to a SQL database (SQLite locally) using SQLAlchemy ORM.

## What happens when using it?

A user is initially presented with a form asking for a story-theme input. Once the form is filled and submitted for processing, a loading screen will appear until the story-generation job on the backend exits the "processing" status and returns either "failed" (in which case a fallback UI is provided where the user is displayed an error) or "completed" (in which case a new story URL is created, to which the user is redirected).

The story is a binary tree of a height predetermined in the backend. The root node is the beginning of the story, edges are the choices users make, and nodes are the consequences of the user's choices. At the bottom of the tree, there will be one node reached by one path that will be "winning".

The user may continue or reattempt their generated story, or they may opt to go back to the theme-input page and generate a new story.

## How can it be used?

Currently, this app only runs locally. Upon cloning this repo from the root of the project, open two terminals:

### Backendend terminal
1) `cd backend`
2) `source .venv/Scripts/activate` (or `. .venv/Scripts/activate`)
3) `uv pip install -e .`
4) `uvicorn src/main:app` (will run on `localhost::8000`)

### Frontend terminal
1) `cd frontend`
2) `npm i`
1) `npm audit fix` (optional)
2) `npm run dev` (will run on `localhost::5173`)

## Acknowledgements
Credit to *Tech with Tim* on YouTube for providing a [project tutorial](https://www.youtube.com/watch?v=_1P0Uqk50Ps).

**NOTE:** This is a pedagogical project. I have followed along while providing code comments, improvements, modernization as I see fit along the way.
