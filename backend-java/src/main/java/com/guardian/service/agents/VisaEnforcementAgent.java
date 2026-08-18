package com.guardian.service.agents;

import com.guardian.model.AgentState;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class VisaEnforcementAgent {

    public AgentState execute(AgentState state) {
        String risk = state.getRisk_level();
        List<String> findings = state.getFindings();

        boolean isUnderAttack = findings != null && (
                findings.stream().anyMatch(f -> f.contains("GHOST") || f.contains("RED-TEAM")) || "CRITICAL".equalsIgnoreCase(risk)
        );

        String action;
        String details;

        if (isUnderAttack) {
            action = "VISA GATEWAY: SAFE MODE ACTIVATED (KILL-SWITCH)";
            details = "CRITICAL THREAT DETECTED. Autonomous Kill-Switch triggered. Non-compliant transactions quarantined pending CCO review.";
        } else if ("HIGH".equalsIgnoreCase(risk)) {
            action = "VISA GATEWAY: CONDITIONAL BLOCK";
            details = "High risk detected. In-flight transactions queued for manual compliance sign-off.";
        } else {
            action = "VISA GATEWAY: AUTHORIZED";
            details = "Compliance checks passed. Real-time transaction flow operational.";
        }

        state.addFinding(action + " | " + details);
        return state;
    }
}
