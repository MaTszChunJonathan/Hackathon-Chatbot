const { MongoClient } = require('mongodb');

// Connection URL
const url = 'mongodb://mongodb:27017';

// Database Name
const dbName = 'mongodb';

// Create a new MongoClient
const client = new MongoClient(url);

// Connect to the MongoDB server
client.connect(function(err) {
    if (err) {
        console.error('Failed to connect to MongoDB:', err);
        return;
    }

    console.log('Connected successfully to MongoDB');

    // Get the database object
    const db = client.db(dbName);

    // Perform database operations here

    // Close the connection
    client.close();
});

// Add your code here to perform database operations