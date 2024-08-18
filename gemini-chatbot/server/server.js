
const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');

const app = express();
const port = 5000;

app.use(cors());

const url = 'mongodb://localhost:27017';
const dbName = 'mongodb';

const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true });

async function connectToMongoDB() {
    try {
        await client.connect();
        console.log('Connected successfully to MongoDB');
        const db = client.db(dbName);
        return db;
    } catch (err) {
        console.error('Failed to connect to MongoDB:', err);
        throw err;
    }
}

app.get('/top10equip', async (req, res) => {
    try {
        const db = await connectToMongoDB();
        const collection = db.collection('equipment');
        const top10Equip = await collection.find().sort({ price: -1 }).limit(10).toArray();
        res.json(top10Equip);
    } catch (err) {
        res.status(500).send(err.toString());
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});