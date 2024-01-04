/**
 * This server proxies requests to Judge0.
 * It modifies GET requests to `/submissions`, and adds the key 'flag', 
 * which is either an empty string, or the flag for that challenge.
 * It also defined the endpoint `/challenge_info/:id`, which will return the 
 * prompt and expected output for the associated id.
 * 
 * Our custom IDE uses this wrapper to know when the user has solved the challege.
 * 
 * Note that there can only be one correct answer or output per challenge.
 */
"use strict";

const yaml = require('js-yaml');
const fs = require('fs');
const express = require('express');
const morgan = require("morgan");
const { createProxyMiddleware, responseInterceptor } = require('http-proxy-middleware');

/**
 * extracts a flag from a challenge.yml file
 * @param {string} filepath 
 * @returns {string}
 */
function getFlag(filepath) {
    let config = yaml.load(fs.readFileSync(filepath, 'utf8'));
    return config.flags[0];
}

/**
 * Reads the challenges from challenges.yml and parses their flags 
 * from the associated challenges in CTFd.
 * @returns {{challenge_id: Number, language_id: Number, prompt: String, answer: String, flag: String}[]}
 */
function getChallenges() {
    let challenges = yaml.load(fs.readFileSync('challenges.yml', 'utf8')).challenges;
    return challenges.map(challenge => {
        const challengeWithFlag = {
            flag: getFlag(challenge.flag_path),
            ...challenge
        };
        delete challengeWithFlag.flag_path;
        return challengeWithFlag;
    });
}

/**
 * This decode method is taken from the Judge0 IDE.
 * It matches the response from the Judge0 backend.
 * It is used to decode stdout.
 * @param {string} bytes 
 * @returns string
 */
function decode(bytes) {
    var escaped = escape(atob(bytes || ""));
    try {
        return decodeURIComponent(escaped);
    } catch {
        return unescape(escaped);
    }
}

const CHALLENGES = getChallenges();

// Create Express Server
const app = express();

// Configuration
const PORT = 3000;
const HOST = "localhost";
const JUDGE0_URL = "http://localhost:2358";

// Logging
app.use(morgan('dev'));

// get prompts and expected outputs
app.get('/challenge_info/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const challenge = CHALLENGES.find(challenge => challenge.challenge_id === id);
    if (!challenge) {
        console.error(`cannot find id '${id}'`)
        res.status(404).send({ prompt: "", answer: "" });
        return;
    }
    res.send({ prompt: challenge.prompt, answer: challenge.answer });
});

// Proxy endpoint
app.use('/submissions', createProxyMiddleware({
    target: JUDGE0_URL,
    changeOrigin: false,
    selfHandleResponse: true, // res.end() will be called internally by responseInterceptor()
    /**
     * Intercept response and inject "flag" key into submissions, 
     * so that the flag can be displayed in our custom IDE.
     **/
    onProxyRes: responseInterceptor(async (responseBuffer, proxyRes, req, res) => {
        if (req.method !== "GET" || responseBuffer.length == 0) {
            return responseBuffer; // only intercept GET requests with data
        }

        try {
            // get the challenge_id
            const id = parseInt(req.query.challenge_id);
            if (isNaN(id)) {
                throw new TypeError(`could not parse id '${req.query.challenge_id}'`);
            }
            // parse the response
            let response = responseBuffer.toString("utf-8");
            response = JSON.parse(response);
            // figure out if the user should get the flag or not
            const flag = (() => {
                if (!response.stdout) {
                    return "";
                }
                const challenge = CHALLENGES.find(challenge => challenge.challenge_id === id);
                const userOutput = decode(response.stdout);
                if (userOutput === challenge.answer) {
                    return challenge.flag;
                }
                return "";
            })();
            // add the flag into the response
            response = {
                flag: flag,
                ...response
            }

            return JSON.stringify(response);
        } catch (error) {
            console.error(error)
            res.status(500);
            return "";
        }
    }),
}));

// Start the Proxy
app.listen(PORT, HOST, () => {
    console.log(`Starting Proxy at http://${HOST}:${PORT}`);
});
