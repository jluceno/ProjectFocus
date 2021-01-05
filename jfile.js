const {app, BrowserWindow} = require('electron')
const path = require('path') 

function createWindow() {
    window = new BrowserWindow({ width: 800, height: 600 })

    // TODO have the option to start separately
    var python = require('child_process').spawn('python', ['./main.py']);
    python.stdout.on('data', function(data){
        console.log("data: ", data.toString('utf8'));
    });

    window.loadURL('http://127.0.0.1:5000/');
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})