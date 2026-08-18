package com.guardian.service.agents;

import com.guardian.model.AgentState;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

@Component
public class FederatedAgent {

    private final List<String> federatedThreats = Arrays.asList(
            "FED-NET (Peer Bank A): Detected 'Micro-Structuring' (<$100) velocity spikes across cross-border nodes.",
            "FED-NET (Peer Bank B): Global consensus weight update -> Obfuscated SQL injection mitigation activated.",
            "FED-NET (Global Consortium): Adjusting Isolation Forest contamination sensitivity baseline to 0.15."
    );

    private final Random random = new Random();

    public AgentState execute(AgentState state) {
        if (!state.isFederated_mode()) {
            return state;
        }

        String insight = federatedThreats.get(random.nextInt(federatedThreats.size()));
        state.addFederatedLog(insight);
        state.addFinding(insight);
        return state;
    }
}
