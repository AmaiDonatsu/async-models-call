# async-models-call

## Usage
async-models-call is a high-performance inference server designed to integrate seamlessly with the asyncControl ecosystem. It specializes in serving lightweight, open-source models optimized for local execution, specifically acting as the backend engine for "Tools" functionality.

By leveraging ONNX Runtime, this server ensures low-latency responses and efficient resource utilization, making it ideal for edge computing or local AI deployments.

## Supported Models
The project currently supports two primary pillars of modern NLP and Vision-Language processing:

*   **MS MARCO (Re-ranking)**:
    *   **ID**: `cross-encoder/ms-marco-MiniLM-L6-v2`
    *   **Source**: [Hugging Face](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2)
    *   **Usage**: Optimized for calculating relevance scores between query-passage pairs. Essential for high-accuracy RAG (Retrieval-Augmented Generation) pipelines.
*   **SigLIP (Image-Text Matching)**:
    *   **ID**: `google/siglip-so400m-patch14-384`
    *   **Source**: [Hugging Face](https://huggingface.co/google/siglip-so400m-patch14-384)
    *   **Usage**: State-of-the-art image-text matching. It allows for advanced visual understanding and zero-shot image classification without retraining.


## Installation

Follow these steps to configure and run the API in your local environment:

### 1. Install dependencies
Ensure you have an active virtual environment and run:
```bash
pip install -r requirements.txt
```

### 2. Convert models to ONNX
To ensure efficient execution, the models must be in ONNX format within the `/models` directory.

*   **For MS MARCO**: Run the export script included:
    ```bash
    python scripts/export_ms_marco_onnx.py
    ```
*   **For SigLIP**: Ensure the ONNX files are present in `models/siglip_onnx/`. (pending script)

### 3. Run the server
Once dependencies are installed and models are prepared, start the API with:
```bash
python server.py
```

The server will start by default at `http://127.0.0.1:8000`.

---
*Developed to work in conjunction with asyncControl.*

<img src="assets/character.webp" alt="Gemini_Generated_Image_fem6h5fem6h5fem6" size=".6">

source: https://wallpapersafari.com/frutiger-aero-aesthetic-wallpapers/
img link: https://wallpapercave.com/wp/wp13865960.jpg
