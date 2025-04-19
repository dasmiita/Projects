import java.awt.*;
import java.sql.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;

public class DeliveryInfoUI extends JFrame {

    public DeliveryInfoUI() {
        setTitle("Delivery Information");
        setSize(900, 400);
        setLocationRelativeTo(null); // Center the window
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); // Only close this window

        String[] columns = {
            "Delivery ID", "Order ID", "Delivery Address",
            "Delivery Person", "Delivery Time", "Status"
        };

        DefaultTableModel model = new DefaultTableModel(columns, 0);
        JTable table = new JTable(model);
        JScrollPane scrollPane = new JScrollPane(table);

        String query = "SELECT delivery_id, order_id, delivery_address, " +
                       "delivery_person_name, delivery_time, status FROM Delivery_Info";

        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {

            while (rs.next()) {
                int deliveryId = rs.getInt("delivery_id");
                int orderId = rs.getInt("order_id");
                String address = rs.getString("delivery_address");
                String person = rs.getString("delivery_person_name");
                Timestamp time = rs.getTimestamp("delivery_time");
                String status = rs.getString("status");

                Object[] row = {
                    deliveryId, orderId, address, person, time, status
                };
                model.addRow(row);
            }

        } catch (SQLException e) {
            JOptionPane.showMessageDialog(this, "Error loading delivery info: " + e.getMessage());
        }

        add(scrollPane, BorderLayout.CENTER);
        setVisible(true);
    }

    public static void main(String[] args) {
        new DeliveryInfoUI();
    }
}
