from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session

from core.models import StoryLLMResponse, StoryNodeLLM
from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode

load_dotenv()


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

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", STORY_PROMPT),
                ("human", f"Create the story with this theme: {theme}"),
            ]
        ).partial(format_instructions=story_parser.get_format_instructions())

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
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(
        cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False
    ) -> StoryNode:
        # Get StoryNode
        node = StoryNode(
            story_id=story_id,
            content=(
                node_data.content
                if hasattr(node_data, "content")
                else node_data["content"]
            ),
            is_root=is_root,
            is_ending=(
                node_data.is_ending
                if hasattr(node_data, "isEnding")
                else node_data["isEnding"]
            ),
            is_winning_ending=(
                node_data.is_winning_ending
                if hasattr(node_data, "isWinningEnding")
                else node_data["isWinningEnding"]
            ),
            options=[],
        )

        db.add(node)
        db.flush()

        # Return if node does not have children (local max depth reached)
        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            return node

        # Recursive tree traversal (begin DFS)
        # (will get and validate child node data; then process and append)
        options_list = []

        for options_data in node_data.options:
            next_node = options_data.next_node

            if isinstance(next_node, dict):
                next_node = StoryNodeLLM.model_validate(next_node)

            child_node = cls._process_story_node(db, story_id, next_node, is_root=False)
            options_list.append({"text": options_data.text, "node_id": child_node.id})

        # Set node.options to options_list and return node (end DFS)
        node.options = options_list

        db.flush()
        return node
