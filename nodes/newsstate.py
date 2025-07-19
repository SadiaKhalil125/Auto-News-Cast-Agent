from typing import TypedDict, List

# This is the single, authoritative definition of our workflow's state.
# total=False means all fields are optional, which is crucial for LangGraph.
class NewsState(TypedDict, total=False):
    title: str
    description: str
    bbc_headlines: List[str]
    cnn_headlines: List[str]
    al_jazeera_headlines: List[str]
    script: str
    script_approved: str 
    video_path: str
    audio_path: str
    upload_status: str