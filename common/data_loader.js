const fs = require('fs');
const path = require('path');

function loadData(dataPath) {
    const data = [];
    const stats = fs.statSync(dataPath);

    if (stats.isDirectory()) {
        const files = fs.readdirSync(dataPath);
        for (const file of files) {
            data.push(fs.readFileSync(path.join(dataPath, file), 'utf8'));
        }
    } else if (dataPath.endsWith('.jsonl')) {
        const lines = fs.readFileSync(dataPath, 'utf8').split('\n').filter(Boolean);
        for (const line of lines) {
            data.push(JSON.parse(line).payload);
        }
    } else if (dataPath.endsWith('.csv')) {
        const lines = fs.readFileSync(dataPath, 'utf8').split('\n').filter(Boolean);
        for (let i = 1; i < lines.length; i++) {
            data.push(lines[i]);
        }
    }
    return data;
}

module.exports = { loadData };
