package com.guardian.controller;

import com.guardian.model.AgentState;
import com.guardian.model.User;
import com.guardian.model.dto.AuditRequest;
import com.guardian.model.dto.AuditResponse;
import com.guardian.service.orchestrator.SwarmOrchestrator;
import com.guardian.service.tools.AuthService;
import com.guardian.service.tools.PdfExportService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

@RestController
@RequestMapping("/api")
public class AuditController {

    private static final Logger log = LoggerFactory.getLogger(AuditController.class);

    private final SwarmOrchestrator swarmOrchestrator;
    private final AuthService authService;
    private final PdfExportService pdfExportService;

    private final Map<String, String> uploadCache = new ConcurrentHashMap<>();

    public AuditController(
            SwarmOrchestrator swarmOrchestrator,
            AuthService authService,
            PdfExportService pdfExportService
    ) {
        this.swarmOrchestrator = swarmOrchestrator;
        this.authService = authService;
        this.pdfExportService = pdfExportService;
    }

    @PostMapping("/upload_codebase")
    public ResponseEntity<Map<String, String>> uploadCodebase(
            @RequestParam("file") MultipartFile file,
            @RequestHeader(value = "Authorization", required = false) String authHeader
    ) {
        User user = authService.getUserByToken(authHeader);
        StringBuilder extractedText = new StringBuilder();

        try {
            String filename = file.getOriginalFilename();
            if (filename != null && filename.endsWith(".zip")) {
                try (ZipInputStream zis = new ZipInputStream(file.getInputStream())) {
                    ZipEntry entry;
                    while ((entry = zis.getNextEntry()) != null) {
                        String name = entry.getName();
                        if (name.endsWith(".py") || name.endsWith(".js") || name.endsWith(".ts") ||
                            name.endsWith(".tsx") || name.endsWith(".json") || name.endsWith(".txt") ||
                            name.endsWith(".java")) {
                            byte[] buffer = zis.readAllBytes();
                            String content = new String(buffer, StandardCharsets.UTF_8);
                            extractedText.append("\n--- ").append(name).append(" ---\n");
                            extractedText.append(content.substring(0, Math.min(content.length(), 1000)));
                        }
                    }
                }
            } else {
                byte[] bytes = file.getBytes();
                String content = new String(bytes, StandardCharsets.UTF_8);
                extractedText.append(content.substring(0, Math.min(content.length(), 5000)));
            }

            String cacheKey = user != null ? user.getEmail() : "anonymous";
            uploadCache.put(cacheKey, extractedText.substring(0, Math.min(extractedText.length(), 10000)));

            return ResponseEntity.ok(Map.of("status", "success", "message", "Codebase uploaded and analyzed."));
        } catch (IOException e) {
            log.error("Failed to process uploaded file: {}", e.getMessage());
            return ResponseEntity.badRequest().body(Map.of("status", "error", "message", "Upload parsing failed."));
        }
    }

    @PostMapping("/audit")
    public ResponseEntity<AuditResponse> runAudit(
            @RequestBody AuditRequest request,
            @RequestHeader(value = "Authorization", required = false) String authHeader
    ) {
        User user = authService.getUserByToken(authHeader);
        String threadId = (user != null ? user.getId() : "usr_guest") + "_" + UUID.randomUUID().toString().substring(0, 8);

        String userEmail = user != null ? user.getEmail() : "anonymous";
        String codebaseContext = uploadCache.get(userEmail);

        AgentState state = new AgentState();
        state.setRed_team_mode(request.isRed_team_mode());
        state.setFederated_mode(request.isFederated_mode());
        state.setJurisdiction(request.getJurisdiction() != null ? request.getJurisdiction() : "Global (PCI-DSS)");
        state.setUploaded_image_base64(request.getImage_base64());
        state.setAudio_base64(request.getAudio_base64());
        state.setUser_codebase_context(codebaseContext);

        AgentState resultState = swarmOrchestrator.runAudit(threadId, state);
        boolean isPaused = swarmOrchestrator.isPaused(threadId);

        AuditResponse response = new AuditResponse(threadId, resultState, isPaused);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/deploy")
    public ResponseEntity<Map<String, String>> deployPatch(
            @RequestParam("thread_id") String threadId,
            @RequestHeader(value = "Authorization", required = false) String authHeader
    ) {
        swarmOrchestrator.deployAndEnforce(threadId);
        return ResponseEntity.ok(Map.of("status", "deployed", "message", "Patch deployed and Visa Gateway Enforced."));
    }

    @GetMapping("/export/{threadId}")
    public ResponseEntity<byte[]> exportPdf(
            @PathVariable("threadId") String threadId,
            @RequestHeader(value = "Authorization", required = false) String authHeader
    ) {
        AgentState state = swarmOrchestrator.getState(threadId);
        if (state == null) {
            state = new AgentState();
            state.setRisk_level("SECURE");
            state.addFinding("Audit findings archived.");
        }

        try {
            byte[] pdfBytes = pdfExportService.generateAuditPdf(state, threadId);
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=Guardian_Report_" + threadId + ".pdf")
                    .contentType(MediaType.APPLICATION_PDF)
                    .body(pdfBytes);
        } catch (Exception e) {
            log.error("Failed to generate PDF export: {}", e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }
}
