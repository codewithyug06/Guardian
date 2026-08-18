package com.guardian.service.agents;

import com.guardian.model.AgentState;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

@Component
public class GhostAgent {

    private final List<String> attackVectors = Arrays.asList(
            "RED-TEAM (GHOST): Injecting 'Structuring' Pattern -> 50x transactions of $9,900 (Evading $10k FinCEN threshold).",
            "RED-TEAM (GHOST): Attempting Policy Bypass -> Injecting obfuscated SQL/Hex payloads in transaction metadata.",
            "RED-TEAM (GHOST): Velocity Flood -> Simulating 10,000 requests/sec DDoS signature on card tokenization endpoint."
    );

    private final Random random = new Random();

    public AgentState execute(AgentState state) {
        if (!state.isRed_team_mode()) {
            return state;
        }

        String attack = attackVectors.get(random.nextInt(attackVectors.size()));
        state.addFinding(attack);
        return state;
    }
}
