package com.guardian.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;

import java.util.ArrayList;
import java.util.List;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class AgentState {

    private List<String> findings = new ArrayList<>();
    private String risk_level = "UNKNOWN";
    private String remediation_plan = "";
    private String evidence_package = "";
    private List<String> policy_gaps = new ArrayList<>();

    // Reflection & Scout
    private int scout_retries = 0;
    private String scout_confidence = "High";

    // Coder & Gen AI
    private String generated_code = "";
    private int coder_retries = 0;

    // Predictive ML
    private List<Integer> risk_forecast = new ArrayList<>();

    // Multi-modal data
    private String uploaded_image_base64;
    private String audio_base64;
    private String user_codebase_context;

    // Adversarial & Federated
    private boolean red_team_mode = false;
    private boolean federated_mode = false;
    private List<String> federated_logs = new ArrayList<>();

    // Trust & Robustness
    private List<String> consensus_audit = new ArrayList<>();
    private double compliance_drift = 0.0;
    private String jurisdiction = "Global (PCI-DSS)";

    // Extraordinary features
    private String digital_twin_metrics = "";
    private List<String> vendor_risks = new ArrayList<>();
    private String decision_hash = "PENDING_COMPUTATION";
    private String policy_update_proposal = "";
    private double adaptive_sensitivity = 0.0;

    public AgentState() {}

    public List<String> getFindings() {
        return findings;
    }

    public void setFindings(List<String> findings) {
        this.findings = findings;
    }

    public void addFinding(String finding) {
        if (this.findings == null) this.findings = new ArrayList<>();
        this.findings.add(finding);
    }

    public String getRisk_level() {
        return risk_level;
    }

    public void setRisk_level(String risk_level) {
        this.risk_level = risk_level;
    }

    public String getRemediation_plan() {
        return remediation_plan;
    }

    public void setRemediation_plan(String remediation_plan) {
        this.remediation_plan = remediation_plan;
    }

    public String getEvidence_package() {
        return evidence_package;
    }

    public void setEvidence_package(String evidence_package) {
        this.evidence_package = evidence_package;
    }

    public List<String> getPolicy_gaps() {
        return policy_gaps;
    }

    public void setPolicy_gaps(List<String> policy_gaps) {
        this.policy_gaps = policy_gaps;
    }

    public void addPolicyGap(String gap) {
        if (this.policy_gaps == null) this.policy_gaps = new ArrayList<>();
        this.policy_gaps.add(gap);
    }

    public int getScout_retries() {
        return scout_retries;
    }

    public void setScout_retries(int scout_retries) {
        this.scout_retries = scout_retries;
    }

    public String getScout_confidence() {
        return scout_confidence;
    }

    public void setScout_confidence(String scout_confidence) {
        this.scout_confidence = scout_confidence;
    }

    public String getGenerated_code() {
        return generated_code;
    }

    public void setGenerated_code(String generated_code) {
        this.generated_code = generated_code;
    }

    public int getCoder_retries() {
        return coder_retries;
    }

    public void setCoder_retries(int coder_retries) {
        this.coder_retries = coder_retries;
    }

    public List<Integer> getRisk_forecast() {
        return risk_forecast;
    }

    public void setRisk_forecast(List<Integer> risk_forecast) {
        this.risk_forecast = risk_forecast;
    }

    public String getUploaded_image_base64() {
        return uploaded_image_base64;
    }

    public void setUploaded_image_base64(String uploaded_image_base64) {
        this.uploaded_image_base64 = uploaded_image_base64;
    }

    public String getAudio_base64() {
        return audio_base64;
    }

    public void setAudio_base64(String audio_base64) {
        this.audio_base64 = audio_base64;
    }

    public String getUser_codebase_context() {
        return user_codebase_context;
    }

    public void setUser_codebase_context(String user_codebase_context) {
        this.user_codebase_context = user_codebase_context;
    }

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

    public List<String> getFederated_logs() {
        return federated_logs;
    }

    public void setFederated_logs(List<String> federated_logs) {
        this.federated_logs = federated_logs;
    }

    public void addFederatedLog(String log) {
        if (this.federated_logs == null) this.federated_logs = new ArrayList<>();
        this.federated_logs.add(log);
    }

    public List<String> getConsensus_audit() {
        return consensus_audit;
    }

    public void setConsensus_audit(List<String> consensus_audit) {
        this.consensus_audit = consensus_audit;
    }

    public void addConsensusAudit(String audit) {
        if (this.consensus_audit == null) this.consensus_audit = new ArrayList<>();
        this.consensus_audit.add(audit);
    }

    public double getCompliance_drift() {
        return compliance_drift;
    }

    public void setCompliance_drift(double compliance_drift) {
        this.compliance_drift = compliance_drift;
    }

    public String getJurisdiction() {
        return jurisdiction;
    }

    public void setJurisdiction(String jurisdiction) {
        this.jurisdiction = jurisdiction;
    }

    public String getDigital_twin_metrics() {
        return digital_twin_metrics;
    }

    public void setDigital_twin_metrics(String digital_twin_metrics) {
        this.digital_twin_metrics = digital_twin_metrics;
    }

    public List<String> getVendor_risks() {
        return vendor_risks;
    }

    public void setVendor_risks(List<String> vendor_risks) {
        this.vendor_risks = vendor_risks;
    }

    public void addVendorRisk(String risk) {
        if (this.vendor_risks == null) this.vendor_risks = new ArrayList<>();
        this.vendor_risks.add(risk);
    }

    public String getDecision_hash() {
        return decision_hash;
    }

    public void setDecision_hash(String decision_hash) {
        this.decision_hash = decision_hash;
    }

    public String getPolicy_update_proposal() {
        return policy_update_proposal;
    }

    public void setPolicy_update_proposal(String policy_update_proposal) {
        this.policy_update_proposal = policy_update_proposal;
    }

    public double getAdaptive_sensitivity() {
        return adaptive_sensitivity;
    }

    public void setAdaptive_sensitivity(double adaptive_sensitivity) {
        this.adaptive_sensitivity = adaptive_sensitivity;
    }
}
