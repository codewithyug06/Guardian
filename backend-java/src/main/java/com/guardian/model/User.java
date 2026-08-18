package com.guardian.model;

public class User {
    private String id;
    private String email;
    private boolean is_pro = false;

    public User() {}

    public User(String id, String email, boolean is_pro) {
        this.id = id;
        this.email = email;
        this.is_pro = is_pro;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public boolean isIs_pro() {
        return is_pro;
    }

    public void setIs_pro(boolean is_pro) {
        this.is_pro = is_pro;
    }
}
