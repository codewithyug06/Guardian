package com.guardian.service.agents;

import com.guardian.model.AgentState;
import com.guardian.service.tools.DigitalTwinSimulationService;
import org.springframework.stereotype.Component;

@Component
public class MirrorAgent {

    private final DigitalTwinSimulationService simulationService;

    public MirrorAgent(DigitalTwinSimulationService simulationService) {
        this.simulationService = simulationService;
    }

    public AgentState execute(AgentState state) {
        String code = state.getGenerated_code();
        String report = simulationService.simulateDigitalTwin(code);
        state.setDigital_twin_metrics(report);
        return state;
    }
}
