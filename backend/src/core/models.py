from typing import Any

from pydantic import BaseModel, Field

# BaseModel schemas for use by LLM.


class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text of the option shown to the user")
    next_node: dict[str, Any] = Field(
        description="The next node content and its options"
    )


class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    is_ending: bool = Field(description="Whether this node is an ending node")
    is_winning_ending: bool = Field(
        description="Whether this node is a winning ending node"
    )
    options: list[StoryOptionLLM] | None = Field(
        default=None, description="The options for this node"
    )


class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    root_node: StoryNodeLLM = Field(description="The root node of the story")
