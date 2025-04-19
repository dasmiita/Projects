import java.awt.*;
import java.sql.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;

public class CategoriesUI extends JFrame {

    public CategoriesUI() {
        setTitle("Categories List");
        setSize(600, 300);
        setLocationRelativeTo(null); // center
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); // close this window only

        // Table columns
        String[] columnNames = {"Category ID", "Category Name"};
        DefaultTableModel tableModel = new DefaultTableModel(columnNames, 0);
        JTable table = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(table);

        // Load data from DB
        String query = "SELECT category_id, category_name FROM Categories";

        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {

            while (rs.next()) {
                Object[] row = {
                    rs.getInt("category_id"),
                    rs.getString("category_name")
                };
                tableModel.addRow(row);
            }

        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Failed to load categories: " + e.getMessage());
        }

        add(scrollPane, BorderLayout.CENTER);
        setVisible(true);
    }

    // Main method to run the CategoriesUI
    public static void main(String[] args) {
        new CategoriesUI();
    }
}
