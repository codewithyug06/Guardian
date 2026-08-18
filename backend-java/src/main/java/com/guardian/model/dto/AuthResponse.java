package com.guardian.model.dto;

public class AuthResponse {
    private String access_token;
    private String token_type = "bearer";
    private boolean is_pro = false;

    public AuthResponse() {}

    public AuthResponse(String access_token, String token_type, boolean is_pro) {
        this.access_token = access_token;
        this.token_type = token_type;
        this.is_pro = is_pro;
    }

    public String getAccess_token() {
        return access_token;
    }

    public void setAccess_token(String access_token) {
        this.access_token = access_token;
    }

    public String getToken_type() {
        return token_type;
    }

    public void setToken_type(String token_type) {
        this.token_type = token_type;
    }

    public boolean isIs_pro() {
        return is_pro;
    }

    public void setIs_pro(boolean is_pro) {
        this.is_pro = is_pro;
    }
}
