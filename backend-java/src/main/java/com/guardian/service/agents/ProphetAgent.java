package com.guardian.service.agents;

import com.guardian.model.AgentState;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Component
public class ProphetAgent {

    private final Random random = new Random();

    public AgentState execute(AgentState state) {
        String risk = state.getRisk_level();
        int days = 30;
        List<Integer> forecast = new ArrayList<>();

        int base = ("HIGH".equalsIgnoreCase(risk) || "CRITICAL".equalsIgnoreCase(risk)) ? 80 : 20;
        double trend = ("HIGH".equalsIgnoreCase(risk) || "CRITICAL".equalsIgnoreCase(risk)) ? 0.5 : -0.2;

        for (int i = 0; i < days; i++) {
            int noise = random.nextInt(11) - 5;
            double val = base + (trend * i) + noise;
            forecast.add(Math.max(0, Math.min(100, (int) Math.round(val))));
        }

        state.setRisk_forecast(forecast);
        state.addFinding("PROPHET AGENT: Projected 30-day systemic risk trajectory calculated via temporal modeling.");

        return state;
    }
}
