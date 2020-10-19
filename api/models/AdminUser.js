module.exports = function (mongoose) {
  const modelName = "AdminUser";
  
  const Schema = new mongoose.Schema({
    username: String,
    password: String
  });

  Schema.statics = {
    collectionName: modelName,
    routeOptions: {
      associations: {},
    },
  };

  return Schema;
};
