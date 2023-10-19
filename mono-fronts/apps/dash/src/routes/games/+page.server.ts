import { env } from "$lib/env.js";
import type { PageServerLoad } from "./$types";
import { redirect } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ locals }) => {
    if (!locals.user) {
        throw redirect(302, "/login");
    }
    const res2 = await fetch(`${env.VITE_BACKEND_DNS}/games`, {
        headers: {
            cookie: `session=${locals.user.uuid}`,
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    });
    const games = await res2.json();
    return {
        games,
    };
};
