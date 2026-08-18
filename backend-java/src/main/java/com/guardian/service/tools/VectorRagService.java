package com.guardian.service.tools;

import com.guardian.config.GuardianProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

@Service
public class VectorRagService {

    private static final Logger log = LoggerFactory.getLogger(VectorRagService.class);

    private final GuardianProperties properties;
    private final List<DocumentChunk> documentChunks = new ArrayList<>();

    public static class DocumentChunk {
        private final String content;
        private final Map<String, Double> termFrequencies;

        public DocumentChunk(String content) {
            this.content = content;
            this.termFrequencies = computeTf(content);
        }

        public String getContent() {
            return content;
        }

        private Map<String, Double> computeTf(String text) {
            Map<String, Double> tf = new HashMap<>();
            String[] tokens = text.toLowerCase().replaceAll("[^a-z0-9 ]", "").split("\\s+");
            double total = tokens.length;
            for (String t : tokens) {
                if (!t.isBlank()) {
                    tf.put(t, tf.getOrDefault(t, 0.0) + (1.0 / total));
                }
            }
            return tf;
        }

        public double cosineSimilarity(Map<String, Double> queryTf) {
            double dotProduct = 0.0;
            double normA = 0.0;
            double normB = 0.0;

            for (double v : termFrequencies.values()) normA += v * v;
            for (double v : queryTf.values()) normB += v * v;

            for (Map.Entry<String, Double> entry : queryTf.entrySet()) {
                if (termFrequencies.containsKey(entry.getKey())) {
                    dotProduct += entry.getValue() * termFrequencies.get(entry.getKey());
                }
            }

            if (normA == 0.0 || normB == 0.0) return 0.0;
            return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
        }
    }

    public VectorRagService(GuardianProperties properties) {
        this.properties = properties;
        indexInternalPolicy();
    }

    public void indexInternalPolicy() {
        String fullText = loadPolicyText();
        if (fullText == null || fullText.isBlank()) return;

        // Split by lines / clauses into chunks
        String[] lines = fullText.split("\n");
        for (String line : lines) {
            String trimmed = line.trim();
            if (!trimmed.isBlank() && trimmed.length() > 10) {
                documentChunks.add(new DocumentChunk(trimmed));
            }
        }
        log.info("Indexed {} chunks for in-memory Vector RAG store", documentChunks.size());
    }

    public String loadPolicyText() {
        try {
            Path path = Paths.get(properties.getPolicyFilePath());
            if (Files.exists(path)) {
                return Files.readString(path, StandardCharsets.UTF_8);
            }
        } catch (Exception ignored) {}

        try {
            ClassPathResource resource = new ClassPathResource("internal_policy.txt");
            try (InputStream is = resource.getInputStream()) {
                return new String(is.readAllBytes(), StandardCharsets.UTF_8);
            }
        } catch (Exception e) {
            return "GLOBAL FINANCIAL DATA HANDLING POLICY v2.1\n1. DATA RETENTION: User transaction logs shall be retained for 5 years.\n2. SENSITIVE DATA: Credit Card numbers (PAN) may be stored in plain text in dev logs.\n3. ENCRYPTION: Backups encrypted using AES-128.";
        }
    }

    public List<String> searchRelevant(String query, int topK) {
        if (documentChunks.isEmpty()) {
            indexInternalPolicy();
        }

        Map<String, Double> queryTf = new DocumentChunk(query).termFrequencies;
        List<Map.Entry<DocumentChunk, Double>> scored = new ArrayList<>();

        for (DocumentChunk chunk : documentChunks) {
            double score = chunk.cosineSimilarity(queryTf);
            scored.add(Map.entry(chunk, score));
        }

        scored.sort((a, b) -> Double.compare(b.getValue(), a.getValue()));

        List<String> results = new ArrayList<>();
        for (int i = 0; i < Math.min(topK, scored.size()); i++) {
            results.add(scored.get(i).getKey().getContent());
        }

        return results;
    }
}
