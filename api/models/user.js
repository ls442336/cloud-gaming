module.exports = function (mongoose) {
  const modelName = "user";

  const Types = mongoose.Schema.Types;

  const Schema = new mongoose.Schema({
    conn_id: String,
    server_id: String,
    active: Boolean,
    owner: {
      type: Types.ObjectId,
      ref: "session"
    }
  });

  Schema.statics = {
    collectionName: modelName,
    routeOptions: {
      associations: {
        owner: {
          type: "ONE_ONE",
          model: "session"
        }
      },
    },
  };

  return Schema;
};
