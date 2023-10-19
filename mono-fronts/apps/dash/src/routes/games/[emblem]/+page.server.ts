import { env } from "$lib/env.js";
import { fail, redirect } from "@sveltejs/kit";
import type { Action, Actions, PageServerLoad } from "./$types";
import { s3 } from "$lib/bucket";
import { pushtoS3Defaults as pushtoS3 } from "$lib/utils";

export const load: PageServerLoad = async ({ locals, params }) => {
    if (!locals.user) {
        throw redirect(302, "/login");
    }
    const headers = {
        Accept: "application/json",
        "Content-Type": "application/json",
        cookie: `session=${locals.user.uuid}`,
    };

    const [gameRes, basicsRes, dateRes, SalonRes, identityRes, formsRes, requestedRes, extrarequestedsRes, pricesRes, dryRunRes] = await Promise.all([
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/basics`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/date`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/salon`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/identity`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/forms`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/requested`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/extrarequesteds`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/prices/dash`,
            { headers }
        ),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/dryrun`,
            { headers }
        ),
    ])
    const [game, basics, date, salon, identity, form, requesteds, extrarequesteds, prices, dryRun] = await Promise.all([
        gameRes.json(),
        basicsRes.json(),
        dateRes.json(),
        SalonRes.json(),
        identityRes.json(),
        formsRes.json(),
        requestedRes.json(),
        extrarequestedsRes.json(),
        pricesRes.json(),
        dryRunRes.json()
    ])
    return {
        game,
        date,
        basics,
        salon,
        identity,
        form,
        requesteds,
        extrarequesteds,
        prices,
        dryRun
    };
};

const getFileName = (data: FormData, perso: boolean): string => {
    console.log("==== Get File Name =====");
    let file: File;
    console.log("joseph");
    if (perso) {
        console.log("martin");
        file = data.get(`logo`) as File;
    } else {
        console.log("msako");
        file = data.get(`img`) as File;
    }
    console.log("jose");
    const date = Date.now();
    console.log("file", file);
    const ext = file.name.split(".").pop();
    return `${env.VITE_S3_ROOT}/${env.VITE_SPCACES_LOGO_IMAGE}/${Math.floor(
        date / 1000
    )}.${ext}`;
};

const getImgName = (img: File): string => {
    console.log("jose");
    const date = Date.now();
    console.log("file sako", img);
    const ext = img.name.split(".").pop();
    return `${env.VITE_S3_ROOT}/${env.VITE_SPCACES_LOGO_IMAGE}/${Math.floor(
        date / 1000
    )}.${ext}`;
};

const getBgName = (img: File): string => {
    console.log("jose");
    const date = Date.now();
    console.log("file nitendo", img);
    const ext = img.name.split(".").pop();
    return `${env.VITE_S3_ROOT}/bg/${Math.floor(date / 1000)}.${ext}`;
};

const basics: Action = async ({ request, locals }) => {
    console.log("==== Edit Basics  =====");
    const data = await request.formData();
    console.log("data", data);
    let bgUrl: string = '';
    const bg = data.get("bgIngame") as File;
    console.log("bg", bg);
    console.log("bg", bg.name);
    if (bg.name !== "undefined") {
        bgUrl = await pushtoS3(bg, "bg", locals.user.uuid);
    }
    const payload = {
        name: data.get("name"),
        gameType: data.get("gameType"),
        skin: data.get("skin"),
        bgUrl,
    };
    try {
        const res = await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/basics`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    cookie: `session=${locals.user.uuid}`,
                },
                method: "PUT",
                body: JSON.stringify(payload),
            }
        );
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }
};

const forms: Action = async ({ request, locals }) => {
    console.log("==== Edit Forms  =====");
    const data = await request.formData();

    const IntroFormLandscape = data.get("IntroFormLandscape") as File;
    const IntroFormPortrait = data.get("IntroFormPortrait") as File;
    let IntroFormLandscapeURL: string = '';
    let IntroFormPortraitURL: string = '';
    if (IntroFormLandscape.name !== "undefined") {
        IntroFormLandscapeURL = await pushtoS3(IntroFormLandscape, "IntroFormLandscape", locals.user.uuid);
    }
    if (IntroFormPortrait.name !== "undefined") {
        IntroFormPortraitURL = await pushtoS3(IntroFormPortrait, "IntroFormPortrait", locals.user.uuid);
    }
    const payload = {
        IntroFormLandscape: IntroFormLandscapeURL,
        IntroFormPortrait: IntroFormPortraitURL,
    };
    try {
        const res = await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/forms`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    cookie: `session=${locals.user.uuid}`,
                },
                method: "PUT",
                body: JSON.stringify(payload),
            }
        );
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }
};

const deleteGame: Action = async ({ request, locals }) => {
    console.log("==== Delete Game =====");
    const data = await request.formData();
    try {
        await fetch(`${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}`, {
            headers: { cookie: `session=${locals.user.uuid}` },
            method: "DELETE",
        });
    } catch {
        return fail(400, { edit: true });
    }
    throw redirect(302, "/games");
};

const requesteds: Action = async ({ request, locals }) => {
    console.log("==== Edit Requested =====");
    const data: FormData = await request.formData();
    const payload = {
        requestName: data.get("requestName"),
        // requestEmail: data.get("requestEmail"),
        requestTel: data.get("requestTel"),
        requestAddress: data.get("requestAddress"),
        isAlwaysWinner: data.get("isAlwaysWinner"),
        canReplay: data.get("canReplay"),
        canReplayToday: data.get("canReplayToday"),
    };
    try {
        const res = await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/requested`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    cookie: `session=${locals.user.uuid}`,
                },
                method: "PUT",
                body: JSON.stringify(payload),
            }
        );
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }
};
const socials: Action = async ({ request, locals }) => {
    console.log("==== Edit Socials =====");
    const data: FormData = await request.formData();
    const payload = {
        facebook: data.get("facebook"),
        twitter: data.get("twitter"),
        insta: data.get("insta"),
    };
    try {
        await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/socials`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    cookie: `session=${locals.user.uuid}`,
                },
                method: "PUT",
                body: JSON.stringify(payload),
            }
        );
    } catch {
        return fail(400, { edit: true });
    }
};
const dryrun: Action = async ({ request, locals }) => {
    console.log("==== Edit DryRun =====");
    const data: FormData = await request.formData();
    const payload = {
        forceResultWon: data.get("forceResultWon"),
        forceResultLost: data.get("forceResultLost"),
        forceResultCantReplay: data.get("forceResultCantReplay"),
        forceResultCantReplayToday: data.get("forceResultCantReplayToday"),
        dryRun: data.get("dryRun"),
    };
    const res = await fetch(
        `${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/dryrun`,
        {
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                cookie: `session=${locals.user.uuid}`,
            },
            method: "PUT",
            body: JSON.stringify(payload),
        }
    );
    if (res.ok) {
        return res.json();
    } else {
        console.log(res)
        return fail(400, { error: res.text });
    }
}

const payableOptions: Action = async ({ request, locals }) => {
    console.log("==== Edit payableOptions =====");
    const data: FormData = await request.formData();
    const payload = {
        email_check: data.get("email_check"),
    };
    try {
        await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get(
                "emblem"
            )}/overrideemailcheck`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    cookie: `session=${locals.user.uuid}`,
                },
                method: "PUT",
                body: JSON.stringify(payload),
            }
        );
    } catch {
        return fail(400, { edit: true });
    }
};

const date: Action = async ({ request, locals }) => {
    console.log("==-------== Edit Dates ===-----==");
    const data: FormData = await request.formData();
    console.log("data molle");
    console.log(data);
    const payload = {
        startDate: data.get("startDate"),
        endDate: data.get("endDate"),
        startHour: data.get("startHour"),
        endHour: data.get("endHour"),
        unlimitedInTime: data.get("unlimitedInTime"),
        losingFactor: data.get("losingFactor"),
        timeZone: data.get("timeZone"),
        extraLangs: data.get("extra-langs"),
    };
    try {
        const res = await fetch(`${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/date`, {
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
const identity: Action = async ({ request, locals }) => {
    console.log("==== Edit Identity =====");
    const data: FormData = await request.formData();
    let imgName;
    let logoCompany = null;
    const file: File = data.get("logo") as File;
    if (file.size !== 0) {
        imgName = getFileName(data, true);
        const fileBlob: Buffer = Buffer.from(await file.arrayBuffer());
        const s3payload = {
            Bucket: env.VITE_BUCKET,
            Key: imgName,
            Body: fileBlob,
            ACL: "public-read",
        };
        await s3.putObject(s3payload, function (err, data) {
            if (err) {
                console.log("image not posted", err);
            } else {
                console.log("image => posted", data);
            }
        });
        logoCompany = `${env.VITE_CDN_URL}/${imgName}`;
    }
    var formOpen: { [key: string]: string } = {};
    var formClose: { [key: string]: string } = {};
    data.forEach(function (value, key) {
        if (key.includes("ope")) {
            formOpen[key] = value as string;
        }
        if (key.includes("clos")) {
            formClose[key] = value as string;
        }
    });

    const payload = {
        opening_text: data.get("startText"),
        closing_text: data.get("endText"),
        opening_texts: formOpen,
        closing_texts: formClose,
        color: data.get("color"),
        logo_company: logoCompany,
    };
    console.log("payload");
    console.log(payload);
    try {
        await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/identity`,
            {
                headers: {
                    cookie: `session=${locals.user.uuid}`,
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                method: "PUT",
                body: JSON.stringify(payload),
            }
        );
    } catch {
        return fail(400, { edit: true });
    }
};
const salon: Action = async ({ request, locals }) => {
    console.log("==== Edit Salon =====");
    const data: FormData = await request.formData();
    const sound = data.get("music") as File;
    let soundBucketURL: string = '';
    if (sound.name !== "undefined") {
        console.log("sound", sound);
        const ext = sound.name.split(".").pop();
        const soundName = `${env.VITE_S3_ROOT}/soundsdefautls/${locals.user.uuid}.${ext}`;
        soundBucketURL = `${env.VITE_CDN_URL}/${soundName}`;
        const fileBlob: Buffer = Buffer.from(await sound.arrayBuffer());
        const payload = {
            Bucket: env.VITE_BUCKET,
            Key: soundName,
            Body: fileBlob,
            ACL: "public-read",
        };
        await s3.putObject(payload, function (err, data) {
            if (err) {
                console.log("image not posted", err);
            } else {
                console.log("image => posted", data);
            }
        });
    }
    else {
        soundBucketURL = data.get("music") as string;
    }
    const payload2 = {
        music: soundBucketURL,
        fullscreen_btn: data.get("fullscreen_btn"),
        restart_btn: data.get("restart_btn"),
        automatic_restart: data.get("automatic_restart"),
        timer: data.get("timer"),
    }
    try {
        const res = await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/salon`,
            {
                headers: {
                    cookie: `session=${locals.user.uuid}`,
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                method: "PUT",
                body: JSON.stringify(payload2),
            }
        );
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }
};

const handelePrice = async (data: FormData) => {
    let price = {
        name: "",
        img: "",
        quantity: 0,
        display_price_name: false,
        consolationPrice: false,
        offset_price_name: "",
        email_template: 0,
        winnableTimeRage: [0],
        trads: {},
    };
    if (data.get(`name`)) {
        price["name"] = data.get(`name`) as string;
    }
    price["quantity"] = data.get(`quantity`) as unknown as number;
    price["consolationPrice"] = data.get(
        `consolationPrice`
    ) as unknown as boolean;
    price["displayPriceName"] = data.get(
        `displayPriceName`
    ) as unknown as boolean;
    price["offset_price_name"] = data.get(`margin`) as string;
    price["emailTemplate"] = data.get(`emailTemplate`) as unknown as number;
    let winATimeRage: number[] = [];
    let trads: {} = {};
    for (let [key, val] of data.entries()) {
        console.log(key, val);
        let tempsName = "";
        let tempsimg = "";
        let exportName = '';

        if (key.includes("winnableTimeRage")) {
            console.log("winnableTimeRage");
            console.log(val);
            winATimeRage.push(val as unknown as number);
        }
        if (key.includes("name-")) {
            exportName = key.replace("name-", "");
            exportName = exportName.substring(5).trim();
            tempsName = val as string;
            if (trads[exportName] !== undefined) {
                trads[exportName]['name'] = val
            }
        }
        if (key.includes("img-")) {
            const file = data.get(key) as File;
            console.log("file");
            console.log(file);
            if (file.name !== "undefined") {
                const imgName = getImgName(file);
                const fileBlob: Buffer = Buffer.from(await file.arrayBuffer());
                const payload = {
                    Bucket: env.VITE_BUCKET,
                    Key: imgName,
                    Body: fileBlob,
                    ACL: "public-read",
                };
                console.log('key.includes("img")');
                console.log(key);
                let exportName = key.replace("img-", "");
                exportName = exportName.substring(5).trim();
                console.log(exportName);
                if (trads[exportName] !== undefined) {
                    trads[exportName]['img'] = `${env.VITE_CDN_URL}/${imgName}`
                }
                // if (trads[exportName] !== undefined) {
                //     trads[exportName] = {
                //         name: trads[exportName].name,
                //         img: `${env.VITE_CDN_URL}/${imgName}`,
                //     };
                // } else {
                //     trads[exportName] = {
                //         img: `${env.VITE_CDN_URL}/${imgName}`,
                //     };
                // }
                tempsimg = `${env.VITE_CDN_URL}/${imgName}`
                await s3.putObject(payload, function (err, data) {
                    if (err) {
                        console.log("image not posted", err);
                    } else {
                        console.log("image => posted", data);
                    }
                });
            }
        }
        trads[exportName] = {
            name: tempsName ? tempsName : "",
            img: tempsimg ? tempsimg : "",
        };
    }
    if (trads.hasOwnProperty('')) {
        delete trads[''];
    }
    price["winnableTimeRage"] = winATimeRage as number[];
    price["trads"] = trads as string[];
    console.log(price);
    return price;
};
const pricecreate: Action = async ({ request, locals }) => {
    console.log("===----= Create Price  ==-----===");
    const data: FormData = await request.formData();
    const price = await handelePrice(data);
    console.log("price ========");
    console.log(price);
    try {
        const res = await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get("emblem")}/prices/dash`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    cookie: `session=${locals.user.uuid}`,
                },
                method: "POST",
                body: JSON.stringify(price),
            }
        );
        return res.json()
    } catch {
        return fail(400, { edit: true });
    }
};

const priceedit: Action = async ({ request, locals }) => {
    console.log("==------= Edit Price  =------====");
    const data: FormData = await request.formData();
    const price = await handelePrice(data);
    try {
        const res = await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get(
                "emblem"
            )}/price/${data.get("id")}`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    cookie: `session=${locals.user.uuid}`,
                },
                method: "PUT",
                body: JSON.stringify(price),
            }
        );
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }
};

const extrarequesteds: Action = async ({ request, locals }) => {
    console.log("==------= Edit extrarequesteds  =------====");
    const data: FormData = await request.formData();
    console.log(data);
    let pack = [];
    for (let [key, val] of data.entries()) {
        console.log(key, val);
        const splitted = key.split("-");
        const index = splitted[0] as unknown as number;
        const jose = {
            id: index,
            key: splitted.slice().toString(),
            val: val,
        };
        pack.push(jose);
    }
    const extraElts = [];
    for (let i = 0; i < pack.length; i++) {
        const element = pack.filter((item) => item.id == i);
        if (element.length > 0) {
            extraElts.push(element);
        }
    }
    console.log();
    const payload = {
        extraElts,
    };
    try {
        const res = await fetch(
            `${env.VITE_BACKEND_DNS}/dash/${data.get(
                "emblem"
            )}/extrarequesteds`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    cookie: `session=${locals.user.uuid}`,
                },
                method: "PUT",
                body: JSON.stringify(payload),
            }
        );
        return res.json();
    } catch {
        return fail(400, { edit: true });
    }
};

export const actions: Actions = {
    basics,
    pricecreate,
    priceedit,
    deleteGame,
    identity,
    date,
    requesteds,
    socials,
    dryrun,
    extrarequesteds,
    payableOptions,
    salon,
    forms,
};
