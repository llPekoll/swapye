import { env } from "$lib/env.js";
import type { RequestHandler } from "./$types";
import { json } from "@sveltejs/kit";

export const POST: RequestHandler = async ({ params, locals, request }) => {
    const url = `${env.VITE_BACKEND_DNS}/dash/${params.emblem}/price/qr`;
    const payload = await request.json();
    const res = await fetch(url, {
        method: "POST",
        headers: {
            cookie: `session=${locals.user.uuid}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload)
    });
    return json(await res.json());
};
