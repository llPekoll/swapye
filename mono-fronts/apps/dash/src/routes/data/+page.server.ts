import { env } from "$lib/env.js";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {

    const res2 = await fetch(`${env.VITE_BACKEND_DNS}/leads`, {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            cookie: `session=${locals.user.uuid}`,
        },
    });
    const uuid = locals.user.uuid;
    const leads = await res2.json();
    return {
        leads,
        uuid,
    };
};
