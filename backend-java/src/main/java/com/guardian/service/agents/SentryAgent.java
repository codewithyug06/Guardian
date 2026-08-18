package com.guardian.service.agents;

import com.guardian.model.AgentState;
import com.guardian.service.tools.MlAnomalyDetectionService;
import com.guardian.service.tools.MultiModalSentryService;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class SentryAgent {

    private final MlAnomalyDetectionService mlService;
    private final MultiModalSentryService multiModalService;

    public SentryAgent(MlAnomalyDetectionService mlService, MultiModalSentryService multiModalService) {
        this.mlService = mlService;
        this.multiModalService = multiModalService;
    }

    public AgentState execute(AgentState state) {
        String targetPayload = state.getUser_codebase_context();
        if (targetPayload == null || targetPayload.isBlank()) {
            targetPayload = "Payment processed for user@financial-hub.com using card 4111-2222-3333-4444 in plain-text telemetry buffer.";
        }

        List<String> staticRisks = mlService.scanPciPii(targetPayload);

        String simMode = state.isRed_team_mode() ? "ATTACK" : "NORMAL";
        boolean fedMode = state.isFederated_mode();

        double sensitivityBoost = 0.0;
        List<Integer> forecast = state.getRisk_forecast();
        if (forecast != null && !forecast.isEmpty()) {
            int maxRisk = forecast.stream().mapToInt(v -> v).max().orElse(0);
            if (maxRisk > 50) {
                sensitivityBoost = 0.15;
            }
        }

        boolean isAnomaly = mlService.detectVelocityAnomaly(simMode, fedMode, sensitivityBoost);

        String status = "LOW";

        if (staticRisks.contains("PCI_CARD") && staticRisks.contains("GDPR_EMAIL")) {
            state.addFinding("[SYSTEMIC RISK]: Simultaneous PCI-DSS 3.4 (Card PAN) + GDPR Article 32 (Exposed Email) Violation Detected in data stream.");
            status = "CRITICAL";
        } else if (staticRisks.contains("PCI_CARD")) {
            state.addFinding("[SENTRY ALERT]: Unmasked Primary Account Number (PAN) detected in unencrypted buffer.");
            status = "HIGH";
        } else if (staticRisks.contains("GDPR_EMAIL")) {
            state.addFinding("[SENTRY ALERT]: PII Email address logged without pseudonymization.");
            status = "HIGH";
        }

        if (isAnomaly) {
            String alertType = fedMode ? "FEDERATED" : "LOCAL";
            state.addFinding(String.format("[BEHAVIORAL ALERT] (%s INTELLIGENCE): Velocity Anomaly Detected (Adaptive Sensitivity +%s).", alertType, sensitivityBoost));
            if (!"CRITICAL".equals(status)) {
                status = "HIGH";
            }
        }

        String visionFinding = multiModalService.analyzeDashboardImage(state.getUploaded_image_base64());
        if (visionFinding != null) {
            state.addFinding("VISION SENTRY: " + visionFinding);
            status = "CRITICAL";
        }

        String audioFinding = multiModalService.transcribeAudioSimulation(state.getAudio_base64());
        if (audioFinding != null) {
            state.addFinding("AUDIO SENTRY: " + audioFinding);
            if (!"CRITICAL".equals(status)) {
                status = "HIGH";
            }
        }

        state.setRisk_level(status);
        state.setAdaptive_sensitivity(sensitivityBoost);

        return state;
    }
}
