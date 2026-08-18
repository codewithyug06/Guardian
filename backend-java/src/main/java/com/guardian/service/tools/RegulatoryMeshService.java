package com.guardian.service.tools;

import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class RegulatoryMeshService {

    public static class Node {
        private final String id;
        private final String type; // Topic, Regulation, Policy
        private final String text;

        public Node(String id, String type, String text) {
            this.id = id;
            this.type = type;
            this.text = text;
        }

        public String getId() { return id; }
        public String getType() { return type; }
        public String getText() { return text; }
    }

    private final Map<String, Node> nodes = new LinkedHashMap<>();
    private final Map<String, List<String>> adjacencyList = new LinkedHashMap<>();

    public RegulatoryMeshService() {
        initGraph();
    }

    private void initGraph() {
        addNode("Concept: Encryption", "Topic", "Encryption at rest and in transit.");
        addNode("Concept: Data Retention", "Topic", "Retention periods for financial and user logs.");
        addNode("PCI-DSS 3.4", "Regulation", "PAN must be unreadable anywhere it is stored.");
        addNode("GDPR Art 32", "Regulation", "Security of processing requires state-of-the-art encryption.");
        addNode("Internal Policy Cl 2", "Policy", "Credit Card numbers (PAN) may be stored in plain text.");
        addNode("Internal Policy Cl 1", "Policy", "User logs retained for 5 years.");

        addEdge("Concept: Encryption", "PCI-DSS 3.4");
        addEdge("Concept: Encryption", "GDPR Art 32");
        addEdge("Internal Policy Cl 2", "Concept: Encryption");
        addEdge("PCI-DSS 3.4", "GDPR Art 32");
        addEdge("Internal Policy Cl 1", "Concept: Data Retention");
    }

    public void addNode(String id, String type, String text) {
        nodes.put(id, new Node(id, type, text));
        adjacencyList.putIfAbsent(id, new ArrayList<>());
    }

    public void addEdge(String from, String to) {
        adjacencyList.computeIfAbsent(from, k -> new ArrayList<>()).add(to);
    }

    public Map<String, Node> getNodes() {
        return nodes;
    }

    public Map<String, List<String>> getAdjacencyList() {
        return adjacencyList;
    }

    public String queryRegulatoryMesh(String topicKeyword) {
        List<String> insights = new ArrayList<>();
        String entryNode = null;

        if (topicKeyword != null && (topicKeyword.contains("Credit Card") || topicKeyword.contains("PCI") || topicKeyword.contains("PAN"))) {
            entryNode = "Internal Policy Cl 2";
        } else if (topicKeyword != null && (topicKeyword.contains("Retention") || topicKeyword.contains("Log"))) {
            entryNode = "Internal Policy Cl 1";
        }

        if (entryNode != null && nodes.containsKey(entryNode)) {
            List<String> neighbors = adjacencyList.getOrDefault(entryNode, Collections.emptyList());
            Set<String> impacts = new LinkedHashSet<>();

            for (String neighbor : neighbors) {
                for (String sec : adjacencyList.getOrDefault(neighbor, Collections.emptyList())) {
                    Node secNode = nodes.get(sec);
                    if (secNode != null && "Regulation".equals(secNode.getType())) {
                        impacts.add(sec);
                        for (String tert : adjacencyList.getOrDefault(sec, Collections.emptyList())) {
                            Node tertNode = nodes.get(tert);
                            if (tertNode != null && "Regulation".equals(tertNode.getType())) {
                                impacts.add(tert + " (via Mesh Link)");
                            }
                        }
                    }
                }
            }

            insights.add("[GRAPH TRAVERSAL ROOT]: " + entryNode);
            insights.add("[CONNECTED CONCEPTS]: " + String.join(", ", neighbors));
            insights.add("[DOWNSTREAM IMPACTS]: " + (impacts.isEmpty() ? "None direct" : String.join(", ", impacts)));
        } else {
            insights.add("[GRAPH SCAN]: Multi-Regulation semantic mapping active. Concept: Encryption linked to PCI-DSS 3.4 and GDPR Art 32.");
        }

        return String.join("\n", insights);
    }
}
