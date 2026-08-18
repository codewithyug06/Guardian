package com.guardian.model.dto;

public class AuditRequest {
    private boolean red_team_mode = false;
    private boolean federated_mode = false;
    private String jurisdiction = "Global (PCI-DSS)";
    private String image_base64;
    private String audio_base64;

    public AuditRequest() {}

    public boolean isRed_team_mode() {
        return red_team_mode;
    }

    public void setRed_team_mode(boolean red_team_mode) {
        this.red_team_mode = red_team_mode;
    }

    public boolean isFederated_mode() {
        return federated_mode;
    }

    public void setFederated_mode(boolean federated_mode) {
        this.federated_mode = federated_mode;
    }

    public String getJurisdiction() {
        return jurisdiction;
    }

    public void setJurisdiction(String jurisdiction) {
        this.jurisdiction = jurisdiction;
    }

    public String getImage_base64() {
        return image_base64;
    }

    public void setImage_base64(String image_base64) {
        this.image_base64 = image_base64;
    }

    public String getAudio_base64() {
        return audio_base64;
    }

    public void setAudio_base64(String audio_base64) {
        this.audio_base64 = audio_base64;
    }
}
