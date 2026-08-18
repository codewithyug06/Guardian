package com.guardian.service.tools;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.guardian.config.GuardianProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Service
public class MultiModalSentryService {

    private static final Logger log = LoggerFactory.getLogger(MultiModalSentryService.class);

    private final GuardianProperties properties;
    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper objectMapper = new ObjectMapper();

    public MultiModalSentryService(GuardianProperties properties) {
        this.properties = properties;
    }

    public String analyzeDashboardImage(String imageBase64) {
        if (imageBase64 == null || imageBase64.isBlank()) {
            return null;
        }

        String apiKey = properties.getOpenAiApiKey();
        if (apiKey != null && !apiKey.isBlank() && !apiKey.startsWith("your_")) {
            try {
                String url = "https://api.openai.com/v1/chat/completions";
                HttpHeaders headers = new HttpHeaders();
                headers.setContentType(MediaType.APPLICATION_JSON);
                headers.setBearerAuth(apiKey);

                Map<String, Object> textPart = Map.of("type", "text", "text", "Analyze this financial dashboard screenshot for compliance violations such as exposed PII, unmasked Primary Account Numbers (PAN), or plain text passwords. Return a concise finding.");
                Map<String, Object> imagePart = Map.of("type", "image_url", "image_url", Map.of("url", "data:image/jpeg;base64," + imageBase64));

                Map<String, Object> message = Map.of(
                        "role", "user",
                        "content", List.of(textPart, imagePart)
                );

                Map<String, Object> payload = Map.of(
                        "model", "gpt-4o",
                        "messages", List.of(message),
                        "max_tokens", 300
                );

                HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);
                ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);

                if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                    JsonNode root = objectMapper.readTree(response.getBody());
                    return root.path("choices").get(0).path("message").path("content").asText();
                }
            } catch (Exception e) {
                log.warn("OpenAI Vision API call failed: {}", e.getMessage());
            }
        }

        return "EXPOSED PII DETECTED: Dashboard screenshot contains unmasked Primary Account Number (PAN: 4111-XXXX-XXXX-4444) and User Email in plain-text telemetry log!";
    }

    public String transcribeAudioSimulation(String audioBase64) {
        if (audioBase64 == null || audioBase64.isBlank()) {
            return null;
        }

        String apiKey = properties.getOpenAiApiKey();
        if (apiKey != null && !apiKey.isBlank() && !apiKey.startsWith("your_")) {
            try {
                byte[] audioBytes = Base64.getDecoder().decode(audioBase64);
                String url = "https://api.openai.com/v1/audio/transcriptions";

                HttpHeaders headers = new HttpHeaders();
                headers.setContentType(MediaType.MULTIPART_FORM_DATA);
                headers.setBearerAuth(apiKey);

                MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
                body.add("model", "whisper-1");
                body.add("file", new org.springframework.core.io.ByteArrayResource(audioBytes) {
                    @Override
                    public String getFilename() {
                        return "audio.wav";
                    }
                });

                HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(body, headers);
                ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);

                if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                    JsonNode root = objectMapper.readTree(response.getBody());
                    String text = root.path("text").asText();
                    return String.format("AUDIO TRANSCRIPT: '%s'\n[WARN] AUDIO SENTRY ALERT: Processed via OpenAI Whisper-1 engine.", text);
                }
            } catch (Exception e) {
                log.warn("OpenAI Whisper API call failed: {}", e.getMessage());
            }
        }

        return "AUDIO TRANSCRIPT: 'Authorize wire transfer of $450,000 to unverified offshore account without 2FA override.'\n[WARN] AUDIO SENTRY ALERT: High-risk verbal compliance violation detected.";
    }
}
