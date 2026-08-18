package com.guardian.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.List;

@Component
public class GuardianProperties {

    @Value("${guardian.openai.api-key:}")
    private String openAiApiKey;

    @Value("${guardian.openai.model:gpt-4o}")
    private String openAiModel;

    @Value("${guardian.supabase.url:}")
    private String supabaseUrl;

    @Value("${guardian.supabase.key:}")
    private String supabaseKey;

    @Value("${guardian.cors.allowed-origins:http://localhost:3000,http://127.0.0.1:3000}")
    private String allowedOriginsString;

    @Value("${guardian.policy.file-path:../internal_policy.txt}")
    private String policyFilePath;

    public String getOpenAiApiKey() {
        return openAiApiKey;
    }

    public String getOpenAiModel() {
        return openAiModel;
    }

    public String getSupabaseUrl() {
        return supabaseUrl;
    }

    public String getSupabaseKey() {
        return supabaseKey;
    }

    public List<String> getAllowedOrigins() {
        return Arrays.asList(allowedOriginsString.split(","));
    }

    public String getPolicyFilePath() {
        return policyFilePath;
    }
}
