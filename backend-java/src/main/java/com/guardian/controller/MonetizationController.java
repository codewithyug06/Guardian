package com.guardian.controller;

import com.guardian.model.User;
import com.guardian.service.tools.AuthService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api")
public class MonetizationController {

    private final AuthService authService;

    public MonetizationController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/checkout")
    public ResponseEntity<Map<String, String>> createCheckoutSession(
            @RequestHeader(value = "Authorization", required = false) String authHeader
    ) {
        return ResponseEntity.ok(Map.of(
                "url", "http://localhost:3000?payment_success=true",
                "session_id", "cs_test_mock_session_guardian"
        ));
    }

    @PostMapping("/webhook/stripe_mock_success")
    public ResponseEntity<Map<String, String>> stripeMockSuccess(
            @RequestHeader(value = "Authorization", required = false) String authHeader
    ) {
        User user = authService.getUserByToken(authHeader);
        if (user != null) {
            authService.upgradeToPro(user);
        }
        return ResponseEntity.ok(Map.of("status", "upgraded to pro", "tier", "ENTERPRISE_PRO"));
    }
}
