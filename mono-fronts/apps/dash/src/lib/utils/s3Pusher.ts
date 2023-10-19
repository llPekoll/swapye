import { env } from "$lib/env.js";
import { s3 } from "$lib/bucket";


export const pushtoS3 = async (file: File, name: string, uuid: string) => {
    const ext = file.name.split(".").pop();
    const fileName = `${env.VITE_S3_ROOT}/${name}/${uuid}.${ext}`;
    const fileBlob: Buffer = Buffer.from(await file.arrayBuffer());
    const params = {
        Bucket: env.VITE_BUCKET,
        Key: fileName,
        Body: fileBlob,
        ACL: "public-read",
    };
    await s3.putObject(params, function (err, data) {
        if (err) {
            console.log("image not posted", err);
        }
    });
    return `${env.VITE_CDN_URL}/${fileName}`;
}