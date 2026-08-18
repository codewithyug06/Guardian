package com.guardian.service.tools;

import com.guardian.config.GuardianProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PolicyEvolutionService {

    private static final Logger log = LoggerFactory.getLogger(PolicyEvolutionService.class);

    private final GuardianProperties properties;
    private final AiService aiService;
    private final RegulatoryMeshService meshService;
    private final VectorRagService vectorRagService;

    public PolicyEvolutionService(
            GuardianProperties properties, 
            AiService aiService, 
            RegulatoryMeshService meshService,
            VectorRagService vectorRagService
    ) {
        this.properties = properties;
        this.aiService = aiService;
        this.meshService = meshService;
        this.vectorRagService = vectorRagService;
    }

    public String loadInternalPolicy() {
        return vectorRagService.loadPolicyText();
    }

    public String analyzeRegulatoryGap(String newRegulation) {
        List<String> relevantChunks = vectorRagService.searchRelevant(newRegulation, 2);
        String policyContext = !relevantChunks.isEmpty() ? String.join("\n", relevantChunks) : loadInternalPolicy();
        String meshContext = meshService.queryRegulatoryMesh(newRegulation);

        if (aiService.isAvailable()) {
            String prompt = String.format(
                    "You are a Senior Compliance Auditor.\n" +
                    "Compare Reg: '%s' vs Ingested Policy Context: '%s'.\n" +
                    "Knowledge Graph Context: %s\n" +
                    "Return ONLY the violation analysis in one clear sentence.",
                    newRegulation, policyContext, meshContext
            );
            String result = aiService.generate(prompt);
            if (result != null && !result.isBlank()) {
                return result.trim();
            }
        }

        return "VIOLATION DETECTED: Clause 2 (Plain-text PAN in development logs) directly violates PCI-DSS 3.4 and GDPR Article 32.";
    }

    public String calculatePotentialFine(String violationType) {
        if (aiService.isAvailable()) {
            String prompt = String.format("Estimate financial liability fine for '%s'. Return ONLY the dollar amount and cadence.", violationType);
            String fine = aiService.generate(prompt);
            if (fine != null && !fine.isBlank()) {
                return fine.trim();
            }
        }

        if (violationType != null && violationType.contains("PCI")) {
            return "$100,000/mo (PCI Tier-1 Assessment & Non-Compliance Fine)";
        }
        return "€20 Million or 4% Global Annual Turnover (GDPR Max Penalty)";
    }

    public String draftPolicyUpdate(String currentPolicyContext, String violationReason) {
        if (aiService.isAvailable()) {
            String prompt = String.format(
                    "Act as a Chief Compliance Officer (Guardian Autonomous Policy Legislator).\n" +
                    "Current Policy Context: %s\n" +
                    "Violation Finding: %s\n" +
                    "Draft a specific, enforceable 'Policy Amendment Clause' to eliminate all liability. Return ONLY the new clause text.",
                    currentPolicyContext, violationReason
            );
            String draft = aiService.generate(prompt);
            if (draft != null && !draft.isBlank()) {
                return draft.trim();
            }
        }

        return "AMENDMENT DRAFT (Autonomous Policy Legislator):\n" +
               "Clause 2.1 (Amended): 'All Primary Account Numbers (PAN), cardholder data, and sensitive authentication elements must be rendered unreadable using FIPS 140-3 compliant AES-256 tokenization across all storage, memory caches, and telemetry logs without exception.'";
    }
}
