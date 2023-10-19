import { env } from "$lib/env.js";
import type { RequestHandler } from "./$types";
import { json } from "@sveltejs/kit";

export const POST: RequestHandler = async ({ params, locals }) => {
    const url = `${env.VITE_BACKEND_DNS}/unlock/price/${params.unlockcode}`;
    const res = await fetch(url,  {
        method: "POST",
        headers: {
            cookie: `session=${locals.user.uuid}`,
            "Content-Type": "application/json",
        },
    });
    return json(await res.json());
};
