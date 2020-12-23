const {app, BrowserWindow} = require('electron')

function createWindow() {
    window = new BrowserWindow({width: 800, height: 600})
    window.loadFile('hfile.html')

    var python = require('child_process').spawn('python', ['./main.py']);
    python.stdout.on('data', function(data){
        console.log("data: ", data.toString('utf8'));
    });

    var { PythonShell } = require('python-shell');
    PythonShell.run('main.py', null, function (err, results) {
        if (err) throw err;
        console.log('main.py finished.');
        console.log('results: ', results);
    });

}


app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})