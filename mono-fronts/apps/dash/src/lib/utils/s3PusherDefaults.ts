import { env } from "$lib/env.js";
import { s3 } from "$lib/bucket";


export const pushtoS3Defaults = async (file: File, name: string, uuid: string) => {
    const ext = file.name.split(".").pop();
    const fileName = `${env.VITE_S3_ROOT}/${name}/${uuid}.${ext}`;
    const fileBlob: Buffer = Buffer.from(await file.arrayBuffer());
    const params = {
        Bucket: env.VITE_BUCKET,
        Key: fileName,
        Body: fileBlob,
        ACL: "public-read",
    };
    console.log("env.VITE_S3_BUCKET");
    console.log(env.VITE_BUCKET);
    console.log("params", params)
    await s3.putObject(params, function (err, data) {
        if (err) {
            console.log("image not posted", err);
        } else {
            console.log("image => posted", data);
        }
    });
    return `${env.VITE_CDN_URL}/${fileName}`;
}