// See https://github.com/yandeu/five-server
module.exports = {
    root: '/',
    host: 'localhost',
    open: '/',
    watch: ['lmo_web', 'index.html', 'pyscript.toml'],

    // enable highlight feature
    highlight: true,
    // enable instant update
    injectBody: false,
    // enable remoteLogs
    remoteLogs: true,
    // disable injecting css
    injectCss: false,
    // enable auto-navigation
    navigate: false,
};
