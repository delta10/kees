const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
    mode: 'development',
    entry: [
        './assets/js/index'
    ],
    output: {
        path: path.resolve('./assets/bundles/'),
        filename: 'app.js'
    },
    module: {
      rules: [
        {
          test: /\.vue$/,
          use: 'vue-loader'
        }
      ]
    },
    plugins: [
      new VueLoaderPlugin(),
      new BundleTracker({filename: './webpack-stats.json'}),
    ]
}