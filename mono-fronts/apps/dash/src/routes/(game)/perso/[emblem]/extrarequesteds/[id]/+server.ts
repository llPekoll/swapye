import { env } from "$lib/env.js";
import type { RequestHandler } from "./$types";
import { json } from "@sveltejs/kit";

export const DELETE: RequestHandler = async ({ request, locals, params }) => {
    console.log("========= Delete requeted ===========");
    const res = await fetch(
        `${env.VITE_BACKEND_DNS}/dash/${params.emblem}/extrarequested/${params.id}`,
        {
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                cookie: `session=${locals.user.uuid}`,
            },
            method: "DELETE",
        }
    );
    return json(await res.json());
};
