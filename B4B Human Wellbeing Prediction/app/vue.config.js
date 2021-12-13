module.exports = {
  pages: {
    index: {
      entry: "./src/main.ts",
      title: "Brains for Buildings - Satisfaction Predictor"
    }
  },
  pwa: {
    name: "Brains for Buildings - Satisfaction Predictor",
    themeColor: "#36805C"
  },
  transpileDependencies: [
    "vuetify"
  ],
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.(graphql|gql)$/,
          use: "graphql-tag/loader"
        }
      ]
    }
  }
};
