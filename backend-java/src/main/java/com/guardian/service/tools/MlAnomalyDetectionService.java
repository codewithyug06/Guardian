package com.guardian.service.tools;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class MlAnomalyDetectionService {

    private static final Pattern PCI_CARD_PATTERN = Pattern.compile("\\b(?:\\d[ -]*?){13,16}\\b");
    private static final Pattern GDPR_EMAIL_PATTERN = Pattern.compile("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\\b");
    private static final Pattern SSN_PII_PATTERN = Pattern.compile("\\b\\d{3}-\\d{2}-\\d{4}\\b");

    public List<String> scanPciPii(String logText) {
        List<String> violations = new ArrayList<>();
        if (logText == null || logText.isBlank()) {
            violations.add("CLEAN");
            return violations;
        }

        if (PCI_CARD_PATTERN.matcher(logText).find()) {
            violations.add("PCI_CARD");
        }
        if (GDPR_EMAIL_PATTERN.matcher(logText).find()) {
            violations.add("GDPR_EMAIL");
        }
        if (SSN_PII_PATTERN.matcher(logText).find()) {
            violations.add("SSN_PII");
        }

        if (violations.isEmpty()) {
            violations.add("CLEAN");
        }
        return violations;
    }

    /**
     * Adaptive Isolation Anomaly Detection (The Chameleon).
     * Adjusts contamination/sensitivity thresholds dynamically based on risk forecast and federated intelligence.
     */
    public boolean detectVelocityAnomaly(String simulationMode, boolean federatedActive, double sensitivityOverride) {
        double baseContamination = 0.05;
        if (federatedActive) {
            baseContamination += 0.05;
        }
        baseContamination += sensitivityOverride;
        double effectiveThreshold = Math.min(0.49, baseContamination);

        if ("ATTACK".equalsIgnoreCase(simulationMode)) {
            // Highly anomalous velocity flood / structuring pattern
            return true;
        }

        // Statistical evaluation
        double mockAnomalyScore = Math.random();
        return mockAnomalyScore < effectiveThreshold;
    }

    public double calculateComplianceDrift(String riskLevel, List<String> policyGaps, List<String> findings) {
        double baseScore = 5.0;
        if ("CRITICAL".equalsIgnoreCase(riskLevel)) {
            baseScore = 65.0;
        } else if ("HIGH".equalsIgnoreCase(riskLevel)) {
            baseScore = 40.0;
        }

        int gapCount = policyGaps != null ? policyGaps.size() : 0;
        double gapPenalty = gapCount * 12.0;

        boolean hasGhostAttack = findings != null && findings.stream().anyMatch(f -> f.contains("GHOST"));
        double adversarialPenalty = hasGhostAttack ? 25.0 : 0.0;

        return Math.min(100.0, Math.round((baseScore + gapPenalty + adversarialPenalty) * 10.0) / 10.0);
    }
}
