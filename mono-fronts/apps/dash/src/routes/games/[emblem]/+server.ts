import { json } from "@sveltejs/kit";
import { env } from "$lib/env.js";
import type { RequestHandler } from "./$types";

export const DELETE: RequestHandler = async ({ request, locals }) => {
    console.log("========= Delete Price ===========");
    const data = await request.json();
    await fetch(
        `${env.VITE_BACKEND_DNS}/dash/${data.emblem}/price/${data.id}`,
        {
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                cookie: `session=${locals.user.uuid}`,
            },
            method: "DELETE",
        }
    );
    return json({ delete: true });
};
