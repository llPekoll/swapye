import { env } from "$lib/env.js";
import type { RequestHandler } from "./$types";
import { json } from "@sveltejs/kit";

export const DELETE: RequestHandler = async ({ params, locals }) => {
    const url = `${env.VITE_BACKEND_DNS}/dash/${params.emblem}/formportrait`;
    const res = await fetch(url, {
        method: "DELETE",
        headers: {
            cookie: `session=${locals.user.uuid}`,
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    });
    return json(await res.json());
};
