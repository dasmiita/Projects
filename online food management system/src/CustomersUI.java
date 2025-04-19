import java.awt.*;
import java.sql.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;

public class CustomersUI extends JFrame {

    public CustomersUI() {
        setTitle("Customer List");
        setSize(600, 400);
        setLocationRelativeTo(null); // center
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); // only close this window

        // Table columns
        String[] columnNames = {"Customer ID", "Name", "Phone", "Email", "Address"};
        DefaultTableModel tableModel = new DefaultTableModel(columnNames, 0);
        JTable table = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(table);

        // Load data from DB
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM Customers")) {

            while (rs.next()) {
                Object[] row = {
                    rs.getInt("cust_id"),
                    rs.getString("name"),
                    rs.getString("phone"),
                    rs.getString("email"),
                    rs.getString("address")
                };
                tableModel.addRow(row);
            }

        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Failed to load customers: " + e.getMessage());
        }

        add(scrollPane, BorderLayout.CENTER);
        setVisible(true);
    }

    // Add this main method to run the application
    public static void main(String[] args) {
        new CustomersUI();  // Launch the CustomersUI JFrame
    }
}
