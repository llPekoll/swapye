import { env } from "$lib/env.js";
import axios from "axios";
import type { Action, Actions, PageServerLoad } from "./$types";
import { fail, redirect } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ params }) => {
    const tradRes = await fetch(`${env.VITE_BACKEND_DNS}/trads/fr/dash`);
    const trads = await tradRes.json();

    return {
        trads,
        token: params.token,
    };
};

const reset: Action = async ({ request }) => {
    let data = await request.formData();
    const payload = {
        password: data.get("password"),
        token: data.get("token"),
    };
    const url = `${env.VITE_BACKEND_DNS}/auth/reset`;
    try {
        await axios.post(url, payload);
    } catch (e) {
        return fail(400, { token: true });
    }
    throw redirect(302, "/login");
};

export const actions: Actions = { reset };
