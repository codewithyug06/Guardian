package com.guardian.model.dto;

import com.guardian.model.AgentState;

public class AuditResponse {
    private String thread_id;
    private AgentState state;
    private boolean is_paused;

    public AuditResponse() {}

    public AuditResponse(String thread_id, AgentState state, boolean is_paused) {
        this.thread_id = thread_id;
        this.state = state;
        this.is_paused = is_paused;
    }

    public String getThread_id() {
        return thread_id;
    }

    public void setThread_id(String thread_id) {
        this.thread_id = thread_id;
    }

    public AgentState getState() {
        return state;
    }

    public void setState(AgentState state) {
        this.state = state;
    }

    public boolean isIs_paused() {
        return is_paused;
    }

    public void setIs_paused(boolean is_paused) {
        this.is_paused = is_paused;
    }
}
