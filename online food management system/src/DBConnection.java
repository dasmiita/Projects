import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {
    private static final String URL = "jdbc:oracle:thin:@localhost:1521:xe";  // Your DB host/SID
    private static final String USER = "system";  // Replace with your Oracle username
    private static final String PASSWORD = "1234";  // Replace with your Oracle password

    public static Connection getConnection() {
        try {
            // Use the more up-to-date driver class
            Class.forName("oracle.jdbc.OracleDriver");  // Updated driver class
            // Establish and return the connection
            return DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (ClassNotFoundException | SQLException e) {
            System.out.println("Connection failed: " + e.getMessage());
            return null;
        }
    }

    public static void main(String[] args) {
        // Test the connection
        Connection conn = getConnection();
        if (conn != null) {
            System.out.println("Connection successful!");
        } else {
            System.out.println("Connection failed.");
        }
    }
}
