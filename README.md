**Auto News Cast**: An Autonomous News-to-Video Agent

![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)

An end-to-end, AI-driven News-to-Video pipeline orchestrated with LangGraph. This agent scrapes news headlines, generates AI-powered video scripts, and builds video content with voiceovers, all controlled via a Streamlit user interface.

The project's key feature is its robust, stateful human-in-the-loop approval gate, which pauses the workflow for human validation before final content creation and upload to YouTube.

![alt text](httpss://i.imgur.com/your-screenshot-url.png)

(Recommendation: Take a screenshot of your app in action and replace the URL above)

Features

Multi-Source News Scraping: Aggregates the latest headlines from BBC News, CNN, and Al Jazeera.

High-Speed AI Summarization: Uses Llama 3 via the Groq API for rapid, high-quality script generation.

Stateful Human Approval: Employs LangGraph's interrupt and checkpointer features to pause the workflow for user approval of the generated script.

AI-Powered Metadata: Automatically generates SEO-friendly video titles and descriptions.

Automated Multimedia Generation: Synthesizes realistic voiceovers with the ElevenLabs API and assembles videos programmatically with MoviePy.

End-to-End YouTube Upload: Seamlessly uploads the final video to YouTube using the v3 API with OAuth 2.0 authentication.

Interactive Web UI: A clean, easy-to-use Streamlit interface for controlling the agent and monitoring its status.

The Workflow Explained

This agent is built as a state machine that can be paused and resumed based on human feedback. State is persisted throughout the process using an SQLite checkpointer, ensuring robustness even if the app is restarted.

![alt text](httpss://i.imgur.com/your-workflow-diagram.png)

(Recommendation: Create a simple flowchart and replace the URL above)

Scrape & Aggregate (scrape node): The process begins by gathering headlines using requests and BeautifulSoup.

Summarize (summarize node): The headlines are passed to Llama 3 to be synthesized into a concise video script.

Approve Script (approval interrupt): This is the critical control point. The LangGraph workflow is explicitly interrupted, and its entire state is saved to the graph.db file. The Streamlit UI displays the script and waits for the user to click "yes" or "no".

Resume or Terminate (final_decision conditional edge): Based on user input, the workflow either resumes to the next step or terminates gracefully.

Generate Metadata (get_metadata node): Upon approval, an LLM is used again to create a suitable title and description for YouTube.

Create Video (create_video node): The script is sent to ElevenLabs for voice synthesis. MoviePy then combines this audio with a simple background and text overlays to create the final .mp4 file.

Upload (upload node): The final video is pushed to YouTube using the YouTube Data API v3. OAuth 2.0 credentials are automatically handled and stored in output/token.pickle after the first authorization.

🛠️ Setup & Installation

Follow these steps to get the project running on your local machine.

1. Prerequisites

Python 3.9+

ImageMagick: Required by MoviePy for creating text overlays. Make sure to install it and note the path to its magick.exe executable.

2. Clone the Repository
Generated bash
git clone https://github.com/sadiakhalil125/AI-News-Cast-Agent.git
cd your-repo-name

3. Install Dependencies

Create a virtual environment and install the required packages.

Generated bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
4. Configure API Keys and Credentials

You will need to get API keys from the following services:

Groq API: For Llama 3 access.

ElevenLabs API: For voice synthesis.

Additionally, you need to set up OAuth 2.0 for the YouTube API:

Go to the Google Cloud Console.

Create a new project.

Enable the "YouTube Data API v3".

Create credentials for an "OAuth client ID", selecting "Desktop app" as the application type.

Download the client_secret_....json file and place it in the root of your project directory.

5. Update Configuration Files

Update the placeholder values in the following files:

nodes/summarize.py & nodes/getmetadata.py:

Set your GROQ_API_KEY.

nodes/create_video.py:

Set your ELEVENLABS_API_KEY.

Update the IMAGEMAGICK_BINARY path to where you installed ImageMagick.

nodes/upload.py:

Update the CLIENT_SECRET_FILE variable to match the name of your downloaded JSON file.

▶️ How to Run the Application

Once everything is configured, run the Streamlit app from your terminal:

Generated bash
streamlit run main.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Your web browser should automatically open to the application's UI.

Click "🚀 Start Creation" to begin the workflow.

The process will run until it generates a script and then pause, waiting for your approval.

Review the script in the UI and select "yes" or "no".

If approved, the process will resume, create the video, and upload it.

The first time you upload, you will be prompted to authorize the application via your browser to allow it to upload videos to your YouTube channel.

All generated files (.mp3, .mp4, token.pickle, graph.db) will be stored in the /output directory.

License

This project is licensed under the MIT License. See the LICENSE file for details.
