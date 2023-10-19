import { env } from "$lib/env";
import type { PageServerLoad, Action, Actions } from "./$types";
import { fail, redirect } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ locals }) => {
    if (!locals.user) {
        throw redirect(302, "/login");
    }
};

const create: Action = async ({ request, locals }) => {
    let data = await request.formData();
    const payload = {
        type: data.get("gameType"),
        skin: data.get("skin"),
        name: data.get("name"),
    };

    try {
        const res = await fetch(`${env.VITE_BACKEND_DNS}/games`, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                cookie: `session=${locals.user.uuid}`,
            },
            body: JSON.stringify(payload),
        });
        return await res.json();
    } catch {
        return fail(400, { token: true });
    }
};

export const actions: Actions = { create };
