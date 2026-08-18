package com.guardian.service.tools;

import com.guardian.config.GuardianProperties;
import com.guardian.model.User;
import com.guardian.model.dto.AuthResponse;
import com.guardian.model.dto.UserCreateRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class AuthService {

    private static final Logger log = LoggerFactory.getLogger(AuthService.class);

    private final GuardianProperties properties;
    private final Map<String, User> userDatabase = new ConcurrentHashMap<>();
    private final Map<String, User> tokenSessions = new ConcurrentHashMap<>();

    public AuthService(GuardianProperties properties) {
        this.properties = properties;
        // Default admin user
        User admin = new User("usr_admin_001", "admin@guardian.ai", true);
        userDatabase.put("admin@guardian.ai", admin);
    }

    public AuthResponse register(UserCreateRequest request) {
        String email = request.getEmail();
        User existing = userDatabase.get(email);
        if (existing != null) {
            String token = "jwt_" + UUID.randomUUID().toString().replace("-", "");
            tokenSessions.put(token, existing);
            return new AuthResponse(token, "bearer", existing.isIs_pro());
        }

        User newUser = new User("usr_" + UUID.randomUUID().toString().substring(0, 8), email, false);
        userDatabase.put(email, newUser);
        String token = "jwt_" + UUID.randomUUID().toString().replace("-", "");
        tokenSessions.put(token, newUser);

        return new AuthResponse(token, "bearer", false);
    }

    public AuthResponse login(String username, String password) {
        User user = userDatabase.computeIfAbsent(username, email ->
                new User("usr_" + UUID.randomUUID().toString().substring(0, 8), email, false)
        );

        String token = "jwt_" + UUID.randomUUID().toString().replace("-", "");
        tokenSessions.put(token, user);

        return new AuthResponse(token, "bearer", user.isIs_pro());
    }

    public User getUserByToken(String authHeader) {
        if (authHeader == null || authHeader.isBlank()) {
            return new User("usr_anonymous", "anon@guardian.ai", false);
        }

        String token = authHeader.replace("Bearer ", "").trim();
        return tokenSessions.getOrDefault(token, new User("usr_guest", "guest@guardian.ai", false));
    }

    public void upgradeToPro(User user) {
        if (user != null) {
            user.setIs_pro(true);
            userDatabase.put(user.getEmail(), user);
        }
    }
}
