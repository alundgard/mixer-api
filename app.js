const express = require('express')
const app = express()
const path = require('path')

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/gen', (req, res) => {

    const dnum = req.query.dnum;
    const fname = req.query.fname;
    const { spawn } = require('child_process');
    const pyProg = spawn('python',['./mixer.py', dnum]);
    var str = "";

    pyProg.stdout.on('data', (data) => {
        str += data.toString();
    });

    pyProg.on('close', (code) => {
        res.set({"Content-Disposition":`attachment; filename=${fname}.json`});
        res.send(str);
    });
    
});

app.listen(4000, () => console.log('app listening on port 4000!'))