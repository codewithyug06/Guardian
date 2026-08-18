package com.guardian.service.orchestrator;

import com.guardian.model.AgentState;
import com.guardian.service.agents.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class SwarmOrchestrator {

    private static final Logger log = LoggerFactory.getLogger(SwarmOrchestrator.class);

    private final ScoutAgent scoutAgent;
    private final GhostAgent ghostAgent;
    private final FederatedAgent federatedAgent;
    private final SentryAgent sentryAgent;
    private final ArchitectAgent architectAgent;
    private final CoderAgent coderAgent;
    private final MirrorAgent mirrorAgent;
    private final ConsensusAgent consensusAgent;
    private final ProphetAgent prophetAgent;
    private final VisaEnforcementAgent visaEnforcementAgent;

    // Checkpointer session storage (maps thread_id to state snapshot)
    private final Map<String, AgentState> stateStore = new ConcurrentHashMap<>();
    private final Map<String, Boolean> pauseStateStore = new ConcurrentHashMap<>();

    public SwarmOrchestrator(
            ScoutAgent scoutAgent,
            GhostAgent ghostAgent,
            FederatedAgent federatedAgent,
            SentryAgent sentryAgent,
            ArchitectAgent architectAgent,
            CoderAgent coderAgent,
            MirrorAgent mirrorAgent,
            ConsensusAgent consensusAgent,
            ProphetAgent prophetAgent,
            VisaEnforcementAgent visaEnforcementAgent
    ) {
        this.scoutAgent = scoutAgent;
        this.ghostAgent = ghostAgent;
        this.federatedAgent = federatedAgent;
        this.sentryAgent = sentryAgent;
        this.architectAgent = architectAgent;
        this.coderAgent = coderAgent;
        this.mirrorAgent = mirrorAgent;
        this.consensusAgent = consensusAgent;
        this.prophetAgent = prophetAgent;
        this.visaEnforcementAgent = visaEnforcementAgent;
    }

    /**
     * Executes the LangGraph-equivalent agent swarm workflow up to the human-in-the-loop checkpoint.
     */
    public AgentState runAudit(String threadId, AgentState initialState) {
        log.info("Initiating Swarm Audit workflow for threadId={}", threadId);

        AgentState state = initialState;

        // 1. Scout Discovery Node (with reflection loop)
        state = scoutAgent.execute(state);
        while ("Low".equalsIgnoreCase(state.getScout_confidence()) && state.getScout_retries() < 3) {
            log.debug("Scout confidence low, executing reflection retry {}", state.getScout_retries());
            state = scoutAgent.execute(state);
        }

        // 2. Ghost Adversarial Red Team Node
        state = ghostAgent.execute(state);

        // 3. Federated Intelligence Node
        state = federatedAgent.execute(state);

        // 4. Sentry Behavioral ML & Multi-modal Node
        state = sentryAgent.execute(state);

        // 5. Architect Strategy & Policy Evolution Node
        state = architectAgent.execute(state);

        // 6. Coder Remediation Node
        state = coderAgent.execute(state);

        // 7. Mirror Digital Twin Simulation Node (with simulation retry loop)
        state = mirrorAgent.execute(state);
        while (state.getDigital_twin_metrics() != null &&
               state.getDigital_twin_metrics().contains("FAIL") &&
               state.getCoder_retries() < 2) {
            log.debug("Digital twin failed, retrying code generation...");
            state = coderAgent.execute(state);
            state = mirrorAgent.execute(state);
        }

        // 8. Consensus Swarm Peer Review Node
        state = consensusAgent.execute(state);

        // 9. Prophet Predictive Temporal Forecasting Node
        state = prophetAgent.execute(state);

        // Check human-in-the-loop interruption condition:
        // Pause if high/critical risk and a patch requires approval before Visa Guard edge execution
        boolean hasGeneratedCode = state.getGenerated_code() != null &&
                !state.getGenerated_code().isBlank() &&
                !state.getGenerated_code().contains("# System Nominal");

        boolean shouldPause = hasGeneratedCode || "HIGH".equalsIgnoreCase(state.getRisk_level()) || "CRITICAL".equalsIgnoreCase(state.getRisk_level());

        stateStore.put(threadId, state);
        pauseStateStore.put(threadId, shouldPause);

        return state;
    }

    /**
     * Resumes the paused workflow after human approval (Deploy Patch / Enforce Visa Guard).
     */
    public AgentState deployAndEnforce(String threadId) {
        log.info("Resuming workflow and enforcing Visa Gateway for threadId={}", threadId);
        AgentState state = stateStore.getOrDefault(threadId, new AgentState());

        // Execute Visa Guard Enforcement Node
        state = visaEnforcementAgent.execute(state);

        // Mark as fully remediated
        state.setRisk_level("SECURE");
        state.setCompliance_drift(0.0);
        stateStore.put(threadId, state);
        pauseStateStore.put(threadId, false);

        return state;
    }

    public AgentState getState(String threadId) {
        return stateStore.get(threadId);
    }

    public boolean isPaused(String threadId) {
        return pauseStateStore.getOrDefault(threadId, false);
    }

    public void updateState(String threadId, AgentState state) {
        stateStore.put(threadId, state);
    }
}
