package com.guardian.model.dto;

public class ChatRequest {
    private String message;
    private String thread_id;

    public ChatRequest() {}

    public ChatRequest(String message, String thread_id) {
        this.message = message;
        this.thread_id = thread_id;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getThread_id() {
        return thread_id;
    }

    public void setThread_id(String thread_id) {
        this.thread_id = thread_id;
    }
}
