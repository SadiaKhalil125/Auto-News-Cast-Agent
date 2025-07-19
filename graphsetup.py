# graphsetup.py
from langgraph.types import Command, interrupt
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.sqlite import SqliteSaver
from nodes.newsstate import NewsState
from nodes.scrape import scrape_and_return
from nodes.summarize import summarize_content
from nodes.approval import approve_decision,final_decision
from nodes.getmetadata import get_metadata
from nodes.create_video import create_video_with_elevenlabs
from nodes.upload import upload_video
import sqlite3


# SQLite checkpointer
db = sqlite3.connect("graph.db", check_same_thread=False)
memorybox = SqliteSaver(db)


def create_graph():
    
    # Build graph
    graph = StateGraph(NewsState)

    graph.add_node("scrape", scrape_and_return)
    graph.add_node("approval",approve_decision)
    graph.add_node("summarize", summarize_content)
    graph.add_node("get_metadata", get_metadata)
    graph.add_node("create_video", create_video_with_elevenlabs)
    graph.add_node("upload", upload_video)

   
    graph.add_edge("scrape", "summarize")
    graph.add_edge("summarize", "approval")
    graph.add_conditional_edges("approval", final_decision)
    graph.add_edge("get_metadata", "create_video")
    graph.add_edge("create_video", "upload")

    graph.set_entry_point("scrape")
    graph.set_finish_point("upload")

    return graph.compile(checkpointer=memorybox)

