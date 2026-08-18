package com.guardian.service.tools;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.guardian.model.AgentState;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Map;
import java.util.TreeMap;

@Service
public class CryptoAnchorService {

    private final ObjectMapper objectMapper = new ObjectMapper();

    public String generateDecisionHash(AgentState state) {
        try {
            // Create a sorted map for deterministic JSON serialization (Merkle leaf hashing)
            Map<String, Object> coreData = new TreeMap<>();
            coreData.put("risk", state.getRisk_level());
            coreData.put("plan", state.getRemediation_plan());
            coreData.put("code", state.getGenerated_code());
            coreData.put("consensus", state.getConsensus_audit());
            coreData.put("jurisdiction", state.getJurisdiction());
            coreData.put("drift", state.getCompliance_drift());

            String jsonString = objectMapper.writeValueAsString(coreData);
            return sha256Hex(jsonString);
        } catch (Exception e) {
            return "0x" + Long.toHexString(System.currentTimeMillis()) + "0000000000000000000000000000000000000000";
        }
    }

    public String sha256Hex(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm not available", e);
        }
    }
}
