import { env } from "$lib/env.js";
import { fail, redirect } from "@sveltejs/kit";
import type { Action, Actions, PageServerLoad } from "./$types";
import { pushtoS3Defaults as pushtoS3 } from "$lib/utils";

export const load: PageServerLoad = async ({ locals }) => {
    if (!locals.user) {
        throw redirect(302, "/login");
    }
    const [personalsRes, apikeyRes, defaultsRes] = await Promise.all([
        fetch(`${env.VITE_BACKEND_DNS}/personals`, {
            headers: {
                cookie: `session=${locals.user.uuid}`,
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        }),
        fetch(`${env.VITE_BACKEND_DNS}/apikey`, {
            headers: {
                cookie: `session=${locals.user.uuid}`,
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        }),
        fetch(`${env.VITE_BACKEND_DNS}/gamedefaults`, {
            headers: {
                cookie: `session=${locals.user.uuid}`,
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        })
    ])
    const [personals, apiKey, defaults] = await Promise.all([
        personalsRes.json(),
        apikeyRes.json(),
        defaultsRes.json()
    ])
    return {
        personals,
        apiKey,
        defaults,
    };
};

const personal: Action = async ({ request, locals }) => {
    console.log("==== Edit Personal  =====");
    const data: FormData = await request.formData();
    const payload = {
        name: data.get("name"),
        address: data.get("address"),
        postal: data.get("postal"),
        city: data.get("city"),
        conact_email: data.get("emailContact"),
        company_name: data.get("companyName"),
        rib: data.get("rib"),
        siret: data.get("siret"),
        phone: data.get("phone"),
    };
    try {
        const res = await fetch(`${env.VITE_BACKEND_DNS}/personals`, {
            headers: {
                cookie: `session=${locals.user.uuid}`,
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            method: "PUT",
            body: JSON.stringify(payload),
        });
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }
};

const apikey: Action = async ({ request, locals }) => {
    console.log("==== Edit ApiKey  =====");
    const data: FormData = await request.formData();
    const payload = {
        provider: data.get("provider"),
        apikey: data.get("key"),
        apipass: data.get("secret"),
        email: data.get("email"),
        display_name: data.get("displayName"),
    };
    try {
        const res = await fetch(`${env.VITE_BACKEND_DNS}/apikey`, {
            headers: {
                cookie: `session=${locals.user.uuid}`,
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            method: "PUT",
            body: JSON.stringify(payload),
        });
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }

};


const gameDefaults: Action = async ({ request, locals }) => {
    console.log("==== Edit EMail validator  =====");
    const data: FormData = await request.formData();
    const payload = {
        email_check: data.get("email_check"),
    };
    const logo = data.get("logo") as File;
    const sound = data.get("music") as File;
    let logoBucketURL: string = '';
    let soundBucketURL: string = '';
    if (logo.name !== "undefined") {
        console.log("sako");
        console.log(env.VITE_S3_BUCKET);
        logoBucketURL = await pushtoS3(logo, 'defautlsLogo', locals.user.uuid);
    }
    if (sound.name !== "undefined") {
        console.log("sound", sound);
        soundBucketURL = await pushtoS3(sound, 'defautlsSounds', locals.user.uuid);
    }

    const payload2 = {
        email_check: data.get("email_check"),
        logo: logoBucketURL,
        music: soundBucketURL,
    }
    console.log("payload2", payload2);
    try {
        const res = await fetch(`${env.VITE_BACKEND_DNS}/gamedefaults`, {
            headers: {
                cookie: `session=${locals.user.uuid}`,
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            method: "PUT",
            body: JSON.stringify(payload2),
        });
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }

};

export const actions: Actions = {
    personal,
    apikey,
    gameDefaults,

};
