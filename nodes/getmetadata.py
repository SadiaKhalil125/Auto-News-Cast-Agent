from langchain_openai import ChatOpenAI
from typing import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.messages import HumanMessage,SystemMessage
from nodes.newsstate import NewsState
from pydantic import BaseModel

class MetaData(BaseModel):
    title: str = Field(..., description="Title of the news video")
    description: str = Field(..., description="Description for the video")

def get_metadata(state: NewsState):
    script = state['script']
    parser = PydanticOutputParser(pydantic_object=MetaData) 
    prompt = ChatPromptTemplate.from_messages([
        ("system","You are an expert news summarizer."),
        ("human","""Given the following script, 
        give structured metadata for a video.
         
        Selected script: {script}
         
        Return only the structured output in this JSON format:
        {format_instructions}
        """)])
    
    full_prompt = prompt.format_messages(
        script=script,
        format_instructions=parser.get_format_instructions()
    )
    
    llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key="your-grok-api-key-here"  # Replace with your actual API key
    )
  
    result = llm.invoke(full_prompt)
    parsed = parser.parse(result.content)
    return {'title': parsed.title, 'description': parsed.description}
