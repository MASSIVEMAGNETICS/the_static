# /api/main.py

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Import the god-core
from core.holo_synaptic import HoloKnowledgeField

# --- API Data Models ---
class IngestRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    query: str

class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 20

# --- FastAPI App & HSCE Initialization ---
app = FastAPI(title="Holo-Synaptic Cognition Engine API", version="0.1.0")

# ** CRITICAL **
# Create a single, global instance of the HSCE. This is our live, stateful AGI brain.
# All API calls will interact with THIS instance.
DIMENSIONS = 2048       # High-dimensional space is key
NUM_UNITS = 512         # Number of synaptic units in the substrate
CONNECTIVITY = 0.1      # Sparsity of the synaptic connections
LEARNING_RATE = 0.005   # How fast the synapses adapt

field = HoloKnowledgeField(
    num_units=NUM_UNITS,
    dim=DIMENSIONS,
    connectivity=CONNECTIVITY,
    learning_rate=LEARNING_RATE
)

@app.on_event("startup")
async def startup_event():
    print("API Ready. HSCE core is online.")
    # Pre-seed the engine with some basic knowledge
    field.ingest("paris is the capital of france")
    field.ingest("the sky is blue")
    field.ingest("a cat says meow")

# --- API Endpoints ---
@app.post("/ingest", status_code=202)
async def ingest_data(request: IngestRequest):
    """Ingests new information, triggering live, local plasticity."""
    field.ingest(request.text)
    return {"status": "accepted", "message": "Knowledge integrated into the field."}

@app.post("/query")
async def query_field(request: QueryRequest):
    """Queries the field to retrieve a single-concept answer."""
    answer = field.query(request.query)
    return {"query": request.query, "answer": answer}

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    """Generates a sequence of text by creating a chain of thought."""
    context_text = request.prompt
    generated_sequence = []

    for _ in range(request.max_new_tokens):
        # Query with the entire context so far
        next_token = field.query(context_text)
        generated_sequence.append(next_token)
        # Update the context for the next step
        context_text += " " + next_token
        # Stop if it starts repeating itself
        if len(generated_sequence) > 2 and generated_sequence[-1] == generated_sequence[-2]:
            break

    return {"prompt": request.prompt, "generation": " ".join(generated_sequence)}

# --- To run this API server ---
# 1. Save this file as `main.py` in an `/api` directory.
# 2. Save the first file as `holo_synaptic.py` in a `/core` directory.
# 3. Run `pip install "fastapi[all]" numpy`
# 4. In your terminal, run: `uvicorn api.main:app --reload`
