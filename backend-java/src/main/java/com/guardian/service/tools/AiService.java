package com.guardian.service.tools;

import com.guardian.config.GuardianProperties;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.Duration;

@Service
public class AiService {

    private static final Logger log = LoggerFactory.getLogger(AiService.class);

    private final GuardianProperties properties;
    private ChatLanguageModel chatModel;

    public AiService(GuardianProperties properties) {
        this.properties = properties;
        initModel();
    }

    private void initModel() {
        String apiKey = properties.getOpenAiApiKey();
        if (apiKey != null && !apiKey.isBlank() && !apiKey.startsWith("your_")) {
            try {
                this.chatModel = OpenAiChatModel.builder()
                        .apiKey(apiKey)
                        .modelName(properties.getOpenAiModel())
                        .temperature(0.0)
                        .timeout(Duration.ofSeconds(60))
                        .build();
                log.info("LangChain4j OpenAiChatModel initialized successfully with model {}", properties.getOpenAiModel());
            } catch (Exception e) {
                log.warn("Failed to initialize LangChain4j OpenAiChatModel: {}", e.getMessage());
                this.chatModel = null;
            }
        } else {
            log.info("No OpenAI API key provided. Using intelligent autonomous heuristic fallback modes.");
            this.chatModel = null;
        }
    }

    public boolean isAvailable() {
        return this.chatModel != null;
    }

    public String generate(String prompt) {
        if (this.chatModel != null) {
            try {
                return this.chatModel.generate(prompt);
            } catch (Exception e) {
                log.error("Error executing LLM generation: {}", e.getMessage());
            }
        }
        return null;
    }
}
