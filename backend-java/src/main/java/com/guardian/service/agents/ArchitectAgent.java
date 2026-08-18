package com.guardian.service.agents;

import com.guardian.model.AgentState;
import com.guardian.service.tools.MlAnomalyDetectionService;
import com.guardian.service.tools.PolicyEvolutionService;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class ArchitectAgent {

    private final PolicyEvolutionService policyService;
    private final MlAnomalyDetectionService mlService;

    public ArchitectAgent(PolicyEvolutionService policyService, MlAnomalyDetectionService mlService) {
        this.policyService = policyService;
        this.mlService = mlService;
    }

    public AgentState execute(AgentState state) {
        String jurisdiction = state.getJurisdiction() != null ? state.getJurisdiction() : "Global (PCI-DSS)";
        String latestReg = buildFallbackRegulation(jurisdiction);

        if (state.getFindings() != null && !state.getFindings().isEmpty()) {
            for (String f : state.getFindings()) {
                if (f.contains("Verified")) {
                    latestReg = f;
                    break;
                }
            }
        }

        String gapAnalysis = policyService.analyzeRegulatoryGap(latestReg);
        String risk = state.getRisk_level();

        String impact;
        String plan;

        if ("HIGH".equalsIgnoreCase(risk) || "CRITICAL".equalsIgnoreCase(risk)) {
            String fine = policyService.calculatePotentialFine(jurisdiction);
            impact = "ESTIMATED LIABILITY: " + fine;
            plan = String.format("ACTION REQUIRED: %s -> Recommendation: Deploy FIPS-140-3 AES-256 Tokenization & Access Gateway for %s.", gapAnalysis, jurisdiction);
        } else {
            impact = "Financial Exposure: Minimal";
            plan = "System Policy aligned with " + jurisdiction + ".";
        }

        String policyDraft = "";
        if (gapAnalysis.contains("VIOLATION")) {
            String currentPolicy = policyService.loadInternalPolicy();
            policyDraft = policyService.draftPolicyUpdate(currentPolicy, gapAnalysis);
        }

        List<String> policyGaps = new ArrayList<>();
        policyGaps.add(gapAnalysis);
        policyGaps.add(impact);

        double drift = mlService.calculateComplianceDrift(risk, policyGaps, state.getFindings());

        state.setRemediation_plan(plan);
        state.setEvidence_package(gapAnalysis + " | " + impact);
        state.setPolicy_gaps(policyGaps);
        state.setCompliance_drift(drift);
        state.setPolicy_update_proposal(policyDraft);

        return state;
    }

    private String buildFallbackRegulation(String jurisdiction) {
        if (jurisdiction.contains("GDPR")) {
            return "GDPR Article 32 mandates state-of-the-art encryption and pseudonymization for all personal data.";
        } else if (jurisdiction.contains("MAS")) {
            return "MAS Technology Risk Management Guidelines mandate strong encryption for customer data.";
        } else if (jurisdiction.contains("CCPA") || jurisdiction.contains("NIST")) {
            return "CCPA / NIST SP 800-53 controls mandate cryptographic protection for consumer PII.";
        }
        return "PCI-DSS 4.0 Requirement 3.4 for storing Primary Account Numbers (PAN)";
    }
}
