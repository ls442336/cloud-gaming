// api.js
let Hapi = require('@hapi/hapi')
let mongoose = require('mongoose')
const { ObjectId } = require('mongodb');
let RestHapi = require('rest-hapi')
let createToken = require('./utils/token')
const Boom = require('boom');

require('dotenv').config()

const validate = async function (decoded, request, h) {
    const AdminUser = mongoose.model("AdminUser");

    let user = await AdminUser.findOne({
        username: decoded.username
    })

    if (user == null) {
        return { isValid: false };
    }
    else {
        return { isValid: true };
    }
};

const verifyCredentials = async (req, h) => {
    const { username, password } = req.payload;

    const user = await mongoose.model('AdminUser').findOne({
        "username": username,
        "password": password
    });

    if (user) {
        if (user.username == username && user.password == password) {
            return h.response(user);
        }
        else {
            throw Boom.badRequest('Username ou senha errados');
        }
    }

    throw Boom.badRequest('Usuário não encontrado')
}

async function api() {
    try {
        let server = Hapi.Server({ port: parseInt(process.env.SERVER_PORT) })

        await server.register({
            plugin: require('hapi-cors'),
            options: {
                origins: ['*'],
                methods: ['*'],
            }
        });

        await server.register(require('hapi-auth-jwt2'));

        server.auth.strategy('jwt', 'jwt',
            {
                key: process.env.SECRET, // Never Share your secret key
                validate,
                verifyOptions: {
                    algorithms: ['HS256']    // specify your secure algorithm
                }
            });

        server.auth.default('jwt');

        let config = {
            appTitle: "CloudGaming API",
            cor: {
                additionalHeaders: [],
                additionalExposedHeaders: []
            },
            enableCreatedAt: true,
            enableUpdatedAt: true,
            enableDeletedAt: true,
            enableCreatedBy: false,
            enableUpdatedBy: false,
            enableDeletedBy: false,
            enableTextSearch: true,

            enableAuditLog: false,

            embedAssociations: true,

            authStrategy: "jwt",

            mongo: {
                URI: `${process.env.DB_URL}`,
                options: {}
            }
        };

        await server.register({
            plugin: RestHapi,
            options: {
                mongoose,
                config
            }
        })

        server.route([
            {
                method: "POST",
                path: "/authenticate",
                config: {
                    auth: false,
                    pre: [
                        { method: verifyCredentials, assign: 'user' }
                    ],
                    handler: function (req, h) {
                        return h.response({ token: createToken(req.pre.user) }).code(201);
                    }
                }
            }
        ])

        server.route([
            {
                method: "GET",
                path: "/sessions/last-dates",
                config: {
                    auth: false,
                    handler: async function (req, h) {
                        const limit = req.query.limit
                        const days = req.query.days

                        const Session = mongoose.model("session");

                        const results = await Session.find({
                            _id: {
                                $gt: ObjectId.createFromTime(Date.now() / 1000 - parseInt(days) * 24 * 60 * 60)
                            }
                        },
                            {
                                createdAt: 1, _id: 0
                            }).sort({
                                createdAt: 1
                            }).limit(parseInt(limit))


                        return h.response(results).code(201);
                    }
                }
            }
        ])

        server.route([
            {
                method: "GET",
                path: "/games/most-popular",
                config: {
                    auth: false,
                    handler: async function (req, h) {
                        const limit = req.query.limit

                        const Session = mongoose.model("session");

                        const results = await Session.aggregate([
                            {
                                "$group": {
                                    "_id": "$game",
                                    "count": {
                                        "$sum": 1
                                    }
                                }
                            },
                            {
                                "$lookup": {
                                    "from": 'games',
                                    "localField": '_id',
                                    "foreignField": '_id',
                                    "as": 'game'
                                }
                            },
                            {
                                "$unwind": "$game"
                            },
                            {
                                "$limit": parseInt(limit)
                            },
                            {
                                "$sort": {
                                    "count": 1
                                }
                            }
                        ])

                        return h.response(results).code(201);
                    }
                }
            }
        ])

        await server.start()

        console.log("Server ready", server.info)

        return server
    } catch (err) {
        console.log("Error starting server:", err);
    }
}

module.exports = api()