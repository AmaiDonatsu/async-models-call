```javascript
import axios from "axios";
import { store } from "../redux/store";
import { addLog, updateLog } from "../redux/NetworkSlicer";

const VITE_CALL_MODELS = import.meta.env.VITE_CALL_MODELS || 'http://127.0.0.1:8000';

const apiClient = axios.create({
    baseURL: VITE_CALL_MODELS,
    timeout: 10000,
});

const logRequest = async (description, type, method, payload, requestFn) => {
    const logId = `log-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const timestamp = new Date().toISOString();
    
    store.dispatch(addLog({
        logId,
        method,
        description,
        keyId: null,
        payload: JSON.stringify(payload),
        response: null,
        status: "pending",
        timestamp,
        type
    }));

    try {
        const response = await requestFn();
        store.dispatch(updateLog({
            logId,
            response: JSON.stringify(response),
            status: "completed"
        }));
        return response;
    } catch (error) {
        store.dispatch(updateLog({
            logId,
            response: JSON.stringify({ error: error.message }),
            status: "error"
        }));
        throw error;
    }
};

export const requestInference = async (imageBlob, texts) => {
    return logRequest("Inferencia SigLIP (Match)", "ModelRequest", "POST", { texts }, async () => {
        try {
            const formData = new FormData();
            formData.append("image", imageBlob, "image.png");
            formData.append("texts", JSON.stringify(texts));
            
            const response = await apiClient.post("/img-text-match", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            return response.data;
        } catch (error) {
            console.error("Error requesting inference:", error);
            throw error;
        }
    });
};

export { logRequest };```