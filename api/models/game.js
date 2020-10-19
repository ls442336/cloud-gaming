module.exports = function (mongoose) {
  const modelName = 'game'

  const Schema = new mongoose.Schema({
    name: String,
    description: String,
    path: String,
    thumbnail_url: String,
    background_url: String,
    bucket_id: String
  })

  Schema.statics = {
    collectionName: modelName,
    routeOptions: {
      readAuth: false,
      associations: {
        sessions: {
          type: "ONE_MANY",
          foreignField: "session",
          model: "session"
        }
      }
    }
  }

  return Schema
}
