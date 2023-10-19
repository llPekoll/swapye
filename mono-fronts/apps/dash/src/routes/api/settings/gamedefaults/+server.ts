import { env } from "$lib/env.js";
import type { RequestHandler } from "./$types";
import { json } from "@sveltejs/kit";

export const GET: RequestHandler = async ({ locals }) => {
    const url = `${env.VITE_BACKEND_DNS}/gamedefaults`;
    const res = await fetch(url, {
        headers: {
            cookie: `session=${locals.user.uuid}`,
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    });
    return json(await res.json());
};
