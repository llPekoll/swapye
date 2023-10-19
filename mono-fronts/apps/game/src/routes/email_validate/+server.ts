import { env } from "$lib/env.js";
import type { RequestHandler } from "@sveltejs/kit";
import { json } from "@sveltejs/kit";

export const POST: RequestHandler = async ({ request }) => {
    const payload = await request.json();
    console.log("======== check lead email =======🚀");
    const res = await fetch(`${env.VITE_BACKEND_DNS}/play/email_validation`, {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });
    return json(await res.json());
};
