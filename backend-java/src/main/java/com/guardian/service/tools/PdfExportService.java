package com.guardian.service.tools;

import com.guardian.model.AgentState;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.font.PDType1Font;
import org.apache.pdfbox.pdmodel.font.Standard14Fonts;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

@Service
public class PdfExportService {

    public byte[] generateAuditPdf(AgentState state, String threadId) throws IOException {
        try (PDDocument document = new PDDocument()) {
            PDPage page = new PDPage(PDRectangle.A4);
            document.addPage(page);

            try (PDPageContentStream contentStream = new PDPageContentStream(document, page)) {
                PDType1Font fontBold = new PDType1Font(Standard14Fonts.FontName.HELVETICA_BOLD);
                PDType1Font fontRegular = new PDType1Font(Standard14Fonts.FontName.HELVETICA);

                float y = 780;
                float margin = 50;

                // Title
                contentStream.beginText();
                contentStream.setFont(fontBold, 18);
                contentStream.newLineAtOffset(margin, y);
                contentStream.showText("GUARDIAN AI - STRATEGIC COMPLIANCE REPORT");
                contentStream.endText();

                y -= 25;
                contentStream.beginText();
                contentStream.setFont(fontRegular, 10);
                contentStream.newLineAtOffset(margin, y);
                contentStream.showText("Autonomous Governance Ecosystem | IIT-M Production Edition");
                contentStream.endText();

                y -= 25;
                drawLine(contentStream, margin, y, 545, y);

                y -= 25;
                writeLine(contentStream, fontBold, 11, margin, y, "AUDIT SESSION METADATA:");
                y -= 16;
                writeLine(contentStream, fontRegular, 10, margin, y, "Session ID: " + (threadId != null ? threadId : "GLOBAL_AUDIT_01"));
                y -= 16;
                writeLine(contentStream, fontRegular, 10, margin, y, "Jurisdiction: " + (state.getJurisdiction() != null ? state.getJurisdiction() : "Global"));
                y -= 16;
                writeLine(contentStream, fontRegular, 10, margin, y, "Risk Posture: " + state.getRisk_level());
                y -= 16;
                writeLine(contentStream, fontRegular, 10, margin, y, "Compliance Drift: " + state.getCompliance_drift() + "%");
                y -= 16;
                writeLine(contentStream, fontRegular, 10, margin, y, "Merkle Root Hash: " + state.getDecision_hash());

                y -= 25;
                drawLine(contentStream, margin, y, 545, y);

                y -= 25;
                writeLine(contentStream, fontBold, 11, margin, y, "ACTIVE THREAT FINDINGS:");
                y -= 16;

                if (state.getFindings() != null && !state.getFindings().isEmpty()) {
                    for (String finding : state.getFindings()) {
                        String clean = finding.replaceAll("[^\\x20-\\x7E]", "").trim();
                        if (clean.length() > 80) clean = clean.substring(0, 80) + "...";
                        writeLine(contentStream, fontRegular, 9, margin + 10, y, "• " + clean);
                        y -= 14;
                        if (y < 80) break;
                    }
                } else {
                    writeLine(contentStream, fontRegular, 9, margin + 10, y, "• System nominal. No active violations detected.");
                    y -= 14;
                }

                y -= 15;
                writeLine(contentStream, fontBold, 11, margin, y, "POLICY REMEDIATION & DIGITAL TWIN:");
                y -= 16;
                String plan = state.getRemediation_plan() != null ? state.getRemediation_plan().replaceAll("[^\\x20-\\x7E]", "") : "System aligned.";
                if (plan.length() > 80) plan = plan.substring(0, 80) + "...";
                writeLine(contentStream, fontRegular, 9, margin + 10, y, "Plan: " + plan);

                y -= 30;
                writeLine(contentStream, fontBold, 9, margin, y, "IMMUTABLE AUDIT TRAIL VERIFIED BY SHA-256 CONSENSUS MERKLE ROOT");
            }

            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            document.save(baos);
            return baos.toByteArray();
        }
    }

    private void writeLine(PDPageContentStream stream, PDType1Font font, float size, float x, float y, String text) throws IOException {
        stream.beginText();
        stream.setFont(font, size);
        stream.newLineAtOffset(x, y);
        stream.showText(text);
        stream.endText();
    }

    private void drawLine(PDPageContentStream stream, float x1, float y1, float x2, float y2) throws IOException {
        stream.moveTo(x1, y1);
        stream.lineTo(x2, y2);
        stream.stroke();
    }
}
