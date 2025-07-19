# Auto News Cast: An Autonomous News-to-Video Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end, AI-driven News-to-Video pipeline orchestrated with **LangGraph**. This agent scrapes news headlines, generates AI-powered video scripts, and builds video content with voiceovers, all controlled via a **Streamlit** user interface.

The project's key feature is its robust, stateful **human-in-the-loop approval gate**, which pauses the workflow for human validation before final content creation and upload to YouTube.

*(Recommendation: Take a screenshot of your app in action and replace the placeholder URL below. You can drag-and-drop the image into a GitHub issue comment to get a URL.)*


---

## Features

-   **Multi-Source News Scraping:** Aggregates the latest headlines from **BBC News**, **CNN**, and **Al Jazeera**.
-   **High-Speed AI Summarization:** Uses **Llama 3** via the **Groq API** for rapid, high-quality script generation.
-   **Stateful Human Approval:** Employs LangGraph's `interrupt` and `checkpointer` features to pause the workflow for user approval of the generated script.
-   **AI-Powered Metadata:** Automatically generates SEO-friendly video titles and descriptions.
-   **Automated Multimedia Generation:** Synthesizes realistic voiceovers with the **ElevenLabs API** and assembles videos programmatically with **MoviePy**.
-   **End-to-End YouTube Upload:** Seamlessly uploads the final video to YouTube using the **v3 API** with **OAuth 2.0** authentication.
-   **Interactive Web UI:** A clean, easy-to-use **Streamlit** interface for controlling the agent and monitoring its status.

---

## The Workflow Explained

This agent is built as a state machine that can be paused and resumed based on human feedback. State is persisted throughout the process using an **SQLite checkpointer**, ensuring robustness even if the app is restarted.

*(Recommendation: Create a simple flowchart (e.g., using draw.io) and replace the placeholder URL below.)*


1.  **Scrape & Aggregate (`scrape` node):** The process begins by gathering headlines using `requests` and `BeautifulSoup`.
2.  **Summarize (`summarize` node):** The headlines are passed to Llama 3 to be synthesized into a concise video script.
3.  **Approve Script (`approval` interrupt):** This is the critical control point. The LangGraph workflow is explicitly **interrupted**, and its entire state is saved to the `graph.db` file. The Streamlit UI displays the script and waits for the user to click "yes" or "no".
4.  **Resume or Terminate (`final_decision` conditional edge):** Based on user input, the workflow either resumes to the next step or terminates gracefully.
5.  **Generate Metadata (`get_metadata` node):** Upon approval, an LLM is used again to create a suitable title and description for YouTube.
6.  **Create Video (`create_video` node):** The script is sent to ElevenLabs for voice synthesis. MoviePy then combines this audio with a simple background and text overlays to create the final `.mp4` file.
7.  **Upload (`upload` node):** The final video is pushed to YouTube using the YouTube Data API v3. OAuth 2.0 credentials are automatically handled and stored in `output/token.pickle` after the first authorization.

---

## 🛠️ Setup & Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

-   Python 3.9+
-   **ImageMagick**: Required by MoviePy for creating text overlays. [Download and install it](https://imagemagick.org/script/download.php), and make sure to note the path to its `magick.exe` executable.

### 2. Clone the Repository

```bash
git clone https://github.com/sadiakhalil125/Auto-News-Cast-Agent.git
cd your-repo-name
```

### 3. Install Dependencies

Create a virtual environment and install the required packages.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 4. Configure API Keys and Credentials

You will need to get API keys from the following services:
-   **Groq API:** For Llama 3 access.
-   **ElevenLabs API:** For voice synthesis.

Additionally, you need to set up **OAuth 2.0** for the YouTube API:
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  Enable the **"YouTube Data API v3"**.
4.  Create credentials for an **"OAuth client ID"**, selecting **"Desktop app"** as the application type.
5.  Download the `client_secret_....json` file and place it in the root of your project directory.

### 5. Update Configuration Files

Update the placeholder values in the following files:

-   **`nodes/summarize.py` & `nodes/getmetadata.py`**:
    -   Set your `GROQ_API_KEY`.
-   **`nodes/create_video.py`**:
    -   Set your `ELEVENLABS_API_KEY`.
    -   Update the `IMAGEMAGICK_BINARY` path to where you installed ImageMagick.
-   **`nodes/upload.py`**:
    -   Update the `CLIENT_SECRET_FILE` variable to match the name of your downloaded JSON file.

---

## ▶️ How to Run the Application

Once everything is configured, run the Streamlit app from your terminal:

```bash
streamlit run main.py
```

Your web browser should automatically open to the application's UI.

1.  Click **"🚀 Start Creation"** to begin the workflow.
2.  The process will run until it generates a script and then pause, waiting for your approval.
3.  Review the script in the UI and select "yes" or "no".
4.  If approved, the process will resume, create the video, and upload it.
5.  **Important:** The first time you upload, you will be prompted in your browser to authorize the application. This allows it to upload videos to your YouTube channel.

All generated files (`.mp3`, `.mp4`, `token.pickle`, `graph.db`) will be stored in the `/output` directory.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
