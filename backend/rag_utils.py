from youtube_transcript_api import YouTubeTranscriptApi
from huggingface_hub import InferenceClient
import re
import faiss
import numpy as np
from config import HUGGINGFACEHUB_API_TOKEN, EMBEDDING_MODEL, LLM_MODEL

# Initializing Hugging Face Inference Client
client = InferenceClient(token=HUGGINGFACEHUB_API_TOKEN)


# 1. Extracting YT Video ID (check & return video id)
def extract_video_id(url):
    patterns = [
        r"(?:v|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


# 2. Fetching Video Transcript (video id -> full transcript text)
def get_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        try:
            transcript_data = ytt_api.fetch(video_id, languages=["en"])
        except Exception:
            transcript_list = ytt_api.list(video_id)
            transcript_data = next(iter(transcript_list)).fetch()

        full_text = " ".join(item.text for item in transcript_data)
        return re.sub(r"\s+", " ", full_text)

    except Exception as e:
        print("Transcript error: ", e)
        return None
    

# 3. Splitting Transcript into Chunks (Full transcript -> split it into smaller chunks)
def split_text(text, chunk_size=150):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])  
        for i in range(0, len(words), chunk_size)
    ]


# 4. Creating Embeddings using Hugging Face
def create_embeddings(text_list):
    # HF Inference client returns a list of lists (embeddings) directly
    embeddings = client.feature_extraction(text=text_list, model=EMBEDDING_MODEL)
    return np.array(embeddings).astype("float32")


# 5. Building FAISS Index
def build_faiss_index(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape[1])      
    index.add(embeddings)       
    return index  


# 6. Retrieving Relevant Chunks
def retrieve_chunks(index, query_embedding, k=3):
    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"), k
    )
    return indices[0]


# 7. Asking Hugging Face LLM
def ask_llm(context, question):
    if not context.strip():
        return "Sorry, I couldn't find relevant information in the video transcript"
    
    # Truncate context to prevent token overflows
    context = context[:4000]

    prompt = f"""You are an AI assistant answering questions about a YouTube video. 
Always answer in English using the provided context.

Transcript Context:
{context}

Question:
{question}

Answer clearly in English:"""

    # Using the standard HF Chat Completion API (mirrors OpenAI's structure)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
           {"role": "system", "content": "You answer questions about YouTube videos based on the provided context."},
           {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content