module.exports = function (mongoose) {
  const modelName = "session";

  const Types = mongoose.Schema.Types;

  const Schema = new mongoose.Schema({
    game: {
      type: Types.ObjectId,
      required: true,
      ref: "game",
    },
    user: {
      type: Types.ObjectId,
      required: true,
      ref: "user",
    },
    instance: {
      type: Types.ObjectId,
      ref: "instance",
    },
    server_id: String,
    status: String,
    active: Boolean,
  });

  Schema.statics = {
    collectionName: modelName,
    routeOptions: {
      associations: {
        game: {
          type: "MANY_ONE",
          model: "game",
        },
        instance: {
          type: "MANY_ONE",
          model: "instance",
        },
        user: {
          type: "ONE_ONE",
          model: "user",
        },
      },
    },
  };

  return Schema;
};
