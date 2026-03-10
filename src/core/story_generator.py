from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session

from core.models import StoryLLMResponse, StoryNodeLLM
from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode


class StoryGenerator:
    @classmethod
    def _get_llm(cls) -> ChatOpenAI:
        return ChatOpenAI(model="gpt-4o-mini")

    @classmethod
    def genereate_story(
        cls, db: Session, session_id: str, theme: str = "fantasy:"
    ) -> Story:
        # Get LLM
        llm = cls._get_llm()

        # Get prompt
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = (
            ChatPromptTemplate()
            .from_messages(
                [
                    ("system", STORY_PROMPT),
                    ("human", f"Create the story with this theme: {theme}"),
                ]
            )
            .partial(format_instructions=story_parser.get_format_instructions)
        )

        # Send promt to LLM
        raw_response = llm.invoke(prompt.invoke({}))
        response_text = (
            raw_response.content if hasattr(raw_response, "content") else raw_response
        )

        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        # Get and validate root node data
        root_node_data = story_structure.root_node

        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        # Process story node, commit to db, and return story_db
        # (TODO: _process_story_node)

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(
        cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False
    ) -> StoryNode:
        pass
