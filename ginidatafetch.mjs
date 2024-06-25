import fetch from 'node-fetch';
import { MongoClient } from 'mongodb';


const url = 'mongodb+srv://---------';

const client = new MongoClient(url);

const apiCalls = [
    { url: 'https://api.geniidata.com/api/1/brc20/balance?limit=20&offset=0&tick=ordi', collection: 'balances' },
    { url: 'https://api.geniidata.com/api/1/brc20/tickinfo/ordi', collection: 'tickinfo' },
    { url: 'https://api.geniidata.com/api/1/brc20/ticks?limit=20&offset=0', collection: 'ticks' },
    { url: 'https://api.geniidata.com/api/1/brc20/address/bc1pv00lg0mj34g2uwgznd4slp7ezsace5kvjlyrfe9hpxzahflgnemqny7r8x/tick/ordi/transferableInscriptions?limit=20&offset=0', collection: 'transferableInscriptions' },
    { url: 'https://api.geniidata.com/api/1/sns/namelist?limit=20&offset=0&relay=all&rev=all&avatar=all', collection: 'namelist' },
    { url: 'https://api.geniidata.com/api/1/sns/namespace/sats/names?limit=20&offset=0&relay=all&rev=all&avatar=all', collection: 'namespaceNames' },
    { url: 'https://api.geniidata.com/api/1/sns/name/ua0h.sats', collection: 'nameDetails' },
    { url: 'https://api.geniidata.com/api/1/collection/balances/bc1p020r7guuhs8wzurhgjnfj5m3l6mfk7fk5uzrtq9ec2zhjewepmdqn6kqpx?collection_id=genesis', collection: 'collectionBalances' },
    { url: 'https://api.geniidata.com/api/1/collection/genesis/holders?offset=0&limit=20', collection: 'collectionHolders' }
];

const options = {
    method: 'GET',
    headers: { accept: 'application/json', 'api-key': '' }
};

async function fetchAndSaveData() {
    try {
        await client.connect();
        console.log('Connected to MongoDB');
        const database = client.db('mongodb'); // Using 'sandbox' as the database name

        for (const call of apiCalls) {
            const response = await fetch(call.url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            const collection = database.collection(call.collection);
            await collection.insertOne(data);
            console.log(`Data inserted into collection ${call.collection}`);
        }
    } catch (error) {
        console.error('Failed to fetch or save data:', error);
    } finally {
        await client.close();
    }
}

// Run the function
fetchAndSaveData();
setInterval(fetchAndSaveData, 3000); // 

export { fetchAndSaveData };
