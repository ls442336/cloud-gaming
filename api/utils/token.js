'use strict';

const jwt = require('jsonwebtoken');

function createToken(user) {
    return jwt.sign({
        id: user._id,
        username: user.username
    },
        process.env.SECRET,
        { algorithm: 'HS256', expiresIn: "1h" }
    );
}

module.exports = createToken;