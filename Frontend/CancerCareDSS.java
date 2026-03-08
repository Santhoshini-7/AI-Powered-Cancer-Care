import javax.swing.*;
import java.awt.*;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class CancerCareDSS extends JFrame {

    public CancerCareDSS() {
        setTitle("Cancer Care Decision Support System - Session 8");
        setSize(600, 700);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        
        JTabbedPane tabs = new JTabbedPane();
        tabs.addTab("Risk Assessment", createRiskPanel());
        tabs.addTab("Diagnosis", createDiagnosisPanel());
        tabs.addTab("Prognosis", createPrognosisPanel());
        
        add(tabs);
    }

    // --- TAB 1: RISK ASSESSMENT ---
    private JPanel createRiskPanel() {
        JPanel p = new JPanel(new GridLayout(9, 2, 10, 10));
        p.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        JTextField ageField = new JTextField();
        JComboBox<String> genBox = new JComboBox<>(new String[]{"Select", "Male", "Female"});
        
        JSlider smokeSlider = new JSlider(0, 10, 0);
        smokeSlider.setMajorTickSpacing(1);
        smokeSlider.setPaintTicks(true);
        smokeSlider.setPaintLabels(true);

        JTextField geneField = new JTextField();
        JComboBox<String> locBox = new JComboBox<>(new String[]{"Select", "Urban", "Rural"});
        
        JButton btn = new JButton("Calculate Risk Score");
        JLabel res = new JLabel("Risk: --", SwingConstants.CENTER);

        p.add(new JLabel("Age:")); p.add(ageField);
        p.add(new JLabel("Gender:")); p.add(genBox);
        p.add(new JLabel("Smoking Level:")); p.add(smokeSlider);
        p.add(new JLabel("Genetic Risk (0-10):")); p.add(geneField);
        p.add(new JLabel("Location:")); p.add(locBox);
        p.add(new JLabel("")); p.add(new JLabel(""));
        p.add(btn); p.add(res);

        btn.addActionListener(e -> {
            if(genBox.getSelectedIndex() == 0 || locBox.getSelectedIndex() == 0) {
                res.setText("Select all fields!"); return;
            }
            String json = String.format("{\"age\":\"%s\",\"gender\":\"%s\",\"smoking\":%d,\"genetic\":\"%s\",\"location\":\"%s\"}",
                          ageField.getText(), genBox.getSelectedItem(), smokeSlider.getValue(), geneField.getText(), locBox.getSelectedItem());
            res.setText("Score: " + callAPI("risk", json));
        });
        return p;
    }

    // --- TAB 2: DIAGNOSIS ---
    private JPanel createDiagnosisPanel() {
        JPanel p = new JPanel(new GridLayout(6, 2, 10, 10));
        p.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        JTextField rad = new JTextField();
        JTextField tex = new JTextField();
        JTextField per = new JTextField();
        JButton btn = new JButton("Run Diagnosis");
        JLabel res = new JLabel("Result: --", SwingConstants.CENTER);

        p.add(new JLabel("Mean Radius:")); p.add(rad);
        p.add(new JLabel("Mean Texture:")); p.add(tex);
        p.add(new JLabel("Mean Perimeter:")); p.add(per);
        p.add(new JLabel("")); p.add(new JLabel(""));
        p.add(btn); p.add(res);

        btn.addActionListener(e -> {
            String json = String.format("{\"radius\":\"%s\",\"texture\":\"%s\",\"perimeter\":\"%s\"}", rad.getText(), tex.getText(), per.getText());
            res.setText("Result: " + callAPI("diagnosis", json));
        });
        return p;
    }

    // --- TAB 3: PROGNOSIS (RECTIFIED) ---
    private JPanel createPrognosisPanel() {
        JPanel p = new JPanel(new GridLayout(5, 2, 10, 10));
        p.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        // Note: Strings must match the Python dictionary keys exactly
        JComboBox<String> aggBox = new JComboBox<>(new String[]{"Select", "Low", "Medium", "High"});
        JComboBox<String> stgBox = new JComboBox<>(new String[]{"Select", "I", "II", "III", "IV"});
        JButton btn = new JButton("Predict Recurrence");
        JLabel res = new JLabel("Outcome: --", SwingConstants.CENTER);

        p.add(new JLabel("Tumor Aggressiveness:")); p.add(aggBox);
        p.add(new JLabel("Cancer Stage:")); p.add(stgBox);
        p.add(new JLabel("")); p.add(new JLabel(""));
        p.add(btn); p.add(res);

        btn.addActionListener(e -> {
            // Check if user has picked a real value
            if(aggBox.getSelectedIndex() == 0 || stgBox.getSelectedIndex() == 0) {
                res.setText("Please select options!");
                return;
            }
            // Send simple keys: "agg" and "stage"
            String json = String.format("{\"agg\":\"%s\",\"stage\":\"%s\"}", 
                          aggBox.getSelectedItem().toString(), stgBox.getSelectedItem().toString());
            res.setText("Recurrence: " + callAPI("prognosis", json));
        });
        return p;
    }

    // --- API CALLER ---
    private String callAPI(String endpoint, String json) {
        try {
            URL url = new URL("http://127.0.0.1:5000/predict_" + endpoint);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);
            try (OutputStream os = conn.getOutputStream()) { os.write(json.getBytes()); }
            
            // Check for 200 OK
            if (conn.getResponseCode() != 200) { return "Model Error (500)"; }

            Scanner s = new Scanner(conn.getInputStream());
            String response = s.useDelimiter("\\A").next().replace("\"", "");
            s.close();
            return response;
        } catch (Exception e) {
            return "Connection Failed";
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new CancerCareDSS().setVisible(true));
    }
}