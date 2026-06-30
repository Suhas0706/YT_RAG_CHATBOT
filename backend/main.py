# file -> runs the FastAPI backend
from fastapi import FastAPI
from rag_utils import get_transcript, split_text, create_embeddings, build_faiss_index, retrieve_chunks, ask_llm
from rag_utils import extract_video_id
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chunks = []
index = None


@app.post("/process_video")
def process_video(url: str):
    global chunks, index

    video_id = extract_video_id(url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    
    text = get_transcript(video_id)
    if text is None:
        return {"error": "Transcript not available for this video"}
    
    chunks = split_text(text)
    embeddings = create_embeddings(chunks)
    index = build_faiss_index(embeddings)

    return {"message": "Video processed successfully"}


@app.post("/ask")
def ask(question: str):
    if index is None:
        return {"error": "Please process a video first"}
    
    try: 
        query_embedding = create_embeddings([question])[0]
        top_chunks = retrieve_chunks(index, query_embedding)
        if len(top_chunks) == 0:
            return {"answer": "No relevant context found in the video."}
        
        context_chunks = []
        for i in top_chunks:
            if i < len(chunks):
                context_chunks.append(chunks[i])

        context = " ".join(context_chunks)

        answer = ask_llm(context, question)
        return {"answer": answer}

    except Exception as e:
        print("Ask error: ", e)
        return {"error": str(e)}