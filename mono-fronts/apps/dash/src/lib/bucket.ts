import { env } from "$lib/env.js";

import AWS from "aws-sdk";

const spacesEndpoint = new AWS.Endpoint(env.VITE_ENDPOINT);

export const s3 = new AWS.S3({
    endpoint: spacesEndpoint,
    accessKeyId: env.VITE_SPACES_KEY,
    secretAccessKey: env.VITE_SPACES_SECRET,
});