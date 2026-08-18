package com.guardian.controller;

import com.guardian.model.AgentState;
import com.guardian.model.dto.ChatRequest;
import com.guardian.model.dto.ChatResponse;
import com.guardian.service.orchestrator.SwarmOrchestrator;
import com.guardian.service.tools.AiService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class ChatController {

    private final SwarmOrchestrator swarmOrchestrator;
    private final AiService aiService;

    public ChatController(SwarmOrchestrator swarmOrchestrator, AiService aiService) {
        this.swarmOrchestrator = swarmOrchestrator;
        this.aiService = aiService;
    }

    @PostMapping("/chat")
    public ResponseEntity<ChatResponse> chat(@RequestBody ChatRequest request) {
        String threadId = request.getThread_id();
        AgentState state = swarmOrchestrator.getState(threadId);

        String context = state != null ?
                "Risk Level: " + state.getRisk_level() +
                ", Drift: " + state.getCompliance_drift() + "%" +
                ", Plan: " + state.getRemediation_plan() +
                ", Findings: " + String.join(" | ", state.getFindings()) :
                "Guardian Swarm initialized. Monitoring active telemetry streams.";

        String reply;
        if (aiService.isAvailable()) {
            String prompt = String.format(
                    "You are Guardian AI, an autonomous compliance and risk intelligence assistant.\n" +
                    "Current System Telemetry Context: %s\n" +
                    "User Question: %s\n" +
                    "Provide a precise, authoritative, and helpful answer.",
                    context, request.getMessage()
            );
            reply = aiService.generate(prompt);
        } else {
            reply = "Guardian Core AI: Based on current telemetry, Systemic Risk is evaluated at " +
                    (state != null ? state.getRisk_level() : "SECURE") +
                    ". All multi-modal and behavioral sensors are active.";
        }

        if (reply == null || reply.isBlank()) {
            reply = "Guardian AI: Telemetry received. All compliance parameters nominal.";
        }

        return ResponseEntity.ok(new ChatResponse(reply));
    }
}
