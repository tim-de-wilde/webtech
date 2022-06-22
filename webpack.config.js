const path = require('path')

module.exports = {
    mode: 'development',
    entry: './src/resources/js/index.js',
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, 'src/static/js'),
    }
}