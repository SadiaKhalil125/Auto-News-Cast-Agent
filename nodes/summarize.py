from langchain_openai import ChatOpenAI
from typing import TypedDict
from langchain_core.prompts import PromptTemplate
from pydantic import Field
from langchain_core.output_parsers import StrOutputParser
from nodes.newsstate import NewsState


def summarize_content(state: NewsState):
    bbc = state['bbc_headlines']
    cnn = state['cnn_headlines']
    al_jazeera = state['al_jazeera_headlines']

    prompt = PromptTemplate(
        template="""You are a news summarizer.
        Summarize the following headlines from BBC, CNN, and Al Jazeera into a concise script for a video.
        BBC Headlines: {bbc}
        CNN Headlines: {cnn}
        Al Jazeera Headlines: {al_jazeera}

        Choose the suitable headlines among the three headlines and create an engaging script of around 100 words.
        The script should be informative and suitable for a video format.
        Ensure to include key points from each source without unnecessary repetition.
        return only script without any other text.
        
        """,
        input_variables=["bbc", "cnn", "al_jazeera"])
    
    llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key="your-grok-api-key-here"  # Replace with your actual API key
    )
    
    parser = StrOutputParser()
    chain = prompt | llm | parser
    script = chain.invoke({
        "bbc": bbc,
        "cnn": cnn,
        "al_jazeera": al_jazeera
    })
    return {'script': script}
