import type { Handle } from "@sveltejs/kit";
import { env } from "$lib/env.js";
import type { Trads } from "$lib/utils";

export const handle: Handle = async ({ event, resolve }) => {

    const session = event.cookies.get("session");
    if (!session) {
        return await resolve(event);
    }
    // user
    let url = `${env.VITE_BACKEND_DNS}/auth/user/${session}`;
    const user = await fetch(url);
    const email = await user.json();
    url = `${env.VITE_BACKEND_DNS}/auth/rights`;
    const rightsRes = await fetch(url, {
        headers: {
            cookie: `session=${session}`,
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    })
    // rights
    const rights = await rightsRes.json() as []
    if (user) {
        event.locals.user = {
            email: email.email,
            uuid: session,
            rights: rights
        };
    }
    // Skin and type

    url = `${env.VITE_BACKEND_DNS}/gametypesnskins`;
    const res = await fetch(url, {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            cookie: `session=${session}`,
        },
    })
    const gametypesnskins = await res.json();
    event.locals.user.typesNskins = {
        types: gametypesnskins.types,
        skins: gametypesnskins.skins
    };

    // trads

    const tradRes = await fetch(`${env.VITE_BACKEND_DNS}/trads/fr/dash`);
    const trads = await tradRes.json();
    event.locals.user.traduction = trads as Trads;
    return await resolve(event);
};
