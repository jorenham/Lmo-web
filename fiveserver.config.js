// See https://github.com/yandeu/five-server
module.exports = {
    root: '/',
    host: 'localhost',
    open: '/',
    watch: [
        'lmo_web',
        'index.html',
        'pyscript.toml'
    ],
    ignore: [
        /\.s[ac]ss$/i,
        /\.tsx?$/i,
        /\.pyi$/i,
        /\.json$/i,
        '**/.venv',
        '**/.vscode',
        '**.json',
        '**/fiveserver.config.js',
        'README.md',
        'pyproject.toml',
        'poetry.lock',
        '**.typings'
    ],
    highlight: false,
    injectBody: true,
    remoteLogs: true,
    injectCss: false,
    navigate: false,
    debugVSCode: true
};
