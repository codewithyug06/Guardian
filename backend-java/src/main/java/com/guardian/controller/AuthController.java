package com.guardian.controller;

import com.guardian.model.dto.AuthResponse;
import com.guardian.model.dto.UserCreateRequest;
import com.guardian.service.tools.AuthService;
import org.springframework.http.ResponseEntity;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@RequestBody UserCreateRequest request) {
        AuthResponse response = authService.register(request);
        return ResponseEntity.ok(response);
    }

    @PostMapping(value = "/login", consumes = {"application/x-www-form-urlencoded", "application/json"})
    public ResponseEntity<AuthResponse> login(
            @RequestParam(required = false) MultiValueMap<String, String> formData,
            @RequestBody(required = false) UserCreateRequest jsonRequest
    ) {
        String username = null;
        String password = null;

        if (formData != null && formData.containsKey("username")) {
            username = formData.getFirst("username");
            password = formData.getFirst("password");
        } else if (jsonRequest != null) {
            username = jsonRequest.getEmail();
            password = jsonRequest.getPassword();
        }

        if (username == null || username.isBlank()) {
            username = "admin@guardian.ai";
        }

        AuthResponse response = authService.login(username, password);
        return ResponseEntity.ok(response);
    }
}
