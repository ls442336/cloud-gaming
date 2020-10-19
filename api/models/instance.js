module.exports = function (mongoose) {
  const modelName = "instance";

  const Schema = new mongoose.Schema({
    server_id: String,
    conn_id: String,
    active: Boolean,
    ready: Boolean,
  });

  Schema.statics = {
    collectionName: modelName,
    routeOptions: {
      associations: {
        sessions: {
          type: "ONE_MANY",
          foreignField: "session",
          model: "session"
        }
      },
    },
  };

  return Schema;
};
